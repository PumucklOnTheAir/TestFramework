from unittest import TestCase
from network.vlan import Vlan
from network.namespace import Namespace
from subprocess import Popen, PIPE


class TestNamespace(TestCase):

    def test_create_namespace(self):
        # Create VLAN
        vlan = Vlan('eth0', 'vlan1', 10, '192.168.1.10', 24)
        assert isinstance(vlan, Vlan)

        # Create Namespace
        namespace = Namespace('nsp1', vlan.vlan_iface_name, vlan.ipdb)
        assert isinstance(namespace, Namespace)

        # Test if the namespace now exists
        process = Popen(["ip", "netns"], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert sterr == ""
        assert namespace.nsp_name in stdout

        # Test if the vlan is encapsulate inside the namspace
        assert isinstance(vlan, Vlan)
        process = Popen(["ifconfig", vlan.vlan_iface_name], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout == ""

        # Remove the Namespace
        namespace.remove()
        process = Popen(["ip", "netns"], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout == ""