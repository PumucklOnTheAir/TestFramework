from unittest import TestCase
from network.vlan import Vlan
from subprocess import Popen, PIPE
from pyroute2.ipdb import IPDB
from router.router import Router, Mode


class TestVlan(TestCase):

    def test_create_vlan(self):
        router = self._create_router()
        # Create VLAN
        ipdb = IPDB()
        vlan = Vlan(ipdb, router, "eth0")
        vlan.create_interface()
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

    def _create_router(self):
        # Create router
        router = Router(1, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.normal
        assert isinstance(router, Router)
        return router
