from .serverproxy import ServerProxy
from .ipc import IPC
from .router import Router
from config.configmanager import ConfigManager
from typing import List


class Server(ServerProxy):
    """" The great runtime server for all tests and more.
    This static class with class methods will be usually run as daemon on the main server.
    It is used to control the other routers, flash the firmwares and execute such as evaluate the tests.
    The web server and cli instances are connecting with this class
    and using his inherit public methods of ServerProxy.

    Troubleshooting:
    The server returns an
        "OSError: [Errno 48] Address already in use" if the server is already started
        "OSError: [Errno 99] Cannot assign requested address" ?? try to restart the computer TODO #51
    """""
    DEBUG = False
    VLAN = True
    CONFIG_PATH = "../config"
    _ipc_server = IPC()

    # runtime vars
    _runningTests = []
    _routers = []
    _reports = []

    @classmethod
    def start(cls, debug_mode: bool = False, config_path: str = CONFIG_PATH, vlan_activate: bool=True) -> None:
        """
        Starts the runtime server with all components
        :param debug_mode: Sets the log and print level
        :param config_path: Path to an alternative config directory
        :param vlan_activate: Activates/Deactivates VLANs
        """
        cls.DEBUG = debug_mode

        cls.CONFIG_PATH = config_path

        cls.VLAN = vlan_activate

        cls.__load_configuration()

        if cls.VLAN:
            from util.router_info import RouterInfo
            RouterInfo.update(cls.get_routers())

        print("Runtime Server started")

        cls._ipc_server.start_ipc_server(cls, True)  # serves forever - works like a while(true)

        # at this point all code will be ignored

    @classmethod
    def __load_configuration(cls):
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
    def get_router_by_id(cls, router_id: int) -> Router:
        """
        Returns a Router with the given id.
        :param router_id:
        :return: Router
        """
        routers = cls.get_routers()
        if routers[router_id].id == router_id:
            return router_id
        for router in routers:
            if router.id == router_id:
                return router
        return None

    @classmethod
    def sysupdate_firmware(cls, router_ids: List[int], all: bool):
        """
        Downloads and copys the firmware to the Router given in the List(by a unique id) resp. to all Routers
        :param router_ids: List of unique numbers to identify a Router
        :param all: Is True if all Routers should be updated
        """
        from util.router_flash_firmware import RouterFlashFirmware
        if all:
            for router in cls.get_routers():
                RouterFlashFirmware.sysupdate(router, ConfigManager.get_firmware_list())
        else:
            for id in router_ids:
                router = cls.get_router_by_id(id)
                RouterFlashFirmware.sysupdate(router, ConfigManager.get_firmware_list())

    @classmethod
    def sysupgrade_firmware(cls, router_ids: List[int], all: bool, n: bool):
        """
        Upgrades the firmware on the given Router(s)
        :param router_ids:
        :param all: If all is True all Routers were upgraded
        :param n: If n is True the upgrade discard the last firmware
        """
        from util.router_flash_firmware import RouterFlashFirmware
        if all:
            for router in cls.get_routers():
                RouterFlashFirmware.sysupgrade(router, n)
        else:
            for id in router_ids:
                router = cls.get_router_by_id(id)
                RouterFlashFirmware.sysupgrade(router, n)

