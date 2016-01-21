from router.ip_address import IPv4, IPv6
from enum import Enum


class Status(Enum):
    """
    A network interface can be in one of this three states.
    """""
    up = 1
    down = 2
    unknown = 3


class NetworkInterface:
    """
    This class represents a Network Interface, with a name, a mac address and two lists of IPs.
    """""

    def __init__(self, name: str, mac: str):
        """
        This class represents a Network Interface.

        :param name: The name of the interface
        :param mac: The mac address of the interface
        """
        self._name = name
        self._status = Status.unknown
        self._mac = mac
        self.ipv4_lst = list()
        self.ipv6_lst = list()

    @property
    def name(self) -> str:
        """
        The name of the network interface
        :return: str
        """
        return self._name

    @name.setter
    def name(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._name = value

    @property
    def status(self) -> Status:
        """
        The status of the network interface
        :return: Status
        """
        return self._status

    @status.setter
    def status(self, value: Status):
        """
        :type value: Status
        """
        assert isinstance(value, Status)
        self._status = value

    @property
    def mac(self) -> str:
        """
        The mac addresses of the network interface
        :return: str
        """
        return self._mac

    @mac.setter
    def mac(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._mac = value
