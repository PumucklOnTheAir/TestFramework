from server.proxyobject import ProxyObject
from enum import Enum


class Mode(Enum):
    master = 1
    managed = 2
    ad_hoc = 3
    monitor = 4
    unknown = 5


class Router(ProxyObject):

    def __init__(self, vlan_iface_name: str, vlan_iface_id: int, ip: str, ip_mask: int, usr_name: str,
                 usr_password: str):

        ProxyObject.__init__(self)

        self._ip = None
        self._ip = ip

        self._vlan_iface_id = None
        self._vlan_iface_id = vlan_iface_id

        self._vlan_iface_name = None
        self._vlan_iface_name = vlan_iface_name

        self._ip_mask = None
        self._ip_mask = ip_mask

        # Optional values
        self._usr_name = usr_name
        self._usr_password = usr_password
        self._mac = None
        self._wlan_mode = Mode.unknown
        self._usr_name = None
        self._ssid = ""

    @property
    def ip(self) -> str:
        """
        IP number of the Router
        :return: IP number as string
        """
        return self._ip

    @property
    def vlan_iface_id(self) -> int:
        """
        The VLAN ID from router
        :return:
        """
        return self._vlan_iface_id

    @property
    def vlan_iface_name(self) -> str:
        """
        Used VLAN name from server for this router
        :return:
        """
        return self._vlan_iface_id

    @property
    def ip_mask(self) -> int:
        """
        IP mask
        :return:
        """
        return self._ip_mask

    # Optional information

    @property
    def usr_name(self) -> str:
        """
        Username of the admin account on the router
        :rtype: str
        :return:
        """
        return self._usr_name

    @usr_name.setter
    def usr_name(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._usr_name = value

    @property
    def usr_password(self) -> str:
        """
        Password of the admin account on the router
        :rtype: str
        :return:
        """
        return self._usr_password

    @usr_password.setter
    def usr_password(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._usr_password = value

    @property
    def mac(self) -> str:
        """
        The mac address of the routers
        :rtype: str
        :return:
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
    def ssid(self) -> str:
        """
        The SSID of the router
        :rtype: str
        :return:
        """
        return self._ssid

    @ssid.setter
    def ssid(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._ssid = value

    @property
    def wlan_mode(self) -> Mode:
        """
        The WLAN mode of the router. Value could be outdated.
        :return:
        """
        return self._wlan_mode

    @wlan_mode.setter
    def wlan_mode(self, value: Mode):
        """
        :type value: str
        """
        assert isinstance(value, Mode)
        self._wlan_mode = value
