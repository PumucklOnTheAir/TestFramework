from unittest import TestCase
from network.nv_assist import NVAssistent
from router.router import Router, Mode


class TestNVAssist(TestCase):

    def test_create_namespace_vlan_veth(self):
        router = self._create_router()

        for i in range(0, 2):
            print("Test" + str(i) + ":")
            nv_assi = NVAssistent("eth0")
            assert isinstance(nv_assi, NVAssistent)
            nv_assi.create_namespace_vlan(router)
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
