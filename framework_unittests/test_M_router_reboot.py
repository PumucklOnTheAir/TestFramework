from unittest import TestCase
from pyroute2 import netns
from router.router import Router, Mode
from util.router_reboot import RouterReboot
from network.nv_assist import NVAssistent
from multiprocessing import Process, Queue
import logging


class TestRouterReboot(TestCase):
    """
    This TestModule tests the reboot functionality.

        1. Create Router (Mode: normal)
        2. Reboot the Router into configuration mode (this is done in another process, cause of namespaces).
        3. Wait until the Router is rebooted
        4. Reboot the Router back into normal mode (this is done in another process, cause of namespaces).
    """""

    def test_reboot(self):
        logging.basicConfig(level=10)
        print("Test the 'reboot'-function")
        router = self._create_router()
        q = Queue()
        """ Falls auskommentiert => Server mode auf 'normal' stellen
        # Reboot Router, in an own thread, into configmode
        p = Process(target=self._reboot_into_config, args=(router, q,))
        p.start()
        print("Wait till the Router has rebooted ...")
        # Get result from process
        router = q.get()
        p.join()

        print("Router Mode: " + str(router.mode))
        """
        # Reboot Router, in an own thread, into normalmode
        p = Process(target=self._reboot_into_normal, args=(router, q,))
        p.start()
        # Get result from process
        router = q.get()
        p.join()
        print("Router Mode: " + str(router.mode))

    def _reboot_into_config(self, router: Router, q: Queue):
        print("Reboot Router into configmode ...")
        # Create NVAssistent
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan(router)
        # Set netns for the current process
        netns.setns(router.namespace_name)

        # Reboot Router into configmode
        try:
            router_reboot = RouterReboot(router, configmode=True)
            router_reboot.start()
            router_reboot.join()
        except Exception as e:
            nv_assist.close()
            raise e
        assert router.mode == Mode.configuration
        nv_assist.close()
        q.put(router)

    def _reboot_into_normal(self, router: Router, q: Queue):
        print("Reboot Router back into normalmode ...")
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan(router)
        # Set netns for the current process
        netns.setns(router.namespace_name)
        try:
            router_reboot = RouterReboot(router, configmode=False)
            router_reboot.start()
            router_reboot.join()
        except Exception as e:
            nv_assist.close()
            raise e
        assert router.mode == Mode.normal
        nv_assist.close()
        q.put(router)

    def _create_router(self) -> Router:
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.configuration
        assert isinstance(router, Router)
        return router
