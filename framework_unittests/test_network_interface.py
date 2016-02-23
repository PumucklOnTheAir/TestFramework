from unittest import TestCase
from router.network_interface import NetworkInterface, Status, WifiInformation, WlanType


class TestNetworkInterface(TestCase):
    def test_create_network_interface(self):
        network_interface = NetworkInterface(0, "eth0")
        assert isinstance(network_interface, NetworkInterface)
        self.assertEqual(Status.unknown, network_interface.status)

        network_interface.mac = "d8:31:26:45:56:2f"

        ipv4 = IPv4("192.168.1.1", 24)
        network_interface.ipaddress_lst.append(ipv4)

        ipv6 = IPv6("fe80::a11:96ff:fe05:3024", 64)
        network_interface.ipaddress_lst.append(ipv6)

        network_interface.status = Status.up

        network_interface.wifi_information = self._get_wifi_informations()

        self.assertEqual("eth0", network_interface.name)
        self.assertEqual("d8:31:26:45:56:2f", network_interface.mac)
        self.assertEqual(Status.up, network_interface.status)
        self.assertEqual(ipv4, network_interface.ipaddress_lst[0])
        self.assertEqual(ipv6, network_interface.ipaddress_lst[1])
        self.assertEqual("0x1", network_interface.wifi_information.wdev)
        self.assertEqual(WlanType.managed, network_interface.wifi_information.type)
        self.assertEqual(1, network_interface.wifi_information.channel)
        self.assertEqual(20, network_interface.wifi_information.channel_width)
        self.assertEqual(2412, network_interface.wifi_information.channel_center1)

    def _get_wifi_informations(self) -> WifiInformation:
        wifi_info = WifiInformation()
        assert isinstance(wifi_info, WifiInformation)
        wifi_info.wdev = "0x1"
        wifi_info.type = WlanType.managed
        wifi_info.channel = 1
        wifi_info.channel_width = 20
        wifi_info.channel_center1 = 2412
        return wifi_info
