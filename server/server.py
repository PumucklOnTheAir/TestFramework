from .serverproxy import ServerProxy
from .ipc import IPC
from .test import FirmwareTest
from typing import List, Union, Iterable, Optional
from router.router import Router
from power_strip.power_strip import PowerStrip
from config.configmanager import ConfigManager
from multiprocessing.pool import Pool
from log.loggersetup import LoggerSetup
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from unittest.result import TestResult
import importlib
from multiprocessing import Event
from threading import Event as DoneEvent
from threading import Semaphore
from network.remote_system import RemoteSystem, RemoteSystemJob
from unittest import defaultTestLoader
from pyroute2 import netns
from collections import deque
import os
import sys
import signal
import platform
from setproctitle import setproctitle

if os.geteuid() == 0 and not os.environ.get('TRAVIS') and platform.system() == "Linux":
    from util.router_info import RouterInfoJob
    from util.router_online import RouterOnlineJob
    from network.nv_assist import NVAssistent
    from util.router_reboot import RouterRebootJob
    from util.router_setup_web_configuration import RouterWebConfigurationJob
    from util.router_flash_firmware import SysupgradeJob
    from util.router_flash_firmware import Sysupdate
    from util.register_public_key import RegisterPublicKey

# type alias
FirmwareTestClass = type(FirmwareTest)
RemoteSystemJobClass = type(RemoteSystemJob)


# initialization method for processes of the task pool
def init_process(event):
    setproctitle("PoolProcess")

    # register the stop signal for CTRL+C
    def signal_handler(signal, frame):
        event.set()
    signal.signal(signal.SIGINT, signal_handler)


