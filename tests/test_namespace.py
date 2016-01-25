from unittest import TestCase
from network.vlan import Vlan
from network.namespace import Namespace
from subprocess import Popen, PIPE
from log.logger import Logger


class TestNamespace(TestCase):

    def test_create_namespace(self):
        Logger().debug("TestNamespace: test_create_namespace ...")
        # Create VLAN
        vlan = Vlan('eth0', 'vlan1', 10, '192.168.1.10', 24)
        assert isinstance(vlan, Vlan)
        vlan.create_interface("192.168.1.11", 24)

        # Create Namespace
        namespace = Namespace('nsp1', vlan.ipdb)
        assert isinstance(namespace, Namespace)

        #encapsulate VLAN
        namespace.encapsulate_interface(vlan.vlan_iface_name)

        # Test if the namespace now exists
        process = Popen(["ip", "netns"], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert sterr.decode('utf-8') == ""
        assert namespace.nsp_name in stdout.decode('utf-8')

        # Remove the Namespace
        namespace.remove()
        process = Popen(["ip", "netns"], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout.decode('utf-8') == ""
