

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
        self._ip = value
