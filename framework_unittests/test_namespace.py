from unittest import TestCase
from network.vlan import Vlan
from network.namespace import Namespace
from subprocess import Popen, PIPE
from pyroute2.ipdb import IPDB
from router.router import Router, Mode


class TestNamespace(TestCase):
    """
    This TestModule tests the configuration of the Namespaces.

        1. Create Router (Mode: normal)
        2. Create VLAN
        3. Encapsulate VLAN inside the Namespace
        4. Remove Namespace and VLAN
    """""

    def test_create_namespace(self):
        router = self._create_router()

        # Create VLAN
        ipdb = IPDB()
        vlan = Vlan(ipdb, router, "eth0")
        assert isinstance(vlan, Vlan)
        vlan.create_interface()

        # Create Namespace
        namespace = Namespace(ipdb,router.namespace_name)
        assert isinstance(namespace, Namespace)

        # encapsulate VLAN
        namespace.encapsulate_interface(vlan.vlan_iface_name)

        # Test if the namespace now exists
        process = Popen(["ip", "netns"], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert sterr.decode('utf-8') == ""
        assert namespace.nsp_name in stdout.decode('utf-8')

        # Remove the Namespace
        vlan.delete_interface(close_ipdb=True)
        namespace.remove()
        ipdb.release()
        process = Popen(["ip", "netns"], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout.decode('utf-8') == ""

    def _create_router(self):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.normal
        assert isinstance(router, Router)
        return router
