from abc import ABCMeta, abstractclassmethod
from typing import List
from server.router import Router


class ServerProxy(metaclass=ABCMeta):
    """A proxy model for inter-process communication between the server runtime and clients like CLI and WebServer.
    Read the method description carefully! The behaviour may be different as expected.
    Normally the method will be execute remote on the server and the return value is given by copy and not reference!
    """""
    @abstractclassmethod
    def start_test(self, router_id, test_name) -> bool:
        """Start an specific test on an router
        :param router_id: The (vlan)ID of the router on which the test will run
        :param test_name: The name of the test to execute
        :return: True if start was successful
        """
        pass

    @abstractclassmethod
    def get_routers(self) -> List[Router]:
        """
        :return: List of known routers
        """
        pass

    @abstractclassmethod
    def get_running_tests(self) -> []:
        """
        :return: List of running test on the test server
        """
        pass

    @abstractclassmethod
    def get_reports(self) -> []:
        """
        :return: List of reports
        """
        pass

    @abstractclassmethod
    def get_tests(self) -> []:
        """
        :return: List of available tests on the server
        """
        pass

    @abstractclassmethod
    def get_firmwares(self) -> []:
        """
        :return: List of known firmwares
        """
        pass

    @abstractclassmethod
    def stop(self) -> []:
        """
        :return: Shutdown the server
        """
        pass
