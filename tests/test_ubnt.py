import unittest
from util.ubnt import Ubnt


class MyTestCase(unittest.TestCase):
    def test_create_power_strip(self):
        global ps
        ps = Ubnt("vlan20", 20, "192.168.1.20", 24, "test", "test")
        assert isinstance(ps, Ubnt)

        assert ps.ip == "192.168.1.20"
        assert ps.usr_name == "test"
        assert ps.usr_password == "test"
        assert ps.ip_mask == 24
        assert ps.vlan_iface_name == "vlan20"
        assert ps.vlan_iface_id == 20

    def test_power(self):
        """ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ps.ip, port=22, username=ps.usr_name, password=ps.usr_password)
        ps.up(1)"""

if __name__ == '__main__':
    unittest.main()
