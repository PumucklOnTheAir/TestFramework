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
    #config = Configuration("")

    def start(self, debug_mode: bool = False, config_path: str = CONFIG_PATH):
        assert isinstance(debug_mode, bool)

        self.DEBUG = debug_mode

        assert isinstance(config_path, str) # TODO funktioniert das?
        self.CONFIG_PATH = config_path

        #self._ipc_server.start_ipc_server(self)

        self.__load_configuration()

        # TODO load more Router information
        # -> (Router[])

    def __load_configuration(self):
        # (re)load the configuration only then no tests are running
        assert len(self._runningTests) == 0
        # TODO how to load the configuration, #16
        self._routers = ConfigManager.get_vlan_list()
        assert len(self._routers) != 0
        assert len(self._reports) == 0

        pass

    def stop(self):
        # TODO self._ipc_server.shutdown()
        pass

    def start_test(self, router_name, test_name) -> bool:
        """Start an specific test on an router
        :param router_name: The name of the router on which the test will run
        :param test_name: The name of the test to execute
        :return: True if start was successful
        """

        #_runningTests.add(Thread.start(test, router))
        pass

    def get_routers(self) -> []:
        """
        :return: List of known routers. List is a copy of the original list.
        """

        # check if list is still valid
        for router in self._routers:
            assert isinstance(router, Router)

        return self._routers.copy()

    def get_running_tests(self) -> []:
        """
        :return: List of running test on the test server. List is a copy of the original list.
        """
        return self._runningTests.copy()

    def get_reports(self) -> []:
        """
        :return: List of reports
        """
        return self._reports

    def get_tests(self) -> []:
        """
        :return: List of available tests on the server
        """
        pass # TODO get available test from config

    def get_firmwares(self) -> []:
        """
        :return: List of known firmwares
        """
        pass # TODO vllt vom config?

if __name__ == "__main__":
    # execute only if run as a script
    Server.start()
