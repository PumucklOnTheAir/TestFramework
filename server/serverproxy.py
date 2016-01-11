from abc import ABCMeta, abstractclassmethod
from typing import List
from server.router import Router


class ServerProxy(metaclass=ABCMeta):
    """A proxy model for inter-process communication between the server runtime and clients like CLI and WebServer.
    Read the method description carefully! The behaviour may be different as expected.
    Normally the method will be execute remote on the server and the return value is given by copy and not reference!
    """""
    @abstractclassmethod
    def start_test(self, router_name, test_name) -> bool:
        """Start an specific test on an router

        :param router_name: The name of the router on which the test will run
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
        :return: List of known firmware
        """
        pass

    @abstractclassmethod
    def stop(self) -> []:
        """
        :return: Shutdown the server
        """
        pass

    @abstractclassmethod
    def update_router_info(self, router_ids: List[int], update_all: bool) -> None:
        """
        Updates all the information about the Router

        :param router_ids: List of unique numbers to identify a Router
        :param update_all: Is True if all Routers should be updated
        """
        pass

    @abstractclassmethod
    def get_router_by_id(self, router_id: int) -> Router:
        """
        Returns a Router with the given id.

        :param router_id:
        :return: Router
        """
        pass

    @abstractclassmethod
    def sysupdate_firmware(self, router_ids: List[int], update_all: bool) -> None:
        """
        Downloads and copys the firmware to the Router given in the List(by a unique id) resp. to all Routers

        :param router_ids: List of unique numbers to identify a Router
        :param update_all: Is True if all Routers should be updated
        """
        pass

    @abstractclassmethod
    def sysupgrade_firmware(self, router_ids: List[int], upgrade_all: bool, n: bool) -> None:
        """
        Upgrades the firmware on the given Router(s)

        :param router_ids:
        :param upgrade_all: If all is True all Routers were upgraded
        :param n: If n is True the upgrade discard the last firmware
        """
        pass
