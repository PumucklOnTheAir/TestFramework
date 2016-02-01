from unittest import TestCase

from router.router import Router, Mode
from util.router_reboot import RouterReboot
from network.nv_assist import NVAssistent
from log.logger import Logger
import time


class TestRouterReboot(TestCase):

    def test_reboot(self):
        router = self._create_router()
        self._reboot_into_config(router)
        Logger().debug("Wait 1min till the Router has rebooted.")
        time.sleep(60)
        self._reboot_into_normal(router)

    def _reboot_into_config(self, router: Router):
        Logger().debug("Reboot Router into configmode...")
        # Create NVAssistent
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan(router)

        # Reboot Router into configmode
        router_reboot = RouterReboot(router, configmode=True)
        router_reboot.start()
        router_reboot.join()
        assert router.mode == Mode.configuration
        nv_assist.close()

    def _reboot_into_normal(self, router: Router):
        Logger().debug("Reboot Router back into normalmode...")
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan(router)
        router_reboot = RouterReboot(router, configmode=False)
        router_reboot.start()
        router_reboot.join()
        assert router.mode == Mode.normal
        nv_assist.close()

    def _create_router(self):
        # Create router
        router = Router(1, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.normal
        assert isinstance(router, Router)
        return router
