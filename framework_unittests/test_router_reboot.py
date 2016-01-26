from unittest import TestCase

from server.router import Router
from util.router_reboot import RouterReboot
from server.router import Mode
from network.nv_assist import NVAssistent


class TestRouterReboot(TestCase):

    def test_reboot_into_config(self):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        router.mode = Mode.normal
        assert isinstance(router, Router)
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan_veth(router)
        router_reboot = RouterReboot(router, configmode=True)
        router_reboot.start()
        router_reboot.join()
        assert router.mode == Mode.configuration
        nv_assist.close()
    '''
    def test_reboot_into_normal(self):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        router.mode = Mode.configuration
        assert isinstance(router, Router)
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan_veth(router)
        router_reboot = RouterReboot(router, configmode=False)
        router_reboot.start()
        router_reboot.join()
        assert router.mode == Mode.normal
        nv_assist.close()
    '''