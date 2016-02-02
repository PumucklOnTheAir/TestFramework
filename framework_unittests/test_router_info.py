from unittest import TestCase
from router.router import Router, Mode
from util.router_info import RouterInfo


class TestRouterInfo(TestCase):

    def test_router_info(self):
        router = self._create_router()

        router_info = RouterInfo(router)
        router_info.start()
        router_info.join()

    def _create_router(self):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.normal
        assert isinstance(router, Router)
        return router
