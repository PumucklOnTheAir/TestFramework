from enum import Enum
import ipaddress


class Status(Enum):
    """
    A network interface can be in one of this three states.
    """""
    up = 1
    down = 2
    unknown = 3


class WlanType(Enum):
    """
    The Wifi can be in six modes or is unknown
    """""
    ap = 1
    managed = 2
    monitor = 3
    ibss = 4
    wds = 5
    mesh = 6
    unkown = 7


class WifiInformation:
    """
    Some informations that only the wlan interfaces do have.
    """""

    def __init__(self):
        """
        wdev: Another identifier for the wireless interface
        type: Wlan Mode
        channel: Wifi Channel from 1 to 14
        channel_width: 20 MHZ or 40 MHZ
        channel_center1: center of the channel in MHZ
        """
        self._wdev = None
        self._ssid = None
        self._type = WlanType.unkown
        self._channel = None
        self._channel_width = None
        self._channel_center1 = None

    @property
    def wdev(self) -> str:
        """
        Another identifier for the wireless interface.

        :return: Another identifier for the wireless interface as a str
        """
        return self._wdev

    @wdev.setter
    def wdev(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._wdev = value

    @property
    def ssid(self) -> str:
        """
        SSID: Service Set Identifier.

        :return: Service Set Identifier as a str
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
    def type(self) -> WlanType:
        """
        Wlan Mode

        :return: WlanType
        """
        return self._type

    @type.setter
    def type(self, value):
        """
        :type value: WlanType or str
        """
        if isinstance(value, WlanType):
            self._type = value
        else:
            if value == "AP":
                self._type = WlanType.ap
            elif value == "managed":
                self._type = WlanType.managed
            elif value == "monitor":
                self._type = WlanType.monitor
            elif value == "IBSS" or value == "adhoc":
                self._type = WlanType.ibss
            elif value == "wds" or value == "WDS":
                self._type = WlanType.wds
            elif value == "mesh":
                self._type = WlanType.mesh
            else:
                self.type = WlanType.unkown

    @property
    def channel(self) -> int:
        """
        Wifi Channel from 1 to 14.

        :return: Wifi Channel as an int
        """
        return self._channel

    @channel.setter
    def channel(self, value: int):
        """
        :type value: int
        """
        assert isinstance(value, int)
        self._channel = value

    @property
    def channel_width(self) -> int:
        """
        Channel_width: 20 MHZ or 40 MHZ

        :return: Channel_width as an int
        """
        return self._channel_width

    @channel_width.setter
    def channel_width(self, value: int):
        """
        :type value: int
        """
        assert isinstance(value, int)
        self._channel_width = value

    @property
    def channel_center1(self) -> int:
        """
        Center of the channel in MHZ.

        :return: Center of the channel as an int
        """
        return self._channel_center1

    @channel_center1.setter
    def channel_center1(self, value: int):
        """
        :type value: int
        """
        assert isinstance(value, int)
        self._channel_center1 = value

    def __str__(self):
        return (str(self.wdev) + ": " + str(self.ssid) + ", " + str(self.type) + ", " +
                str(self.channel) + ", " + str(self.channel_width) + ", " + str(self.channel_center1))


class NetworkInterface:
    """
    This class represents a Network Interface, with an id, a name, a status, a mac address and a list of IPs.
    """""

    def __init__(self, id: int, name: str):
        """
        :param name: The name of the network-interface
        """
        self._id = id
        self._name = name
        self._status = Status.unknown
        self._mac = "00:00:00:00:00:00"
        self.ipaddress_lst = list()
        self._wifi_information = None

    @property
    def id(self) -> str:
        """
        The id of the network-interface.

        :return: The id of the network-interface as an int
        """
        return self._id

    @property
    def name(self) -> str:
        """
        The name of the network-interface.

        :return: The name of the network-interface as a str
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
        The status of the network-interface.

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
        The mac addresses of the network-interface.

        :return: The mac addresses of the network-interface as a str
        """
        return self._mac

    @mac.setter
    def mac(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._mac = value

    def add_ip_address(self, ip: str, ip_mask: int):
        """
        Add a new IP to the network-interface.

        :param ip: ip address
        :param ip_mask: ip mask or length prefix-length if IPv6
        """
        self.ipaddress_lst.append(ipaddress.ip_interface(ip + "/" + str(ip_mask)))

    @property
    def wifi_information(self) -> WifiInformation:
        """
        Some informations that only the wlan-interfaces do have.

        :return: WifiInformation
        """
        return self._wifi_information

    @wifi_information.setter
    def wifi_information(self, value: WifiInformation):
        """
        :type value: WifiInformation
        """
        assert isinstance(value, WifiInformation)
        self._wifi_information = value

    def __str__(self):
        ipaddresses = "["
        for ip in self.ipaddress_lst:
            ipaddresses = ipaddresses + " " + str(ip)
        ipaddresses += " ]"
        return (str(self.id) + ": " + self.name + ", " + self.mac + ", " + str(self.status) + ", " + str(ipaddresses) +
                "\n Wifi info: " + str(self.wifi_information))
