from unittest import TestCase
from router.network_interface import NetworkInterface, Status, WifiInformation, WlanType
import ipaddress


class TestNetworkInterface(TestCase):

    def test_create_network_interface(self):
        network_interface = NetworkInterface(0, "eth0")

        assert isinstance(network_interface, NetworkInterface)

        self.assertEqual(Status.unknown, network_interface.status)

        network_interface.mac = "d8:31:26:45:56:2f"

        network_interface.add_ip_address("192.168.1.1", 24)
        network_interface.add_ip_address("fe80::a11:96ff:fe05:3024", 64)

        network_interface.status = Status.up

        network_interface.wifi_information = self._get_wifi_informations()

        self.assertEqual("eth0", network_interface.name)
        self.assertEqual("d8:31:26:45:56:2f", network_interface.mac)
        self.assertEqual(Status.up, network_interface.status)
        self.assertEqual(ipaddress.ip_interface("192.168.1.1/24"), network_interface.ipaddress_lst[0])
        self.assertEqual(ipaddress.ip_interface("fe80::a11:96ff:fe05:3024/64"), network_interface.ipaddress_lst[1])
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

    def test_wifi_type_setter(self):
        wifi_info = WifiInformation()

        assert isinstance(wifi_info, WifiInformation)

        self.assertEqual(WlanType.unkown, wifi_info.type)
        wifi_info.type = "AP"
        self.assertEqual(WlanType.ap, wifi_info.type)
        wifi_info.type = "managed"
        self.assertEqual(WlanType.managed, wifi_info.type)
        wifi_info.type = "monitor"
        self.assertEqual(WlanType.monitor, wifi_info.type)
        wifi_info.type = "IBSS"
        self.assertEqual(WlanType.ibss, wifi_info.type)
        wifi_info.type = "adhoc"
        self.assertEqual(WlanType.ibss, wifi_info.type)
        wifi_info.type = "wds"
        self.assertEqual(WlanType.wds, wifi_info.type)
        wifi_info.type = "WDS"
        self.assertEqual(WlanType.wds, wifi_info.type)
        wifi_info.type = "mesh"
        self.assertEqual(WlanType.mesh, wifi_info.type)

