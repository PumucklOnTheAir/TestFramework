from abc import ABCMeta, abstractmethod


class ServerProxy(metaclass=ABCMeta):
    """A proxy model for inter-process communication between the server runtime and clients like CLI and WebServer.
    Read the method description carefully! The behaviour may be different as expected.
    Normally the method will be execute remote on the server and the return value is given by copy and not reference!
    """""
    @abstractmethod
    def start_test(self, router_name, test_name) -> bool:
        """Start an specific test on an router
        :param router_name: The name of the router on which the test will run
        :param test_name: The name of the test to execute
        :return: True if start was successful
        """
        pass

    @abstractmethod
    def get_routers(self) -> []:
        """
        :return: List of known routers
        """
        pass

    @abstractmethod
    def get_running_tests(self) -> []:
        """
        :return: List of running test on the test server
        """
        pass

    @abstractmethod
    def get_reports(self) -> []:
        """
        :return: List of reports
        """
        pass

    @abstractmethod
    def get_tests(self) -> []:
        """
        :return: List of available tests on the server
        """
        pass

    @abstractmethod
    def get_firmwares(self) -> []:
        """
        :return: List of known firmwares
        """
        pass
