from server.serverproxy import ServerProxy
from server.ipc import IPC
from server.router import Router
from config.ConfigManager import ConfigManager


class Server(ServerProxy):
    DEBUG = False
    CONFIG_PATH = "../config"
    _ipc_server = IPC()

    # runtime vars
    _runningTests = []
    _routers = []
    _reports = []

    @classmethod
    def start(cls, debug_mode: bool = False, config_path: str = CONFIG_PATH):
        assert isinstance(debug_mode, bool)
        cls.DEBUG = debug_mode

        assert isinstance(config_path, str)
        cls.CONFIG_PATH = config_path

        cls._ipc_server.start_ipc_server(cls)

        cls.__load_configuration()

        # TODO load more Router information
        # -> (Router[])

    @classmethod
    def __load_configuration(cls):
        # (re)load the configuration only then no tests are running
        assert len(cls._runningTests) == 0
        cls._routers = ConfigManager.get_vlan_list()
        assert len(cls._routers) != 0
        assert len(cls._reports) == 0

    @classmethod
    def stop(cls):
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
    def get_routers(cls) -> []:
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
