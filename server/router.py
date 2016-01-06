from .proxyobject import ProxyObject
from enum import Enum

from firmware.firmware import Firmware
from network.network_iface import NetworkIface

from abc import ABCMeta, abstractmethod
from log.logger import Logger
from threading import Thread


class Mode(Enum):
    master = 1
    managed = 2
    ad_hoc = 3
    monitor = 4
    unknown = 5


class Router(ProxyObject, NetworkIface):

    def __init__(self, id: int, vlan_iface_name: str, vlan_iface_id: int, ip: str, ip_mask: int, usr_name: str,
                 usr_password: str, power_socket: int):

        ProxyObject.__init__(self)

        self._id = None
        self._id = id

        self._ip = None
        self._ip = ip

        self._vlan_iface_id = None
        self._vlan_iface_id = vlan_iface_id

        self._vlan_iface_name = None
        self._vlan_iface_name = vlan_iface_name

        self._ip_mask = None
        self._ip_mask = ip_mask

        self._power_socket = None
        self._power_socket = power_socket

        # Optional values
        self._model = None
        self._usr_name = usr_name
        self._usr_password = usr_password
        self._mac = '00:00:00:00:00:00'
        self._wlan_mode = Mode.unknown
        self._ssid = ''
        self._firmware = Firmware.get_default_firmware()

        # test/task handling
        self.running_task = None
        self.waiting_tasks = []

    def __str__(self):
        return "Router{ID:%s, PS:%s, %s}" % (self.id, self.power_socket, self.wlan_mode)

    @property
    def id(self) -> int:
        """
        ID of the Router
        :return: ID number as in
        """
        return self._id

    @property
    def ip(self) -> str:
        """
        IP number of the Router
        :return: IP number as string
        """
        return self._ip

    @property
    def id(self) -> int:
        """
        The ID from router. Is the same as the VLAN ID.
        :return:
        """
        return self._vlan_iface_id

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
        return self._vlan_iface_name

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
        assert isinstance(value, Mode)
        self._wlan_mode = value

    @property
    def model(self) -> str:
        """
        The model and version of the router. Value could be outdated.
        :return:
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
        The firmware of the routers
        :rtype: Firmware
        :return:
        """
        return self._firmware

    @firmware.setter
    def firmware(self, value: Firmware):
        """
        :type value: Firmware
        """
        assert isinstance(value, Firmware)
        self._firmware = value


class RouterTask(metaclass=ABCMeta):
    def __init__(self):
        self.router = None

    def prepare(self, router: Router):
        Logger().debug("TestCase prepare", 3)
        self.router = router


class RouterJob(RouterTask, Thread, metaclass=ABCMeta):

    @abstractmethod
    def post_process(self, data):
        pass
