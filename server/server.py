from server.serverproxy import ServerProxy
from server.ipc import IPC
from server.router import Router
from config.ConfigManager import ConfigManager
from typing import List


class Server(ServerProxy):
    """" The great runtime server for all tests and more.
    This static class with class methods will be usually run as deamon on the main server.
    It is used to control the other routers, flash the firmwares and execute such as evaluate the tests.
    The webserver and cli instances are connecting with this class
    and using his inherit public methods of ServerProxy.
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
        assert isinstance(debug_mode, bool)
        cls.DEBUG = debug_mode

        assert isinstance(config_path, str)
        cls.CONFIG_PATH = config_path

        cls.VLAN = vlan_activate

        cls._ipc_server.start_ipc_server(cls)

        cls.__load_configuration()

        if cls.VLAN:
            from util.router_info import RouterInfo
            RouterInfo.update(cls.get_routers())

    @classmethod
    def __load_configuration(cls):
        # (re)load the configuration only then no tests are running
        assert len(cls._runningTests) == 0
        cls._routers = ConfigManager.get_vlan_list()
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

if __name__ == "__main__":
    # execute only if run as a script
    Server.start()
