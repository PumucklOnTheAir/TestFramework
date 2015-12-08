import unittest

from server.router import Router
from server.router import Mode


class MyTestCase(unittest.TestCase):
    def test_create_Router(self):
        r1 = Router("VLAN Name1", 42, "192.168.0.99", 43, "admin", "pwd", 1)
        assert isinstance(r1, Router)

        assert r1.ip == "192.168.0.99"
        assert r1.ip_mask == 43

    def test_add_information(self):
        r2 = Router("VLAN Name2", 43, "192.168.0.99", 44, "admin2", "pwd2", 2)

        r2.usr_name = "adminX"
        r2.usr_password = "pwdY"
        r2.ssid = "lol funk"
        r2.wlan_mode = Mode.master


if __name__ == '__main__':
    unittest.main()
