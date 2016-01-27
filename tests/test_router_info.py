from unittest import TestCase
from router.router import Router, Mode
from network.nv_assist import NVAssistent
from util.router_info import RouterInfo
import os


class TestRouterInfo(TestCase):

    def test_router_info(self):
        # Create router
        # 10.223.254.254/16
        router = Router(1, "vlan1", 21, "192.168.2.13", 24, "192.168.1.1", 24, "bananapi", "bananapi", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        router.mode = Mode.normal

        router_info = RouterInfo(router)
        router_info.start()
        router_info.join()
