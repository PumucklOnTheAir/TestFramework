from unittest import TestCase
from util.router_flash_firmware import Sysupdate, Sysupgrade
from router.router import Router, Mode
from config.configmanager import ConfigManager


class TestRouterFlashFirmware(TestCase):

    def test_flash_firmware(self):
        router = self._create_router()
        # Create firware configuration
        firmware_config = ConfigManager.get_firmware_dict()[0]

        sysupdate = Sysupdate(router, firmware_config)
        sysupdate.start()
        sysupdate.join()

        sysupgrade = Sysupgrade(router, n=True, debug=True)
        sysupgrade.start()
        sysupgrade.join()


    def _create_router(self):
        # Create router
        router = Router(1, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.normal
        assert isinstance(router, Router)
        return router