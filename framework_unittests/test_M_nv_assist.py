from unittest import TestCase
from network.nv_assist import NVAssistent
from router.router import Router, Mode
from subprocess import Popen, PIPE


class TestNVAssist(TestCase):
    """
    This TestModule tests the functionality of the NV_Assistent.

        1. Create Router (Mode: normal)
        2. Try to create a nv_assistent
            - create vlan
            - create namespace
            - encapsulate vlan in namespace
    """""

    def test_create_namespace_vlan_veth(self):
        router = self._create_router()

        print("Test NVAssistent ...")
        for i in range(0, 2):
            print("Test" + str(i))
            nv_assi = NVAssistent("eth0")
            assert isinstance(nv_assi, NVAssistent)
            nv_assi.create_namespace_vlan(router)

            # Test if the Namespace now exists
            process = Popen(["ip", "netns"], stdout=PIPE, stderr=PIPE)
            stdout, sterr = process.communicate()
            assert sterr.decode('utf-8') == ""
            assert router.namespace_name in stdout.decode('utf-8')

            # Test if the VLAN now in Namespace exists
            process = Popen(["ip", "netns", "exec", router.namespace_name,
                             "ip", "link", "show", "dev", router.vlan_iface_name], stdout=PIPE, stderr=PIPE)
            stdout, sterr = process.communicate()
            assert sterr.decode('utf-8') == ""
            assert router.vlan_iface_name in stdout.decode('utf-8')

            nv_assi.close()

    def _create_router(self):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.configuration
        assert isinstance(router, Router)
        return router
