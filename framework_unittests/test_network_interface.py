from unittest import TestCase
from router.ip_address import IPv4, IPv6
from router.network_interface import NetworkInterface, Status


class TestNetworkInterface(TestCase):
    def test_create_network_interface(self):
        network_interface = NetworkInterface("eth0")
        assert isinstance(network_interface, NetworkInterface)
        self.assertEqual(Status.unknown, network_interface.status)

        network_interface.mac = "d8:31:26:45:56:2f"

        ipv4 = IPv4("192.168.1.1", 24)
        network_interface.ipv4_lst.append(ipv4)

        ipv6 = IPv6("fe80::a11:96ff:fe05:3024", 64)
        network_interface.ipv6_lst.append(ipv6)

        network_interface.status = Status.up

        self.assertEqual("eth0", network_interface.name)
        self.assertEqual("d8:31:26:45:56:2f", network_interface.mac)
        self.assertEqual(Status.up, network_interface.status)
        self.assertEqual(ipv4, network_interface.ipv4_lst[0])
        self.assertEqual(ipv6, network_interface.ipv6_lst[0])

        ipv4 = IPv4("192.168.1.1", 24)
        assert isinstance(ipv4, IPv4)
        self.assertEqual("192.168.1.1", ipv4.ip)
        self.assertEqual(24, ipv4.mask)
