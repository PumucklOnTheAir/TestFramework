from unittest import TestCase
from router.router import Router, Mode
from pyroute2 import netns
from network.nv_assist import NVAssistent
from util.router_online import RouterOnline


class TestRouterOnline(TestCase):
    """
    This TestModule tests the functionality of RouterOnline.
    """""

    def test_router_online(self):
        print("Test if the Router is reachable")
        router = self._create_router()
        # NVAssisten
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan(router)
        # Set netns for the current process
        netns.setns(router.namespace_name)

        print("Send a Ping to the two static IP-addresses ...")
        router_online = RouterOnline(router)
        router_online.start()
        router_online.join()

        print("Router is online with IP " + router.ip + "/" + str(router.ip_mask))

        self.assertEqual(router.mode, Mode.configuration, "The Configuration Mode is not correct")

        # Close Namespaces and VLANs
        nv_assist.close()

    def _create_router(self):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)
        return router
