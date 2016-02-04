from unittest import TestCase
from router.ip_address import IPv4, IPv6

# TODO Kann eigentlich gelöscht werden
class TestIPAddress(TestCase):

    def test_ipv4(self):
        ipv4 = IPv4("192.168.1.1", 24)
        assert isinstance(ipv4, IPv4)
        self.assertEqual("192.168.1.1", ipv4.ip)
        self.assertEqual(24, ipv4.mask)

    def test_ipv6(self):
        ipv6 = IPv6("fe80::a11:96ff:fe05:3024", 64)
        assert isinstance(ipv6, IPv6)
        self.assertEqual("fe80::a11:96ff:fe05:3024", ipv6.ip)
        self.assertEqual(64, ipv6.prefix_len)
