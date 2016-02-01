from unittest import TestCase
from router.router import Router, Mode
from util.router_info import RouterInfo


class TestRouterInfo(TestCase):

    def test_router_info(self):
        # Create router
        router = Router(1, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        router.mode = Mode.normal

        RouterInfo.update(router)
