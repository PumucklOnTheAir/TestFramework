from Router.ip_address import IPAddress


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
