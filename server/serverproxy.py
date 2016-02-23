from abc import ABCMeta, abstractclassmethod
from typing import List
from router.router import Router


class ServerProxy(metaclass=ABCMeta):
    """
    A proxy model for inter-process communication between the server runtime and clients like CLI and WebServer.
    Read the method description carefully! The behaviour may be different as expected.
    Normally the method will be executed remotely on the server and
    the return value is given by copy and not by reference!
    """""
    @abstractclassmethod
    def start_test(self, router_id, test_name) -> bool:
        """
        Start an specific test on an router

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
    def get_routers_task_queue_size(self, router_id: int) -> int:
        """
        returns current task queue at the first place and after that the task queue of the router
        :param router_id: ID of the router
        :return: task queue + current active task as a string
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
        Returns a :py:class:`Router` with the given id.

        :param router_id:
        :return: Router
        """
        pass

    @abstractclassmethod
    def sysupdate_firmware(self, router_ids: List[int], update_all: bool) -> None:
        """
        Downloads and copys the firmware to the :py:class:`Router` given in the List(by a unique id) resp. to all Routers

        :param router_ids: List of unique numbers to identify a :py:class:`Router`
        :param update_all: Is True if all Routers should be updated
        """
        pass

    @abstractclassmethod
    def sysupgrade_firmware(self, router_ids: List[int], upgrade_all: bool, n: bool) -> None:
        """
        Upgrades the firmware on the given Router(s)

        :param router_ids: List of unique numbers to identify a Router
        :param upgrade_all: If all is True all Routers were upgraded
        :param n: If n is True the upgrade discard the last firmware
        """
        pass

    @abstractclassmethod
    def setup_web_configuration(cls, router_ids: List[int], setup_all: bool, wizard: bool):
        """
        After a systemupgrade, the Router starts in config-mode without the possibility to connect again via SSH.
        Therefore this class uses selenium to parse the given webpage. All options given by the web interface of the
        Router can be set via the 'web_interface_config.yaml', except for the sysupgrade which isn't implemented yet

        :param router_ids: List of unique numbers to identify a Router
        :param setup_all: If True all Routers will be setuped via the webinterface
        :param wizard: If True the wizard-page will be configured, otherwise the expert-page
        """
        pass

    @abstractclassmethod
    def reboot_router(cls, router_ids: List[int], reboot_all: bool, configmode: bool):
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
