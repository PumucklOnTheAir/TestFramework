

class IPAddress:
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
        self._ip= value


class IPv4(IPAddress):
    def __init__(self, ip: str, mask: int):
        super().__init__(ip)
        self._mask = mask

    @property
    def mask(self) -> int:
        """
        The mask of the ip address

        :return: int
        """
        return self._mask

    @mask.setter
    def mask(self, value: int):
        """
        :type value: int
        """
        assert isinstance(value, int)
        self._mask= value


class IPv6(IPAddress):
    def __init__(self, ip: str, prefix_len: int):
        super().__init__(ip)
        self._prefix_len = prefix_len

    @property
    def prefix_len(self) -> int:
        """
        The prefix_length of the ip address

        :return: int
        """
        return self._prefix_len

    @prefix_len.setter
    def prefix_len(self, value: int):
        """
        :type value: int
        """
        assert isinstance(value, int)
        self._prefix_len= value
