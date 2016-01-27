from server.proxyobject import ProxyObject
from enum import Enum
from firmware.firmware import Firmware
from network.remote_system import RemoteSystem
from router.memory import RAM, Flashdriver


class WlanMode(Enum):
    master = 1
    managed = 2
    ad_hoc = 3
    monitor = 4
    unknown = 5


class Mode(Enum):
    """
    The Router can be in two modes: normal and configuration.
    If the mode changes also the ip-address changes.
    """""
    normal = 1
    configuration = 2
    unknown = 3


class Router(ProxyObject, RemoteSystem):
    """
    This class represent a Freifunk-Router
    """""

    def __init__(self, id: int, vlan_iface_name: str, vlan_iface_id: int, ip: str, ip_mask: int,
                 config_ip: str, config_ip_mask: int, usr_name: str, usr_password: str, power_socket: int):

        ProxyObject.__init__(self)

        self._id = id
        self._ip = ip
        self._ip_mask = ip_mask
        self._config_ip = config_ip
        self._config_ip_mask = config_ip_mask
        self._vlan_iface_id = vlan_iface_id
        self._vlan_iface_name = vlan_iface_name
        self._namespace_name = "nsp" + str(self._vlan_iface_id)
        self._power_socket = power_socket

        # Optional values
        self._mode = Mode.unknown
        self._model = None
        self._usr_name = usr_name
        self._usr_password = usr_password
        self._mac = '00:00:00:00:00:00'
        self._wlan_mode = WlanMode.unknown
        self._ssid = ''
        self.interfaces = dict()
        self.cpu_processes = list()
        self._ram = None
        self._flashdriver = None
        self._firmware = Firmware.get_default_firmware()

    @property
    def id(self) -> int:
        """
        ID of the :py:class:`Router`

        :return: ID number as in
        """
        return self._id

    @property
    def ip(self) -> str:
        """
        :return: IP number of the Router. In dependency of the Mode
        """
        if self._mode == Mode.configuration:
            return self._config_ip
        else:
            return self._ip

    @property
    def ip_mask(self) -> int:
        """
        IP mask. In dependency of the Mode

        :return:
        """
        if self._mode == Mode.configuration:
            return self._config_ip_mask
        else:
            return self._ip_mask

    @property
    def vlan_iface_id(self) -> int:
        """
        :return The VLAN ID from router:
        """
        return self._vlan_iface_id

    @property
    def vlan_iface_name(self) -> str:
        """
        Used VLAN name from server for this router

        :return:
        """
        return self._vlan_iface_name

    # Optional information

    @property
    def usr_name(self) -> str:
        """
        Username of the admin account on the router

        :rtype: str
        :return:
        """
        return self._usr_name

    @property
    def usr_password(self) -> str:
        """
        Password of the admin account on the router

        :rtype: str
        :return:
        """
        return self._usr_password

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
        assert isinstance(value, WlanMode)
        self._wlan_mode = value

    @property
    def model(self) -> str:
        """
        :return The model and version of the router. Value could be outdated.:
        """
        return self._model

    @model.setter
    def model(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._model = value

    @property
    def power_socket(self) -> int:
        """
        The power socket of the routers

        :rtype: int
        :return:
        """
        return self._power_socket

    @power_socket.setter
    def power_socket(self, value: int):
        """
        :type value: int
        """
        assert isinstance(value, int)
        self._power_socket = value

    @property
    def firmware(self) -> Firmware:
        """
        The :py:class:`Firmware` of the router

        :rtype: Firmware
        :return:
        """
        return self._firmware

    @firmware.setter
    def firmware(self, value: Firmware):
        """
        :type value: :py:class:`Firmware`
        """
        assert isinstance(value, Firmware)
        self._firmware = value

    @property
    def namespace_name(self) -> str:
        """
        The namespace name of the router

        :rtype: str
        :return:
        """
        return self._namespace_name

    @property
    def mode(self) -> Mode:
        """
        The Mode of the routers

        :rtype: Mode
        :return:
        """
        return self._mode

    @mode.setter
    def mode(self, value: Mode):
        """
        :type value: Mode
        """
        assert isinstance(value, Mode)
        self._mode = value

    @property
    def ram(self) -> RAM:
        """
        The RAM of the routers

        :rtype: RAM
        :return:
        """
        return self._ram

    @ram.setter
    def ram(self, value: RAM):
        """
        :type value: RAM
        """
        assert isinstance(value, RAM)
        self._ram = value

    @property
    def flashdriver(self) -> Flashdriver:
        """
        The Flashdriver of the routers

        :rtype: Flashdriver
        :return:
        """
        return self._flashdriver

    @flashdriver.setter
    def flashdriver(self, value: Flashdriver):
        """
        :type value: Flashdriver
        """
        assert isinstance(value, Flashdriver)
        self._flashdriver = value
