from router.ipv4 import IPv4
from router.ipv6 import IPv6


class NetworkInterface:

    def __init__(self, name: str, mac: str):
        self._name = name
        self._mac = mac
        self._ipv4_lst = list()
        self._ipv6_lst = list()

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

    @property
    def ipv4_lst(self, index: int) -> IPv4:
        """
        The ipv4 addresses of the network interface
        :return: IPv4
        """
        return self._ipv4_lst[index]

    @ipv4_lst.setter
    def ipv4_lst(self, value: IPv4):
        """
        :type value: IPv4
        """
        assert isinstance(value, IPv4)
        self._ipv4_lst.append(value)

    @property
    def ipv6_lst(self, index: int) -> IPv6:
        """
        The ipv6 addresses of the network interface
        :return: IPv6
        """
        return self._ipv6_lst[index]

    @ipv6_lst.setter
    def ipv6_lst(self, value: IPv6):
        """
        :type value: IPv6
        """
        assert isinstance(value, IPv6)
        self._ipv6_lst.append(value)