class Server(ServerProxy):
    """ The great runtime server for all tests and more.
    This static class with class methods will be usually run as daemon on the main server.
    It is used to control the other routers, flash the firmwares and execute such as evaluate the tests.
    The web server and cli instances are connecting with this class
    and using its inherit public methods of :py:class:`ServerProxy`.

    Troubleshooting at server start:

        *OSError: [Errno 48] Address already in use" server is already started*

        *OSError: [Errno 99] Cannot assign requested address" try to restart the computer TODO #51*
    """""
    VERSION = "0.2"
    DEBUG = False
    VLAN = True
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
    CONFIG_PATH = os.path.join(BASE_DIR, 'config')  # Join Project Root with config

    _ipc_server = IPC()

    # runtime vars
    _routers = []  # all registered routers on the system
    _power_strips = []  # all registered power strips on the system
    _test_results = []  # all test reports in form (router.id, str(test), TestResult)
    _stopped = False  # marks if the server is still running

    _max_subprocesses = 0  # will be set at start. describes how many Processes are needed in the Pool

    # test/task handling
    _running_task = []  # List[Union[RemoteSystemJobClass, RemoteSystemJob]]
    _waiting_tasks = []  # List[deque[Union[RemoteSystemJobClass, RemoteSystemJob]]]
    _task_pool = None  # multiprocessing.pool.Pool for task execution
    _job_wait_executor = None  # ThreadPoolExecutor for I/O handling on tasks
    _semaphore_task_management = Semaphore(1)
    _test_sets = {}  # Dict[List[str]]

    # NVAssistent
    _nv_assistent = None

    _pid = None  # PID of the server

    _server_stop_event = None

    @classmethod
    def start(cls, config_path: str = CONFIG_PATH) -> None:
        """
        Starts the runtime server with all components

        :param config_path: Path to an alternative config directory
        """

        # server has to be run with root rights - except on travis CI
        if not os.geteuid() == 0 and not os.environ.get('TRAVIS'):
            sys.exit('Script must be run as root')

        cls.CONFIG_PATH = config_path
        # set the config_path at the manager
        ConfigManager.set_config_path(config_path)

        # read from config the Vlan mode
        vlan_activate = ConfigManager.get_server_property("Vlan_On")
        cls.VLAN = vlan_activate

        # read from config if debug mode is on
        log_level = int(ConfigManager.get_server_property("Log_Level"))
        debug_mode = False
        if log_level is 10:
            debug_mode = True
        cls.DEBUG = debug_mode

        setproctitle("fftserver")

        cls._server_stop_event = Event()

        cls._pid = os.getpid()

        # create instance and give params to the logger object
        LoggerSetup.setup(log_level)

        # load Router configs
        cls.__load_configuration()

        for router in cls.get_routers():
            cls._running_task.append(None)
            cls._waiting_tasks.append(deque())

        # start thread for multiprocess stop wait
        t = threading.Thread(target=cls._close_wait)
        t.start()

        # start process/thread pool for job and test handling
        cls._max_subprocesses = (len(cls._routers) + 1)  # plus one for the power strip
        cls._task_pool = Pool(processes=cls._max_subprocesses, initializer=init_process,
                              initargs=(cls._server_stop_event,), maxtasksperchild=1)
        cls._job_wait_executor = ThreadPoolExecutor(max_workers=(cls._max_subprocesses * 2))

        # add Namespace and Vlan for each Router
        if cls.VLAN:
            cls._nv_assistent = NVAssistent("eth0")

            for router in cls.get_routers():
                logging.debug("Add Namespace and Vlan for Router(" + str(router.id) + ")")
                cls._nv_assistent.create_namespace_vlan(router)

            # add Namespace and Vlan for 1 Powerstrip (expand to more if necessary)
            logging.debug("Add Namespace and Vlan for Powerstrip")
            cls._nv_assistent.create_namespace_vlan(cls.get_power_strip())

            # update Router
            cls.router_online(None, update_all=True, blocked=True)
            cls.update_router_info(None, update_all=True)

        logging.info("Runtime Server started")

        try:
            cls._ipc_server.start_ipc_server(cls, True)  # serves forever - works like a while(true)
        except (KeyboardInterrupt, SystemExit):
            logging.info("Received an interrupt signal")
            cls.stop()

        # at this point following code will be ignored

    @classmethod
    def __load_configuration(cls):
        logging.debug("Load configuration")
        cls._routers = ConfigManager.get_routers_list()
        for i, r in enumerate(cls._routers):
            if len(ConfigManager.get_web_interface_list()) >= i:
                if 'node_name' in ConfigManager.get_web_interface_list()[i]:
                    r.set_node_name(ConfigManager.get_web_interface_list()[i]['node_name'])
        cls._power_strips = ConfigManager.get_power_strip_list()
        cls._test_sets = ConfigManager.get_test_sets()

    @classmethod
    def stop(cls) -> None:
        """
        Stops the server, all running tests and closes all connections.
        """
        cls._server_stop_event.set()

    @classmethod
    def _close_wait(cls) -> None:
        assert(cls._pid == os.getpid())

        cls._server_stop_event.wait()

        if not cls._stopped:
            print("Shutdown server")
            cls._stopped = True
            cls._task_pool.close()
            cls._task_pool.terminate()
            cls._task_pool.join()
            cls._job_wait_executor.shutdown(wait=False)
            if cls.VLAN:
                cls._nv_assistent.close()

            cls._ipc_server.shutdown()

            # close open streams and the logger instance
            LoggerSetup.shutdown()
            sys.exit(0)

    @classmethod
    def stop_all_tasks(cls) -> None:
        """
        Stops all running jobs on the RemoteSystems
        """
        cls._task_pool.terminate()
        cls._task_pool = Pool(processes=cls._max_subprocesses, maxtasksperchild=1)

        logging.info("Stopped all jobs")

    @classmethod
    def get_test_by_name(cls, test_name: str) -> FirmwareTestClass:
        # TODO test verwaltung #36
        raise NotImplementedError

    @classmethod
    def get_running_task(cls, remote_system: RemoteSystem) -> Optional[Union[RemoteSystemJob, RemoteSystemJobClass]]:
        """
        Returns which task is running on the given RemoteSystem

        :param remote_system: the RemoteSystem
        :return: if no job is running, it returns None
        """
        return cls._running_task[remote_system.id]

    @classmethod
    def set_running_task(cls, remote_system: RemoteSystem, task: Union[RemoteSystemJob, RemoteSystemJobClass]) -> None:
        """
        Sets internally which RemoteSystem executes which Task.
        It doesn't run or starts the job on the RemoteSystem!

        :param remote_system: the RemoteSystem
        :param task: the Task
        """
        cls._running_task[remote_system.id] = task

    @classmethod
    def get_waiting_task_queue(cls, remote_system: RemoteSystem) -> Iterable[Union[RemoteSystemJobClass,
                                                                                   RemoteSystemJob]]:
        """
        Returns the waiting task queue

        :param remote_system: the associated RemoteSystem of the queue
        :return: Returns the queue as a collections.deque, filled with RemoteSystemJobClass and RemoteSystemJob
        """
        result = cls._waiting_tasks[remote_system.id]
        return result

    @classmethod
    def set_waiting_task(cls, remote_system: RemoteSystem, task: Union[RemoteSystemJob, RemoteSystemJobClass]) -> None:
        """
        Add a task to the waiting Queue of a specific RemoteSystem

        :param remote_system: the associated RemoteSystem of the queue
        :param task: task which has to wait
        """
        queue = cls.get_waiting_task_queue(remote_system)
        queue.appendleft(task)
        logging.debug("%sAdded " + str(task) + " to queue of " + str(remote_system) + ". Queue length: " + str(len(queue)),
                      LoggerSetup.get_log_deep(3))

    @classmethod
    def start_job(cls, remote_sys: RemoteSystem, remote_job: RemoteSystemJob, wait: int= -1) -> bool:
        """
        Starts an specific job on a RemoteSystem.
        The job will be executed asynchronous this means the method is not blocking.
        It add only the job to the task queue from RemoteSystem.
        If you want, that this method wait until the job is executed, you have to set the wait param.
        Think about that your job has maybe to wait in the queue.

        :param remote_sys: The RemoteSystem on which the job will run. If none then the job will be executed on all
        routers
        :param remote_job: The name of the test to execute
        :param wait: -1 for async execution and positive integer for wait in seconds
        :return: True if job was successful added in the queue
        """
        assert isinstance(remote_job, RemoteSystemJob)
        if remote_sys is None:
            result = True
            for router in cls.get_routers():
                done_event = DoneEvent()
                result = result and cls.__start_task(router, remote_job, done_event)
                if wait != -1:
                    done_event.wait(wait)
            return result
        else:
            done_event = DoneEvent()
            result = cls.__start_task(remote_sys, remote_job, done_event)
            if wait != -1:
                done_event.wait(wait)
            return result

    @classmethod
    def start_test_set(cls, router_id: int, test_set_name: str, wait: int= -1) -> bool:
        """
        Start an specific test on a router

        :param router_id: The id of the router on which the test will run.
        If id is -1 the test will be executed on all routers.
        :param test_set_name: The name of the test set to execute
        :param wait: -1 for async execution and positive integer for wait in seconds
        :return: True if test was successful added in the queue
        """

        for file_name in cls._test_sets[test_set_name]:
            module = importlib.import_module("firmware_tests." + file_name)
            import inspect

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, FirmwareTest) and name != "FirmwareTest":
                    if router_id == -1:  # all routers
                        for router in cls._routers:
                            done_event = DoneEvent()
                            cls.__start_task(router, obj, done_event)
                            if wait != -1:
                                done_event.wait(wait)
                    else:
                        done_event = DoneEvent()
                        cls.__start_task(cls.get_router_by_id(router_id), obj, done_event)
                        if wait != -1:
                            done_event.wait(wait)
        return True

    @classmethod
    def __start_task(cls, remote_sys: RemoteSystem, job: Union[RemoteSystemJobClass, RemoteSystemJob],
                     done_event: DoneEvent = DoneEvent()) -> bool:
        """
        Apply a job or a test to the ProcessPool, execute it in the right network namespace with
        the matching VLAN from RemoteSystem and insert a method for result/post process handling.
        This method is thread-safe but not multi process safe.

        :param remote_sys: the RemoteSystem
        :param job: the Job
        :return: true if job directly started, false if not
        """
        assert(cls._pid == os.getpid())
        # Check if it is the the same PID as the PID Process which started the ProcessPool
        try:
            cls._semaphore_task_management.acquire(blocking=True)  # No concurrent task handling
            if job is None:  # no job given? look up for the next job in the queue
                logging.debug("%sLookup for next task in the queue %i", LoggerSetup.get_log_deep(1), remote_sys.id)
                if not len(cls.get_waiting_task_queue(remote_sys)):
                    logging.debug("%sNo tasks in the queue %i to run.", LoggerSetup.get_log_deep(2), remote_sys.id)
                    return False
                else:
                    if cls.get_running_task(remote_sys) is not None:
                        logging.debug("%sRouter working. Next task has to wait..", LoggerSetup.get_log_deep(3))
                        return False
                    else:
                        logging.debug("%sGet next task from the queue", LoggerSetup.get_log_deep(3))
                        job = cls.get_waiting_task_queue(remote_sys).pop()

            if cls.get_running_task(remote_sys) is None:
                logging.debug("%sStarting task " + str(job), LoggerSetup.get_log_deep(1))
                cls.set_running_task(remote_sys, job)
                if isinstance(job, FirmwareTestClass):
                    # task is a test
                    cls._job_wait_executor.submit(cls._wait_for_test_done, job, remote_sys, done_event)
                else:
                    # task is a regular job
                    cls._job_wait_executor.submit(cls._wait_for_job_done, job, remote_sys, done_event)
                return True
            else:
                logging.debug("%sPut task in the wait queue. " + str(job), LoggerSetup.get_log_deep(1))
                cls.set_waiting_task(remote_sys, job)

                return False
        except KeyboardInterrupt:
            cls.stop()
        except Exception as e:
            logging.error("%s start_task: " + str(e), LoggerSetup.get_log_deep(2))
        finally:
            cls._semaphore_task_management.release()
            # logging.debug(str(cls._waiting_tasks), 3)
            # logging.debug(str(cls._running_task), 3)

    @classmethod
    def _execute_job(cls, job: RemoteSystemJob, remote_sys: RemoteSystem, routers: List[Router]) -> {}:
        logging.debug("%sExecute job " + str(job) + " on Router(" + str(remote_sys.id) + ")",
                      LoggerSetup.get_log_deep(2))
        setproctitle(str(remote_sys.id) + " - " + str(job))
        job.prepare(remote_sys, routers)

        cls.__setns(remote_sys)
        try:
            result = job.run()
        except Exception:
            logging.debug("Error while execute job " + str(job))

        return result

    @classmethod
    def _execute_test(cls, test: FirmwareTestClass, router: Router, routers: List[Router]) -> TestResult:
        if not isinstance(router, Router):
            raise ValueError("Chosen Router is not a real Router...")
        # proofed: this method runs in other process as the server
        setproctitle(str(router.id) + " - " + str(test))
        logging.debug("%sExecute test " + str(test) + " on " + str(router), LoggerSetup.get_log_deep(2))

        test_suite = defaultTestLoader.loadTestsFromTestCase(test)

        # prepare all test cases
        for test_case in test_suite:
            logging.debug("%sTestCase " + str(test_case), LoggerSetup.get_log_deep(4))
            test_case.prepare(router, routers)

        result = TestResult()

        cls.__setns(router)
        try:

            result = test_suite.run(result)  # TODO if debug set, run as debug()
        except Exception as e:
            logging.error("%sTestCase raised an exception", LoggerSetup.get_log_deep(3))
            logging.error("%s" + str(e), LoggerSetup.get_log_deep(3))
        finally:

            # I'm sry for this dirty hack, but if you don't do this you get an
            # "TypeError: cannot serialize '_io.TextIOWrapper' object" because sys.stdout is not serializeable...
            result._original_stdout = None
            result._original_stderr = None

            logging.debug("%sResult from test " + str(result), LoggerSetup.get_log_deep(3))
            return result

    @classmethod
    def _wait_for_test_done(cls, test: FirmwareTestClass, router: Router, done_event: DoneEvent) -> None:
        """
        Wait 5 minutes until the test is done.
        Handles the result from the tests.
        Triggers the next job/test.

        :param test: test to execute
        :param router: the Router
        """
        logging.debug("%sWait for test" + str(test), LoggerSetup.get_log_deep(2))
        try:
            async_result = cls._task_pool.apply_async(func=cls._execute_test, args=(test, router, cls._routers))
            result = async_result.get(300)  # wait 5 minutes or raise an TimeoutError
            logging.debug("%sTest done " + str(test), LoggerSetup.get_log_deep(1))
            logging.debug("%sFrom " + str(router), LoggerSetup.get_log_deep(2))

            cls._test_results.append((router.id, str(test), result))
        except Exception as e:
            # TODO #105
            logging.error("%sTest raised an Exception: " + str(e), LoggerSetup.get_log_deep(1))

            result = TestResult()
            result._original_stdout = None
            result._original_stderr = None
            # result.addError(None, (type(exception), exception, None))
            # TODO exception handling for failed Tests

            cls._test_results.append((router.id, str(test), result))

        finally:
            cls.set_running_task(router, None)
            # logging.debug(str(cls._test_results))
            # start next test in the queue
            done_event.set()
            cls.__start_task(router, None)

    @classmethod
    def _wait_for_job_done(cls, job: RemoteSystemJob, remote_sys: RemoteSystem, done_event: DoneEvent) -> None:
        """
        Wait 5 minutes until the job is done.
        Handles the result from the job with the job.prepare(data) method.
        Triggers the next job/test.

        :param job: job to execute
        :param remote_sys: the RemoteSystem
        """
        async_result = cls._task_pool.apply_async(func=cls._execute_job, args=(job, remote_sys, cls._routers))
        result = async_result.get(300)  # wait 5 minutes or raise an TimeoutError
        logging.debug("%sJob done " + str(job), LoggerSetup.get_log_deep(1))
        logging.debug("%sAt Router(" + str(remote_sys.id) + ")", LoggerSetup.get_log_deep(2))
        try:
            exception = None  # task.exception() # TODO #105
            if exception is not None:
                logging.error("%sTask raised an exception: " + str(exception), LoggerSetup.get_log_deep(1))
            else:
                job.post_process(result, cls)

        finally:
            cls.set_running_task(remote_sys, None)
            # start next test in the queue
            done_event.set()
            cls.__start_task(remote_sys, None)

    @classmethod
    def __setns(cls, remote_sys: RemoteSystem) -> None:
        """
        Set Namespace and VLAN for the current process.

        :param remote_sys: The RemoteSystem which you want to connect over VLAN
        """
        if cls.VLAN:
            logging.debug("%sSet Namespace and VLAN for the current process(" + str(os.getpid()) + ")",
                          LoggerSetup.get_log_deep(2))
            netns.setns(remote_sys.namespace_name)

    @classmethod
    def __unsetns(cls, remote_sys: RemoteSystem) -> None:
        """
        Deactivates VLAN after you activate it with cls.__setns

        :param remote_sys: The RemoteSystem
        """
        if cls.VLAN:
            logging.debug("%sRemove Namespace and VLAN for the current process(" + str(os.getpid()) + ")",
                          LoggerSetup.get_log_deep(2))
            cls._nv_assistent.delete_namespace(remote_sys.namespace_name)

    @classmethod
    def get_routers(cls) -> List[Router]:
        """
        List of known routers

        :return: List is a copy of the original list.
        """

        return cls._routers.copy()

    @classmethod
    def get_power_strip(cls) -> PowerStrip:
        """
        Power strip as object, for now only 1

        :return: Copy of the original object
        """
        for ps in cls._power_strips:
            assert isinstance(ps, PowerStrip)
        return cls._power_strips[0]

    @classmethod
    def get_routers_task_queue_size(cls, router_id: int) -> int:
        """
        Returns the size of the task queue including the actual running task

        :param router_id: ID of the router
        :return: queue length
        """
        remote_sys = cls.get_router_by_id(router_id)
        result = 0
        if cls.get_running_task(remote_sys) is not None:
            result = 1

        task_queue = cls.get_waiting_task_queue(remote_sys)
        return len(task_queue) + result

    @classmethod
    def get_running_tests(cls) -> List[FirmwareTestClass]:
        """
        List of running test on the test server.

        :return: List as a copy of the original list.
        """
        # FIXME
        raise NotImplementedError
        return cls._running_tasks.copy()

    @classmethod
    def get_test_results(cls, router_id: int = -1) -> [(int, str, TestResult)]:
        """
        Returns the firmware test results for the router

        :param router_id: the specific router or all router if id = -1
        :return: List of results
        """

        if router_id == -1:
            return cls._test_results
        else:
            results = []
            for result in cls._test_results:
                if result[0] == router_id:
                    results.append(result)
            return results

    @classmethod
    def delete_test_results(cls) -> int:
        """
        Remove all test results

        :return: Number of deleted results
        """
        size_results = len(cls._test_results)
        cls._test_results = []
        return size_results

    @classmethod
    def get_tests(cls) -> List[FirmwareTestClass]:
        """
        :return: List of available tests on the server
        """
        # TODO get available test from config
        raise NotImplementedError

    @classmethod
    def get_firmwares(cls) -> []:
        """
        :return: List of known firmwares
        """
        # TODO vllt vom config?
        raise NotImplementedError

    @classmethod
    def get_router_by_id(cls, router_id: int) -> Router:
        """
        Returns a Router with the given id.

        :param router_id:
        :return: Router
        """
        routers = cls.get_routers()
        for router in routers:
            if router.id == router_id:
                logging.debug("%sget_router_by_id: " + str(router.id), LoggerSetup.get_log_deep(4))
                return router
        return None

    @classmethod
    def router_online(cls, router_ids: Union[List[int], None], update_all: bool, blocked: bool = False) -> None:
        """
        Tries to connect to the `Router` and updates the Mode of the Router.

        :param router_ids: List of unique numbers to identify a :py:class:`Router`
        :param update_all: Is True if all Routers should be updated
        :param blocked: blocks until it finished
        """

        if blocked:
            wait = 300
        else:
            wait = -1

        if update_all:
            for router in cls.get_routers():
                cls.start_job(router, RouterOnlineJob(), wait)
        else:
            for router_id in router_ids:
                router = cls.get_router_by_id(router_id)
                cls.start_job(router, RouterOnlineJob(), wait)

    @classmethod
    def update_router_info(cls, router_ids: Union[List[int], None], update_all: bool) -> None:
        """
        Updates all the information about the :py:class:`Router`

        :param router_ids: List of unique numbers to identify a :py:class:`Router`
        :param update_all: Is True if all Routers should be updated
        """
        if cls.VLAN:
            if update_all:
                for router in cls.get_routers():
                    cls.start_job(router, RouterInfoJob())
            else:
                for router_id in router_ids:
                    router = cls.get_router_by_id(router_id)
                    cls.start_job(router, RouterInfoJob())
        else:
            logging.info("set VLAN to true to activate 'update_router_info' it")

    @classmethod
    def sysupdate_firmware(cls, router_ids: Union[List[int], None], update_all: bool) -> None:
        """
        Downloads and copies the firmware to the :py:class:`Router` given in
        the List(by a unique id) resp. to all Routers

        :param router_ids: List of unique numbers to identify a :py:class:`Router`
        :param update_all: Is True if all Routers should be updated
        """

        if update_all:
            for router in cls.get_routers():
                sysupdate = Sysupdate(router)
                sysupdate.start()
                sysupdate.join()
        else:
            for router_id in router_ids:
                router = cls.get_router_by_id(router_id)
                sysupdate = Sysupdate(router)
                sysupdate.start()
                sysupdate.join()

    @classmethod
    def sysupgrade_firmware(cls, router_ids: Union[List[int], None], upgrade_all: bool, n: bool) -> None:
        """
        Upgrades the firmware on the given :py:class:`Router` s

        :param router_ids: List of unique numbers to identify a Router
        :param upgrade_all: If all is True all Routers were upgraded
        :param n: If n is True the upgrade discard the last firmware
        """

        if upgrade_all:
            for router in cls.get_routers():
                # The IP where the Router can download the firmware image (should be the frameworks IP)
                web_server_ip = cls._nv_assistent.get_ip_address(router.namespace_name, router.vlan_iface_name)[0]
                cls.start_job(router, SysupgradeJob(n, web_server_ip, debug=False))
        else:
            for router_id in router_ids:
                router = cls.get_router_by_id(router_id)
                # The IP where the Router can download the firmware image (should be the frameworks IP)
                web_server_ip = cls._nv_assistent.get_ip_address(router.namespace_name, router.vlan_iface_name)[0]
                cls.start_job(router, SysupgradeJob(n, web_server_ip, debug=False))

    @classmethod
    def setup_web_configuration(cls, router_ids: Union[List[int], None], setup_all: bool, wizard: bool):
        """
        After a systemupgrade, the Router starts in config-mode without the possibility to connect again via SSH.
        Therefore this class uses selenium to parse the given webpage. All options given by the web interface of the
        Router can be set via the 'web_interface_config.yaml', except for the sysupgrade which isn't implemented yet

        :param router_ids: List of unique numbers to identify a Router
        :param setup_all: If True all Routers will be setuped via the webinterface
        :param wizard
        """

        if setup_all:
            for i, router in enumerate(cls.get_routers()):
                cls.start_job(router, RouterWebConfigurationJob(ConfigManager.get_web_interface_list()[i], wizard))
        else:
            for i, router_id in enumerate(router_ids):
                router = cls.get_router_by_id(router_id)
                cls.start_job(router, RouterWebConfigurationJob(ConfigManager.get_web_interface_list()[i], wizard))

    @classmethod
    def reboot_router(cls, router_ids: Union[List[int], None], reboot_all: bool, configmode: bool):
        """
        Reboots the given Routers.

        :param router_ids: List of unique numbers to identify a Router
        :param reboot_all: Reboots all Routers
        :param configmode: Reboots Router into configmode
        """

        if reboot_all:
            for router in cls.get_routers():
                cls.start_job(router, RouterRebootJob(configmode))
        else:
            for router_id in router_ids:
                router = cls.get_router_by_id(router_id)
                cls.start_job(router, RouterRebootJob(configmode))

    @classmethod
    def register_key(cls, router_ids: List[int], register_all: bool):
        """
        Sends the public-key of the given Routers to an email that is specified in the config-file.

        :param router_ids: List of unique numbers to identify a Router
        :param register_all: Register the public-keys of all Routers
        """

        if register_all:
            for router in cls.get_routers():
                reg_pub_key = RegisterPublicKey(router, ConfigManager.get_server_dict()[1])
                reg_pub_key.start()
                reg_pub_key.join()
        else:
            for router_id in router_ids:
                router = cls.get_router_by_id(router_id)
                reg_pub_key = RegisterPublicKey(router, ConfigManager.get_server_dict()[1])
                reg_pub_key.start()
                reg_pub_key.join()

    @classmethod
    def control_switch(cls, router_ids: List[int], switch_all: bool, on_or_off: bool):
        """
        Switches the power for different routers on or off

        :param router_ids: List of router IDs
        :param switch_all: apply to all routers
        :param on_or_off: true for on, false for off
        """
        from power_strip.power_strip_control import PowerStripControlJob

        # for now only 1 power strip, change in router if more are added
        power_strip = cls.get_power_strip()

        if switch_all:
            for router in cls.get_routers():
                port_id = router.power_socket
                cls.start_job(power_strip, PowerStripControlJob(on_or_off, port_id))
        else:
            for router_id in router_ids:
                port_id = cls.get_router_by_id(router_id).power_socket
                cls.start_job(power_strip, PowerStripControlJob(on_or_off, port_id))

    @classmethod
    def get_server_version(cls) -> str:
        """
        Returns the server version as a string
        """
        return cls.VERSION

    def register_tty(self, tty_name: str = '') -> bool:
        """
        Register tty from cli in logging
        :param tty_name: Name of the console
        :return bool: Success of the register
        """
        # register console from cli in the current process and logging instance
        return LoggerSetup.add_handler(tty_name)
