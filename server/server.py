from .serverproxy import ServerProxy
from .ipc import IPC
from .router import Router, RouterTask, RouterJob
from config.configmanager import ConfigManager
from typing import List
from .test import FirmwareTest
from concurrent.futures import ProcessPoolExecutor
# from util.router_info import RouterInfo # TODO can not import properly the RouterInfo #64
from log.logger import Logger
from concurrent.futures import Future
import os
# type alias
FirmwareTestClass = type(FirmwareTest)


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
    VERSION = "0.1"
    DEBUG = False
    VLAN = True
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
    CONFIG_PATH = os.path.join(BASE_DIR, 'config')  # Join Project Root with config
    _ipc_server = IPC()

    # runtime vars
    _routers = []
    _reports = []
    # TODO reichen Threads aus? oder müssen es Prozesse sein wegen VLAN? -> Es müssen Prozesse sein..
    executor = None

    @classmethod
    def start(cls, config_path: str = CONFIG_PATH) -> None:
        """
        Starts the runtime server with all components

        :param config_path: Path to an alternative config directory
        """
        cls.CONFIG_PATH = config_path
        # set the config_path at the manager
        ConfigManager.set_config_path(config_path)

        # read from config the Vlan mode
        vlan_activate = ConfigManager.get_server_property("Vlan_On")
        cls.VLAN = vlan_activate

        # read from config if debug mode is on
        log_level = ConfigManager.get_server_property("Log_Level")
        debug_mode = False
        if log_level is 10:
            debug_mode = True
        cls.DEBUG = debug_mode

        # load Router configs
        cls.__load_configuration()

        # deprecated
        # cls.update_router_info(cls.get_routers()[0])  # TODO das ist doch nicht richtig? #64

        Logger().info("Runtime Server started")

        cls.executor = ProcessPoolExecutor(max_workers=len(cls._routers))

        try:
            cls._ipc_server.start_ipc_server(cls, True)  # serves forever - works like a while(true)
        except (KeyboardInterrupt, SystemExit):
            Logger().info("Received an interrupt signal")
            cls.stop()

        # at this point following code will be ignored

    @classmethod
    def __load_configuration(cls):
        Logger().debug("Load configuration")
        cls._routers = ConfigManager.get_router_auto_list()
        # cls._ set fixed demo test ConnectionTest

    @classmethod
    def stop(cls) -> None:
        """
        Stops the server, all running tests and closes all connections.
        """
        cls.executor.shutdown(wait=False)
        cls._ipc_server.shutdown()

    @classmethod
    def stop_all_tasks(cls):
        cls.executor.shutdown(wait=False)
        for router in cls.get_routers():
            router.running_task = None

    @classmethod
    def get_test_by_name(cls, test_name: str) -> FirmwareTestClass:
        # TODO test verwaltung
        pass

    @classmethod
    def start_test(cls, router_id: int, test_name: str) -> bool:
        """Start an specific test on an router

        :param router_id: The id of the router on which the test will run
        :param test_name: The name of the test to execute
        :return: True if start was successful
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
    def __start_task(cls, router: Router, job: RouterTask) -> bool:
        if job is None:  # no job given? look up for the next job in the queue
            Logger().debug("Task object is none", 1)
            if len(router.waiting_tasks) == 0:
                Logger().debug("No tasks in the queue to run.", 2)
                return False
            else:
                if router.running_task is not None:
                    Logger().debug("Router working. Next task has to wait..", 3)
                    return False
                else:
                    Logger().debug("Get next task from the queue", 3)
                    job = router.waiting_tasks.pop(0)

        if router.running_task is None:
            Logger().debug("Starting test " + str(job), 1)
            router.running_task = job
            if isinstance(job, FirmwareTestClass):
                # Task is a test
                task = cls.executor.submit(cls._execute_test, job, router)
                task.add_done_callback(cls._test_done)
            else:
                # task is a regular job
                task = cls.executor.submit(cls._execute_task, job, router)
                task.add_done_callback(cls._task_done)
            task.router = router

            return True
        else:
            Logger().debug("Put test in the wait queue. " + str(job), 1)
            router.waiting_tasks.append(job)
            return False

    @classmethod
    def _execute_task(cls, job: RouterJob, router: Router):
        # proofed: this method runs in other process as the server
        Logger().debug("Execute task " + str(job) + " on " + str(router), 2)
        cls.__activate_vlan(router)
        job.run()
        return job.join()  # TODO timeout setzen

    @classmethod
    def _execute_test(cls, test: FirmwareTestClass, router: Router):  # -> TestResult:
        # proofed: this method runs in other process as the server
        Logger().debug("Execute test " + str(test) + " on " + str(router), 2)
        Logger().debug("Execute test cases.. ", 3)

        from unittest import defaultTestLoader
        from unittest.result import TestResult
        test_suite = defaultTestLoader.loadTestsFromTestCase(test)

        nv_assi = cls.__activate_vlan(router)

        # prepare all test cases
        for test_case in test_suite:
            Logger().debug("Next TestCase " + str(test_case), 3)
            test_case.prepare(router)

        result = TestResult()
        result = test_suite.run(result)  # TODO if debug set, run as debug()
        Logger().debug("Result from test " + str(result), 3)

        # I'm sry for this dirty hack, but if you don't do this you get an
        # "TypeError: cannot serialize '_io.TextIOWrapper' object" because sys.stdout is not serializeable...
        result._original_stdout = None
        result._original_stderr = None

        cls.__deactivate_vlan(nv_assi)

        return result

    @classmethod
    def _test_done(cls, task: Future):
        Logger().debug("Test done " + str(task), 1)
        Logger().debug("From " + str(task.router), 2)
        task.router.running_task = None
        exception = task.exception()
        if exception is not None:
            Logger().error("Test case raised an exception: " + str(exception), 1)
        else:
            cls._reports.append(task.result())

        # start next test in the queue
        cls.__start_task(task.router, None)

    @classmethod
    def _task_done(cls, task: Future):
        Logger().debug("Task done " + str(task), 1)
        Logger().debug("At " + str(task.router), 2)
        task.router.running_task = None
        # TODO task steckerleiste has now router
        exception = task.exception()
        if exception is not None:
            Logger().error("Task raised an exception: " + str(exception), 1)
        else:
            task.router.running_task.post_process(task.result())

        # start next test in the queue
        cls.__start_task(task.router, None)

    @classmethod
    def __activate_vlan(cls, router: Router):  # -> NVAssistent:
        if cls.VLAN:
            from network.nv_assist import NVAssistent  # TODO auslagern...
            #NetworkCtrl(router)
            nv_assi = NVAssistent()
            nv_assi.create_namespace_vlan(router.namespace_name, "eth0", router.vlan_iface_name, router.vlan_iface_id)
            return nv_assi
        else:
            Logger().debug("Ignoring activate VLAN", 2)
            Logger().debug("Var VLAN is false", 3)

    @classmethod
    def __deactivate_vlan(cls, nv_assi): # "NVAssistent"
        nv_assi.delete_namespace()

    @classmethod
    def get_routers(cls) -> List[Router]:
        """
        :return: List of known routers. List is a copy of the original list.
        """

        # check if list is still valid
        for router in cls._routers:
            assert isinstance(router, Router)

        return cls._routers.copy()

    @classmethod
    def get_running_tests(cls) -> List[FirmwareTestClass]:
        """
        :return: List of running test on the test server. List is a copy of the original list.
        """
        # TODO exist now in router
        return cls._running_tasks.copy()

    @classmethod
    def get_reports(cls) -> []:
        """
        :return: List of reports
        """
        return cls._reports

    @classmethod
    def get_tests(cls) -> List[FirmwareTestClass]:
        """
        :return: List of available tests on the server
        """
        # TODO get available test from config
        pass

    @classmethod
    def get_firmwares(cls) -> []:
        """
        :return: List of known firmwares
        """
        # TODO vllt vom config?
        pass

    @classmethod
    def update_router_info(cls, router_ids: List[int], update_all: bool) -> None:
        """
        Updates all the information about the :py:class:`Router`

        :param router_ids: List of unique numbers to identify a :py:class:`Router`
        :param update_all: Is True if all Routers should be updated
        """
        if cls.VLAN:
            from util.router_info import RouterInfo  # TODO remove it from here #64

            if update_all:
                for router in cls.get_routers():
                    RouterInfo.update(router)
            else:
                for router_id in router_ids:
                    router = cls.get_router_by_id(router_id)
                    RouterInfo.update(router)
        else:
            Logger().info("Update Router Info deactivated - set VLAN to true to activate it")

    @classmethod
    def get_router_by_id(cls, router_id: int) -> Router:
        """
        Returns a Router with the given id.

        :param router_id:
        :return: Router
        """
        Logger().debug("get_router_by_id with id: " + str(router_id), 1)
        # if routers[router_id].id == router_id:
        #     return router_id # IndexError
        for router in cls._routers:
            if router.id == router_id:
                Logger().debug("return Router: " + str(router), 2)
                return router
        return None

    @classmethod
    def sysupdate_firmware(cls, router_ids: List[int], update_all: bool) -> None:
        """
        Downloads and copies the firmware to the :py:class:`Router` given in the List(by a unique id) resp. to all Routers

        :param router_ids: List of unique numbers to identify a :py:class:`Router`
        :param update_all: Is True if all Routers should be updated
        """
        from util.router_flash_firmware import RouterFlashFirmware
        if update_all:
            for router in cls.get_routers():
                RouterFlashFirmware.sysupdate(router, ConfigManager.get_firmware_dict()[0])
        else:
            for router_id in router_ids:
                router = cls.get_router_by_id(router_id)
                RouterFlashFirmware.sysupdate(router, ConfigManager.get_firmware_dict()[0])

    @classmethod
    def sysupgrade_firmware(cls, router_ids: List[int], upgrade_all: bool, n: bool) -> None:
        """
        Upgrades the firmware on the given :py:class:`Router` s

        :param router_ids: List of unique numbers to identify a Router
        :param upgrade_all: If all is True all Routers were upgraded
        :param n: If n is True the upgrade discard the last firmware
        """
        from util.router_flash_firmware import RouterFlashFirmware
        if upgrade_all:
            for router in cls.get_routers():
                RouterFlashFirmware.sysupgrade(router, n)
        else:
            for router_id in router_ids:
                router = cls.get_router_by_id(router_id)
                RouterFlashFirmware.sysupgrade(router, n)

    @classmethod
    def setup_web_configuration(cls, router_ids: List[int], setup_all: bool):
        """
        After a systemupgrade, the Router starts in config-mode without the possibility to connect again via SSH.
        Therefore this class uses selenium to parse the given webpage. All options given by the web interface of the
        Router can be set via the 'web_interface_config.yaml', except for the sysupgrade which isn't implemented yet

        :param router_ids: List of unique numbers to identify a Router
        :param setup_all: If True all Routers will be setuped via the webinterface
        """
        from util.router_setup_web_configuration import RouterWebConfiguration
        if setup_all:
            for i, router in enumerate(cls.get_routers()):
                RouterWebConfiguration.setup(router, ConfigManager.get_web_interface_config()[i])
        else:
            for i, router_id in enumerate(router_ids):
                router = cls.get_router_by_id(router_id)
                RouterWebConfiguration.setup(router, ConfigManager.get_web_interface_config()[i])

    @classmethod
    def reboot_router(cls, router_ids: List[int], reboot_all: bool, configmode: bool):
        """
        Reboots the given Routers.

        :param router_ids: List of unique numbers to identify a Router
        :param reboot_all: Reboots all Routers
        :param configmode: Reboots Router into configmode
        """
        from util.router_reboot import RouterReboot
        if reboot_all:
            for router in cls.get_routers():
                if configmode:
                    RouterReboot.configmode(router)
                else:
                    RouterReboot.normal(router)
        else:
            for router_id in router_ids:
                router = cls.get_router_by_id(router_id)
                if configmode:
                    RouterReboot.configmode(router)
                else:
                    RouterReboot.normal(router)

    @classmethod
    def get_server_version(cls) -> str:
        """
        Returns the server version as a string
        """
        return cls.VERSION
