import unittest

from router.router import Router, WlanMode, Mode


class MyTestCase(unittest.TestCase):
    def test_create_Router(self):
        router = Router(1, "vlan1", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.mode = Mode.normal
        assert isinstance(router, Router)

        assert router.ip == "10.223.254.254"
        assert router.ip_mask == 16

    def test_add_information(self):
        router = Router(1, "vlan1", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)

        router.ssid = "lol funk"
        router.wlan_mode = WlanMode.master

        assert router.ssid == "lol funk"
        assert router.wlan_mode == WlanMode.master


if __name__ == '__main__':
    unittest.main()
