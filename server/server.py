from .serverproxy import ServerProxy
from .ipc import IPC
from .test import FirmwareTest
from typing import List, Union, Iterable, Optional
from router.router import Router
from config.configmanager import ConfigManager
from multiprocessing.pool import Pool
from log.logger import Logger
from concurrent.futures import ThreadPoolExecutor
from unittest.result import TestResult
from threading import Event, Semaphore
from network.remote_system import RemoteSystem, RemoteSystemJob
from unittest import defaultTestLoader
from pyroute2 import netns
from collections import deque
import os
import sys

# type alias
FirmwareTestClass = type(FirmwareTest)
RemoteSystemJobClass = type(RemoteSystemJob)


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
    _reports = []  # all test reports
    _stopped = False  # marks if the server is still running

    _max_subprocesses = 0  # will be set at start. describes how many Processes are needed in the Pool

    # test/task handling
    _running_task = []  # List[Union[RemoteSystemJobClass, RemoteSystemJob]]
    _waiting_tasks = []  # List[deque[Union[RemoteSystemJobClass, RemoteSystemJob]]]
    _task_pool = None  # multiprocessing.pool.Pool for task execution
    _job_wait_executor = None  # ThreadPoolExecutor for I/O handling on tasks
    _semaphore_task_management = Semaphore(1)

    # NVAssistent
    _nv_assistent = None

    _pid = None  # PID of the server

    @classmethod
    def start(cls, config_path: str = CONFIG_PATH) -> None:
        """
        Starts the runtime server with all components

        :param config_path: Path to an alternative config directory
        """

        # server has to be run with root rights - except on travi CI
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

        cls._pid = os.getpid()

        # create instance and give params to the logger object
        Logger().setup(log_level, log_level, log_level)

        # load Router configs
        cls.__load_configuration()

        for router in cls.get_routers():
            cls._running_task.append(None)
            cls._waiting_tasks.append(deque())

        # start process/thread pool for job and test handling
        cls._max_subprocesses = (len(cls._routers)+2)
        cls._task_pool = Pool(processes=cls._max_subprocesses, maxtasksperchild=1)
        cls._job_wait_executor = ThreadPoolExecutor(max_workers=(cls._max_subprocesses + 5))

        # add Namespace and Vlan for each Router
        if cls.VLAN:
            # TODO wrong place #70
            from network.nv_assist import NVAssistent
            cls._nv_assistent = NVAssistent("eth0")

            for router in cls.get_routers():
                Logger().debug("Add Namespace and Vlan for Router(" + str(router.id) + ")")
                cls._nv_assistent.create_namespace_vlan(router)

            # update Router
            cls.router_online(None, all=True)
            # TODO Hat error verursacht
            #cls.update_router_info(None, update_all=True)

        Logger().info("Runtime Server started")

        try:
            cls._ipc_server.start_ipc_server(cls, True)  # serves forever - works like a while(true)
        except (KeyboardInterrupt, SystemExit):
            Logger().info("Received an interrupt signal")
            cls.stop()

        # at this point following code will be ignored

    @classmethod
    def __load_configuration(cls):
        Logger().debug("Load configuration")
        cls._routers = ConfigManager.get_router_manual_list()

    @classmethod
    def stop(cls) -> None:
        """
        Stops the server, all running tests and closes all connections.
        """
        if not cls._stopped:
            cls._stopped = True
            cls._task_pool.close()
            if cls.VLAN:
                cls._nv_assistent.close()
            # close open streams and the logger instance
            Logger().close()

            cls._ipc_server.shutdown()

    @classmethod
    def stop_all_tasks(cls) -> None:
        """
        Stops all running jobs on the RemoteSystems
        """
        cls._task_pool.terminate()
        cls._task_pool = Pool(processes=cls._max_subprocesses, maxtasksperchild=1)

        Logger().info("Stopped all jobs")

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
    def get_waiting_task_queue(cls, remote_system: RemoteSystem) -> Iterable[Union[RemoteSystemJobClass, RemoteSystemJob]]:
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
        Logger().debug("Added " + str(task) + " to queue of " + remote_system + ". Queue length: " + len(queue), 3)

    @classmethod
    def start_job(cls, remote_sys: RemoteSystem, remote_job: RemoteSystemJob, wait: int= -1) -> bool:
        """
        Starts an specific job on a RemoteSystem.
        The job will be executed asynchronous this means the method is not blocking.
        It add only the job to the task queue from RemoteSystem.
        If you want, that this method wait until the job is executed, you have to set the wait param.
        Think about that your job has maybe to wait in the queue.

        :param remote_sys: The RemoteSystem on which the job will run. If none then the job will be executed on all routers
        :param remote_job: The name of the test to execute
        :param wait: -1 for async execution and positive integer for wait in seconds
        :return: True if job was successful added in the queue
        """
        assert isinstance(remote_job, RemoteSystemJob)

        if wait != -1:
            raise NotImplementedError  # TODO #102
            done_event = Event()
            remote_job.set_done_event(done_event)
            # TODO all routers if remote_sys == None
            result = cls.__start_task(remote_sys, remote_job)
            done_event.wait(wait)
            return result
        else:
            if remote_sys is None:
                result = True
                for router in cls.get_routers():
                    result = result and cls.__start_task(router, remote_job)
                return result
            else:
                return cls.__start_task(remote_sys, remote_job)

    @classmethod
    def start_test(cls, router_id: int, test_name: str) -> bool:
        """
        Start an specific test on a router

        :param router_id: The id of the router on which the test will run
        :param test_name: The name of the test to execute
        :return: True if test was successful added in the queue
        """
        router = cls.get_router_by_id(router_id)
        if router is None:
            Logger().error("Router ID unknown")
            return False

        # TODO Testverwaltung - ermittlung des passenden Tests #36
        # cls.get_test_by_name
        from firmware_tests.connection_test import ConnectionTest, VeryLongTest
        if test_name == "ConnectionTest":
            demo_test = ConnectionTest  # Important: Param is a class and not an object
        elif test_name == "VeryLongTest":
            demo_test = VeryLongTest
        else:
            Logger().error("Testname unknown")
            return False

        return cls.__start_task(router, demo_test)

    @classmethod
    def __start_task(cls, remote_sys: RemoteSystem, job: Union[RemoteSystemJobClass, RemoteSystemJob]) -> bool:
        """
        Apply a job or a test to the ProcessPool, execute it in the right network namespace with
        the matching VLAN from RemoteSystem and insert a method for result/post process handling.
        This method is thread-safe but not multi process safe.

        :param remote_sys: the RemoteSystem
        :param job: the Job
        :return: true if job directly started, false if
        """
        assert(cls._pid == os.getpid())
        # Check if it is the the same PID as the PID Process which started the ProcessPool

        cls._semaphore_task_management.acquire(blocking=True)  # No concurrent task handling
        try:
            if job is None:  # no job given? look up for the next job in the queue
                Logger().debug("Lookup for next task", 1)
                if not len(cls.get_waiting_task_queue(remote_sys)):
                    Logger().debug("No tasks in the queue to run.", 2)
                    return False
                else:
                    if cls.get_running_task(remote_sys) is not None:
                        Logger().debug("Router working. Next task has to wait..", 3)
                        return False
                    else:
                        Logger().debug("Get next task from the queue", 3)
                        job = cls.get_waiting_task_queue(remote_sys).pop()

            if cls.get_running_task(remote_sys) is None:
                Logger().debug("Starting task " + str(job), 1)
                cls.set_running_task(remote_sys, job)
                if isinstance(job, FirmwareTestClass):
                    # task is a test
                    cls._job_wait_executor.submit(cls._wait_for_test_done, job, remote_sys)
                else:
                    # task is a regular job
                    data = job.pre_process(cls)
                    async_result = cls._task_pool.apply_async(func=cls._execute_job,
                                                              args=(job, remote_sys, data,))

                    cls._job_wait_executor.submit(cls._wait_for_job_done, job, remote_sys, async_result)
                return True
            else:
                Logger().debug("Put task in the wait queue. " + str(job), 1)
                cls.set_waiting_task(remote_sys, job)

                return False

        except Exception as e:
            Logger().error(str(e), 2)

        finally:
            cls._semaphore_task_management.release()
            # Logger().debug(str(cls._waiting_tasks), 3)
            # Logger().debug(str(cls._running_task), 3)

    @classmethod
    def _execute_job(cls, job: RemoteSystemJob, remote_sys: RemoteSystem, data: {}) -> {}:
        Logger().debug("Execute job " + str(job) + " on Router(" + str(remote_sys.id) + ")", 2)
        job.prepare(remote_sys, data)

        cls.__setns(remote_sys)
        try:
            job.run()
        except Exception:
            Logger().debug("Error while execute job " + str(job))
        result = job.get_return_data()

        return result

    @classmethod
    def _execute_test(cls, test: FirmwareTestClass, router: Router) -> TestResult:
        if not isinstance(router, Router):
            raise ValueError("Chosen Router is not a real Router...")
        # proofed: this method runs in other process as the server
        Logger().debug("Execute test " + str(test) + " on " + str(router), 2)

        test_suite = defaultTestLoader.loadTestsFromTestCase(test)

        # prepare all test cases
        for test_case in test_suite:
            Logger().debug("TestCase " + str(test_case), 4)
            test_case.prepare(router)

        result = TestResult()

        cls.__setns(router)
        try:

            result = test_suite.run(result)  # TODO if debug set, run as debug()
        except Exception as e:
            Logger().error("TestCase raised an exception", 3)
            Logger().error(str(e), 3)
        finally:

            # I'm sry for this dirty hack, but if you don't do this you get an
            # "TypeError: cannot serialize '_io.TextIOWrapper' object" because sys.stdout is not serializeable...
            result._original_stdout = None
            result._original_stderr = None

            Logger().debug("Result from test " + str(result), 3)
            return result

    @classmethod
    def _wait_for_test_done(cls, test: FirmwareTestClass, router: Router) -> None:
        """
        Wait 5 minutes until the test is done.
        Handles the result from the tests.
        Triggers the next job/test.

        :param test: test to execute
        :param router: the Router
        """
        Logger().debug("Wait for test" + str(test), 2)
        try:
            async_result = cls._task_pool.apply_async(func=cls._execute_test, args=(test, router))
            result = async_result.get(300)  # wait 5 minutes or raise an TimeoutError
            Logger().debug("Test done " + str(test), 1)
            Logger().debug("From " + str(router), 2)

            cls._reports.append(result)
        except Exception as e:
            # TODO #105
            Logger().error("Test raised an Exception: " + str(e), 1)

            result = TestResult()
            result._original_stdout = None
            result._original_stderr = None
            # result.addError(None, (type(exception), exception, None))
            # TODO exception handling for failed Tests

            cls._reports.append(result)

        finally:
            cls.set_running_task(router, None)
            # Logger().debug(str(cls._reports))
            # start next test in the queue
            cls.__start_task(router, None)

    @classmethod
    def _wait_for_job_done(cls, job: RemoteSystemJob, remote_sys: RemoteSystem, async_result) -> None:
        """
        Callback function for tests.
        Needed to start the next test/task in the queue.
        Calls the post process of the Remote

        :param job: the Future which runs the test
        """
        result = async_result.get(timeout=60*5)
        Logger().debug("Job done " + str(job), 1)
        Logger().debug("At Router(" + str(remote_sys.id) + ")", 2)
        try:
            exception = None  # task.exception() # TODO #105
            if exception is not None:
                Logger().error("Task raised an exception: " + str(exception), 1)
            else:
                job.post_process(result, cls)
                job.done()

        finally:
            cls.set_running_task(remote_sys, None)
            # start next test in the queue
            cls.__start_task(remote_sys, None)

    @classmethod
    def __setns(cls, remote_sys: RemoteSystem) -> None:
        """
        Set Namespace and VLAN for the current process.

        :param remote_sys: The RemoteSystem which you want to connect over VLAN
        """
        if cls.VLAN:
            Logger().debug("Set Namespace and VLAN for the current process(" + str(os.getpid()) + ")", 2)
            netns.setns(remote_sys.namespace_name)

    @classmethod
    def __unsetns(cls, remote_sys: RemoteSystem) -> None:
        """
        Deactivates VLAN after you activate it with cls.__setns

        :param remote_sys: The RemoteSystem
        """
        if cls.VLAN:
            Logger().debug("Remove Namespace and VLAN for the current process(" + str(os.getpid()) + ")", 2)
            cls._nv_assistent.delete_namespace(remote_sys.namespace_name)

    @classmethod
    def get_routers(cls) -> List[Router]:
        """
        List of known routers

        :return: List is a copy of the original list.
        """

        # check if list is still valid
        for router in cls._routers:
            assert isinstance(router, Router)

        return cls._routers.copy()

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
    def get_reports(cls) -> []:
        """
        Returns the test results.

        :return: List of reports
        """
        return cls._reports

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
                Logger().debug("get_router_by_id: " + str(router.id), 4)
                return router
        return None

    @classmethod
    def router_online(cls, router_ids: List[int], all: bool) -> None:
        """
        Tries to connect to the `Router` and updates the Mode of the Router.

        :param router_ids: List of unique numbers to identify a :py:class:`Router`
        :param update_all: Is True if all Routers should be updated
        """
        from util.router_online import RouterOnlineJob  # TODO remove it from here #64
        if all:
            for router in cls.get_routers():
                cls.start_job(router, RouterOnlineJob())
        else:
            for router_id in router_ids:
                router = cls.get_router_by_id(router_id)
                cls.start_job(router, RouterOnlineJob())

    @classmethod
    def update_router_info(cls, router_ids: List[int], update_all: bool) -> None:
        """
        Updates all the information about the :py:class:`Router`

        :param router_ids: List of unique numbers to identify a :py:class:`Router`
        :param update_all: Is True if all Routers should be updated
        """
        if cls.VLAN:
            from util.router_info import RouterInfoJob  # TODO remove it from here #64

            if update_all:
                for router in cls.get_routers():
                    cls.start_job(router, RouterInfoJob())
            else:
                for router_id in router_ids:
                    router = cls.get_router_by_id(router_id)
                    cls.start_job(router, RouterInfoJob())
        else:
            Logger().info("set VLAN to true to activate 'update_router_info' it")

    @classmethod
    def sysupdate_firmware(cls, router_ids: List[int], update_all: bool) -> None:
        """
        Downloads and copies the firmware to the :py:class:`Router` given in
        the List(by a unique id) resp. to all Routers

        :param router_ids: List of unique numbers to identify a :py:class:`Router`
        :param update_all: Is True if all Routers should be updated
        """
        from util.router_flash_firmware import Sysupdate
        if update_all:
            for router in cls.get_routers():
                sysupdate = Sysupdate(router, ConfigManager.get_firmware_dict()[0])
                sysupdate.start()
                sysupdate.join()
        else:
            for router_id in router_ids:
                router = cls.get_router_by_id(router_id)
                sysupdate = Sysupdate(router, ConfigManager.get_firmware_dict()[0])
                sysupdate.start()
                sysupdate.join()

    @classmethod
    def sysupgrade_firmware(cls, router_ids: List[int], upgrade_all: bool, n: bool) -> None:
        """
        Upgrades the firmware on the given :py:class:`Router` s

        :param router_ids: List of unique numbers to identify a Router
        :param upgrade_all: If all is True all Routers were upgraded
        :param n: If n is True the upgrade discard the last firmware
        """
        from util.router_flash_firmware import SysupgradeJob  # TODO remove it from here #64
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
    def setup_web_configuration(cls, router_ids: List[int], setup_all: bool, wizard: bool):
        """
        After a systemupgrade, the Router starts in config-mode without the possibility to connect again via SSH.
        Therefore this class uses selenium to parse the given webpage. All options given by the web interface of the
        Router can be set via the 'web_interface_config.yaml', except for the sysupgrade which isn't implemented yet

        :param router_ids: List of unique numbers to identify a Router
        :param setup_all: If True all Routers will be setuped via the webinterface
        """
        from util.router_setup_web_configuration import RouterWebConfigurationJob  # TODO remove it from here #64
        if setup_all:
            for i, router in enumerate(cls.get_routers()):
                cls.start_job(router, RouterWebConfigurationJob(ConfigManager.get_web_interface_config()[i], wizard))
        else:
            for i, router_id in enumerate(router_ids):
                router = cls.get_router_by_id(router_id)
                cls.start_job(router, RouterWebConfigurationJob(ConfigManager.get_web_interface_config()[i], wizard))

    @classmethod
    def reboot_router(cls, router_ids: List[int], reboot_all: bool, configmode: bool):
        """
        Reboots the given Routers.

        :param router_ids: List of unique numbers to identify a Router
        :param reboot_all: Reboots all Routers
        :param configmode: Reboots Router into configmode
        """
        from util.router_reboot import RouterRebootJob  # TODO remove it from here #64
        if reboot_all:
            for router in cls.get_routers():
                cls.start_job(router, RouterRebootJob(configmode))
        else:
            for router_id in router_ids:
                router = cls.get_router_by_id(router_id)
                cls.start_job(router, RouterRebootJob(configmode))

    @classmethod
    def get_server_version(cls) -> str:
        """
        Returns the server version as a string
        """
        return cls.VERSION
