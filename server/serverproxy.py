from abc import ABCMeta, abstractclassmethod
from typing import List
from router.router import Router
from unittest import TestResult


class ServerProxy(metaclass=ABCMeta):
    """
    A proxy model for inter-process communication between the server runtime and clients like CLI and WebServer.
    Read the method description carefully! The behaviour may be different as expected.
    Normally the method will be executed remotely on the server and
    the return value is given by copy and not by reference!
    """""
    @abstractclassmethod
    def start_test_set(self, router_id: int, test_set_name: str) -> bool:
        """
        Start an specific test on a router

        :param router_id: The id of the router on which the test will run
        :param test_set_name: The name of the test set to execute
        :return: True if test was successful added in the queue
        """
        pass

    @abstractclassmethod
    def get_routers(self) -> List[Router]:
        """
        List of known routers

        :return: List is a copy of the original list.
        """
        pass

    @abstractclassmethod
    def get_routers_task_queue_size(self, router_id: int) -> int:
        """
        Returns the size of the task queue including the actual running task

        :param router_id: ID of the router
        :return: queue length
        """
        pass

    @abstractclassmethod
    def get_running_tests(self) -> []:
        """
        List of running test on the test server.

        :return: List as a copy of the original list.
        """
        pass

    @abstractclassmethod
    def get_test_results(self, router_id: int = -1) -> [(int, str, TestResult)]:
        """
        Returns the firmware test results for the router

        :param router_id: the specific router or all router if id = -1
        :return: List of results
        """
        pass

    @abstractclassmethod
    def delete_test_results(self) -> int:
        """
        Remove all test results

        :return: Number of deleted results
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
    def stop(self) -> None:
        """
        Shutdown the server
        """
        pass

    @abstractclassmethod
    def stop_all_tasks(self):
        pass

    @abstractclassmethod
    def update_router_info(self, router_ids: List[int], update_all: bool) -> None:
        """
        Updates all the information about the :py:class:`Router`

        :param router_ids: List of unique numbers to identify a :py:class:`Router`
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

    @classmethod
    def router_online(cls, router_ids: List[int], update_all: bool) -> None:
        """
        Tries to connect to the `Router` and updates the Mode of the Router.

        :param router_ids: List of unique numbers to identify a :py:class:`Router`
        :param update_all: Is True if all Routers should be updated
        """
        pass

    @abstractclassmethod
    def sysupdate_firmware(self, router_ids: List[int], update_all: bool) -> None:
        """
        Downloads and copies the firmware to the :py:class:`Router` given in
        the List(by a unique id) resp. to all Routers

        :param router_ids: List of unique numbers to identify a :py:class:`Router`
        :param update_all: Is True if all Routers should be updated
        """
        pass

    @abstractclassmethod
    def sysupgrade_firmware(self, router_ids: List[int], upgrade_all: bool, n: bool) -> None:
        """
        Upgrades the firmware on the given :py:class:`Router` s

        :param router_ids: List of unique numbers to identify a Router
        :param upgrade_all: If all is True all Routers were upgraded
        :param n: If n is True the upgrade discard the last firmware
        """
        pass

    @abstractclassmethod
    def setup_web_configuration(self, router_ids: List[int], setup_all: bool, wizard: bool):
        """
        After a systemupgrade, the Router starts in config-mode without the possibility to connect again via SSH.
        Therefore this class uses selenium to parse the given webpage. All options given by the web interface of the
        Router can be set via the 'web_interface_config.yaml', except for the sysupgrade which isn't implemented yet

        :param router_ids: List of unique numbers to identify a Router
        :param setup_all: If True all Routers will be setuped via the webinterface
        :param wizard
        """
        pass

    @abstractclassmethod
    def reboot_router(self, router_ids: List[int], reboot_all: bool, configmode: bool):
        """
        Reboots the given Routers.

        :param router_ids: List of unique numbers to identify a Router
        :param reboot_all: Reboots all Routers
        :param configmode: Reboots Router into configmode
        """
        pass

    @abstractclassmethod
    def get_server_version(self) -> str:
        """
        Returns the server version as a string
        """
        pass

    @abstractclassmethod
    def register_tty(self, tty_name: str = '') -> bool:
        """
        Register tty from cli in logging
        :param tty_name: Name of the console
        :return bool: Success of the register
        """
        pass
