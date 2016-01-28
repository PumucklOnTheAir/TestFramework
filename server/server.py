from .serverproxy import ServerProxy
from .ipc import IPC
from router.router import Router
from config.configmanager import ConfigManager
from typing import List
from log.logger import Logger
import os


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
    _runningTests = []
    _routers = []
    _reports = []

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
        log_level = int(ConfigManager.get_server_property("Log_Level"))
        debug_mode = False
        if log_level is 10:
            debug_mode = True
        cls.DEBUG = debug_mode

        # create instance and give params to the logger object
        Logger().setup(log_level, log_level, log_level)

        # load Router configs
        cls.__load_configuration()

        ''' von simon auskommentiert
        if cls.VLAN:
            from util.router_info import RouterInfo
            # TODO: Die Funktion 'cls.update_router_info' sollte verwendet werden
            RouterInfo.update(cls.get_routers()[0])
        '''

        print("Runtime Server started")

        cls._ipc_server.start_ipc_server(cls, True)  # serves forever - works like a while(true)

        # at this point all code will be ignored

    @classmethod
    def __load_configuration(cls) -> None:
        # (re)load the configuration only then no tests are running
        assert len(cls._runningTests) == 0
        cls._routers = ConfigManager.get_router_auto_list()
        assert len(cls._routers) != 0
        assert len(cls._reports) == 0

    @classmethod
    def stop(cls) -> None:
        """
        Stops the server, all running tests and closes all connections.
        """
        # close open streams and the logger instance
        Logger().close()

        cls._ipc_server.shutdown()
        pass

    @classmethod
    def start_test(cls, router_name, test_name) -> bool:
        """Start an specific test on an router

        :param router_name: The name of the router on which the test will run
        :param test_name: The name of the test to execute
        :return: True if start was successful
        """
        # runningTests.add(Thread.start(test, router))
        pass

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
    def get_running_tests(cls) -> []:
        """
        :return: List of running test on the test server. List is a copy of the original list.
        """
        return cls._runningTests.copy()

    @classmethod
    def get_reports(cls) -> []:
        """
        :return: List of reports
        """
        return cls._reports

    @classmethod
    def get_tests(cls) -> []:
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
        from util.router_info import RouterInfo
        if update_all:
            for router in cls.get_routers():
                router_info = RouterInfo(router)
                router_info.start()
                router_info.join()
        else:
            for router_id in router_ids:
                router = cls.get_router_by_id(router_id)
                router_info = RouterInfo(router)
                router_info.start()
                router_info.join()

    @classmethod
    def get_router_by_id(cls, router_id: int) -> Router:
        """
        Returns a Router with the given id.

        :param router_id:
        :return: Router
        """
        routers = cls.get_routers()
        if routers[router_id].id == router_id:
            return routers[router_id]
        for router in routers:
            if router.id == router_id:
                return router
        return None

    @classmethod
    def sysupdate_firmware(cls, router_ids: List[int], update_all: bool) -> None:
        """
        Downloads and copies the firmware to the :py:class:`Router` given in the List(by a unique id) or to all Routers

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
