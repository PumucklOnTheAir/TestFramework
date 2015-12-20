from unittest import TestCase
from network.vlan import Vlan
from subprocess import Popen, PIPE
from log.logger import Logger


class TestVlan(TestCase):

    def test_create_vlan(self):
        Logger().debug("TestVlan: test_create_vlan ...")
        # Create VLAN
        vlan = Vlan('eth0', 'vlan1', 10, '192.168.1.10', 24)
        vlan.create_interface("192.168.1.11", 24)
        assert isinstance(vlan, Vlan)

        # Test if the VLAN now exists
        process = Popen(["ifconfig", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert sterr.decode('utf-8') == ""
        assert vlan.vlan_iface_name in stdout.decode('utf-8')

        # Remove the VLAN
        vlan.delete_interface()
        process = Popen(["ifconfig", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout.decode('utf-8') == ""

    def test_create_existing_vlan(self):
        Logger().debug("TestVlan: test_create_existing_vlan ...")
        # Create VLAN 1
        vlan = Vlan('eth0', 'vlan1', 10, '192.168.1.10', 24)
        vlan.create_interface("192.168.1.11", 24)
        assert isinstance(vlan, Vlan)
        # Create VLAN 2
        vlan = Vlan('eth0', 'vlan1', 10, '192.168.1.10', 24)
        vlan.create_interface("192.168.1.11", 24)
        assert isinstance(vlan, Vlan)

        # Test if the VLAN now exists
        process = Popen(["ifconfig", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert sterr.decode('utf-8') == ""
        assert vlan.vlan_iface_name in stdout.decode('utf-8')

        # Remove the VLAN
        vlan.delete_interface()
        process = Popen(["ifconfig", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout.decode('utf-8') == ""

    def test_create_vlan_with_existing_name(self):
        Logger().debug("TestVlan: test_create_vlan_with_existing_name ...")
        # Create VLAN 1
        vlan = Vlan('eth0', 'vlan1', 10, '192.168.1.10', 24)
        vlan.create_interface("192.168.1.11", 24)
        assert isinstance(vlan, Vlan)
        # Create VLAN 2
        vlan = Vlan('eth0', 'vlan1', 11, '192.168.1.10', 24)
        vlan.create_interface("192.168.1.11", 24)
        assert isinstance(vlan, Vlan)

        # Test if the VLAN now exists
        process = Popen(["ifconfig", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert sterr.decode('utf-8') == ""
        assert vlan.vlan_iface_name in stdout.decode('utf-8')

        # Remove the VLAN
        vlan.delete_interface()
        process = Popen(["ifconfig", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout.decode('utf-8') == ""

    def test_create_vlan_with_existing_id(self):
        Logger().debug("TestVlan: test_create_vlan_with_existing_id ...")
        # Create VLAN 1
        vlan1 = Vlan('eth0', 'vlan1', 10, '192.168.1.10', 24)
        assert isinstance(vlan1, Vlan)
        vlan1.create_interface("192.168.1.11", 24)

        # Create VLAN 2
        vlan2 = Vlan('eth0', 'vlan2', 10, '192.168.1.10', 24)
        assert isinstance(vlan2, Vlan)
        vlan2.create_interface("192.168.1.11", 24)

        # Test if the VLAN now exists
        process = Popen(["ifconfig", vlan2.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert sterr.decode('utf-8') != ""

        # Remove the VLAN
        vlan2.delete_interface()
        process = Popen(["ifconfig", vlan2.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout.decode('utf-8') == ""

        # Remove the VLAN
        vlan1.delete_interface()
        process = Popen(["ifconfig", vlan1.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout.decode('utf-8') == ""