import unittest

from server.router import Router
from server.router import WlanMode


class MyTestCase(unittest.TestCase):
    def test_create_Router(self):
        router = Router(1, "vlan1", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        assert isinstance(router, Router)

        assert router.ip == "192.168.0.99"
        assert router.ip_mask == 43

    def test_add_information(self):
        router = Router(1, "vlan1", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)

        router.ssid = "lol funk"
        router.wlan_mode = WlanMode.master


if __name__ == '__main__':
    unittest.main()
