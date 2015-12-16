from unittest import TestCase
from network.vlan import Vlan
from subprocess import Popen, PIPE


class TestVlan(TestCase):
    def test_create_vlan(self):
        # Create VLAN
        vlan = Vlan('eth0', 'vlan1', 10, '192.168.1.10', 24)
        assert isinstance(vlan, Vlan)

        # Test if the VLAN now exists
        process = Popen(["ifconfig", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert sterr == ""
        assert vlan.vlan_iface_name in stdout

        # Remove the VLAN
        vlan.delete_interface()
        process = Popen(["ifconfig", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout == ""