from unittest import TestCase

from server.router import Router
from util.router_reboot import RouterReboot


class TestRouterReboot(TestCase):

    def test_reboot_into_config(self):
        # Create router
        router = Router(1, "vlan1", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)
        RouterReboot().configmode(router)

    '''
    def test_reboot_into_normal(self):
        # Create router
        router = Router(1, "vlan1", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)
        RouterReboot().normal(router)
    '''
TestRouterReboot().test_reboot_into_config()