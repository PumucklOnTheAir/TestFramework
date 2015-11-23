from abc import ABCMeta, abstractmethod


class ServerProxy(metaclass=ABCMeta):
    """A proxy model for inter-process communication between the server runtime and clients like CLI and WebServer.
    Read the method description carefully! The behaviour may be different as expected.
    Normally the method will be execute remote on the server and the return value is given by copy and not reference!
    """""
    @abstractmethod
    def start_test(self, router_id, test_id):
        pass

    @abstractmethod
    @property
    def get_routers(self) -> []:
        pass

    @abstractmethod
    @property
    def get_running_tests(self) -> []:
        pass

    @abstractmethod
    @property
    def get_reports(self) -> []:
        pass

    @abstractmethod
    def get_tests(self) -> []:
        pass

    @abstractmethod
    def get_firmwares(self) -> []:
        pass
