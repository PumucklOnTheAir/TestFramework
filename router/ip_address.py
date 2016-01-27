from abc import ABCMeta


class IPAddress(metaclass=ABCMeta):
    """
    This abstract class represents the IP address as an object.
    """""

    def __init__(self, ip: str):
        self._ip = ip

    @property
    def ip(self) -> str:
        """
        The ip address

        :return: str
        """
        return self._ip

    @ip.setter
    def ip(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._ip = value


class IPv4(IPAddress):
    """
    This class represents an IPv4 address, with IPAddress as the super-class.
    """""
    def __init__(self, ip: str, mask: int):
        """
        :param ip: the ip address
        :param mask: the netmask of the ip address
        """
        super().__init__(ip)
        self._mask = mask

    @property
    def mask(self) -> int:
        """
        The netmask of the ip address

        :return: int
        """
        return self._mask

    @mask.setter
    def mask(self, value: int):
        """
        :type value: int
        """
        assert isinstance(value, int)
        self._mask = value

    def __str__(self):
        return self.ip + "/" + str(self.mask)


class IPv6(IPAddress):
    def __init__(self, ip: str, prefix_len: int):
        """
        :param ip: the ip address
        :param prefix_len: the prefix-length of the ip address
        """
        super().__init__(ip)
        self._prefix_len = prefix_len

    @property
    def prefix_len(self) -> int:
        """
        The prefix-length of the ip address

        :return: int
        """
        return self._prefix_len

    @prefix_len.setter
    def prefix_len(self, value: int):
        """
        :type value: int
        """
        assert isinstance(value, int)
        self._prefix_len = value

    def __str__(self):
        return self.ip + str(self.prefix_len)
