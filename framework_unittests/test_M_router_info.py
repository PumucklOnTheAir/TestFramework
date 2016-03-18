from unittest import TestCase
from router.router import Router, Mode
from util.router_info import RouterInfo
from network.nv_assist import NVAssistent
from pyroute2 import netns


class TestRouterInfo(TestCase):
    """
    This TestModule tests the functionality of the RouterInfo.
    """""

    def test_router_info(self):
        print("Test Router_Info")
        router = self._create_router()

        # NVAssisten
        nv_assist = NVAssistent("enp0s25")
        try:
            nv_assist.create_namespace_vlan(router)
            # Set netns for the current process
            netns.setns(router.namespace_name)

            print("Get informations via ssh-commands ...")
            router_info = RouterInfo(router)
            router_info.start()
            router_info.join()

            print(str(router))
        finally:
            # Close Namespaces and VLANs
            nv_assist.close()

    def _create_router(self):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.normal
        assert isinstance(router, Router)
        return router
