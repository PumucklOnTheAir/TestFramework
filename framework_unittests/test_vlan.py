from unittest import TestCase
from network.vlan import Vlan
from subprocess import Popen, PIPE
from log.logger import Logger
from pyroute2.ipdb import IPDB


class TestVlan(TestCase):

    def test_create_vlan(self):
        Logger().debug("TestVlan: test_create_vlan ...")
        # Create VLAN
        ipdb = IPDB()
        vlan = Vlan(ipdb, 'eth0', 'vlan21', 21)
        vlan.create_interface("192.168.1.11", 24)
        assert isinstance(vlan, Vlan)

        # Test if the VLAN now exists
        process = Popen(["ip", "link", "show", "dev", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert sterr.decode('utf-8') == ""
        assert vlan.vlan_iface_name in stdout.decode('utf-8')

        # Remove the VLAN
        vlan.delete_interface(close_ipdb=True)
        process = Popen(["ip", "link", "show", "dev", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout.decode('utf-8') == ""

    def test_create_existing_vlan(self):
        Logger().debug("TestVlan: test_create_existing_vlan ...")
        # Create VLAN 1
        ipdb = IPDB()
        vlan = Vlan(ipdb, 'eth0', 'vlan21', 21)
        vlan.create_interface("192.168.1.11", 24)
        assert isinstance(vlan, Vlan)
        # Create VLAN 2
        vlan = Vlan(ipdb, 'eth0', 'vlan21', 21)
        vlan.create_interface("192.168.1.11", 24)
        assert isinstance(vlan, Vlan)

        # Test if the VLAN now exists
        process = Popen(["ip", "link", "show", "dev", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert sterr.decode('utf-8') == ""
        assert vlan.vlan_iface_name in stdout.decode('utf-8')

        # Remove the VLAN
        vlan.delete_interface(close_ipdb=True)
        process = Popen(["ip", "link", "show", "dev", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout.decode('utf-8') == ""

    def test_create_vlan_with_existing_name(self):
        Logger().debug("TestVlan: test_create_vlan_with_existing_name ...")
        # Create VLAN 1
        ipdb = IPDB()
        vlan = Vlan(ipdb, 'eth0', 'vlan21', 21)
        vlan.create_interface("192.168.1.11", 24)
        assert isinstance(vlan, Vlan)
        # Create VLAN 2
        ipdb = IPDB()
        vlan = Vlan(ipdb, 'eth0', 'vlan21', 22)
        vlan.create_interface("192.168.1.11", 24)
        assert isinstance(vlan, Vlan)

        # Test if the VLAN now exists
        process = Popen(["ip", "link", "show", "dev", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert sterr.decode('utf-8') == ""
        assert vlan.vlan_iface_name in stdout.decode('utf-8')

        # Remove the VLAN
        vlan.delete_interface(close_ipdb=True)
        process = Popen(["ip", "link", "show", "dev", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout.decode('utf-8') == ""
