from unittest import TestCase
from util.router_flash_firmware import Sysupdate, Sysupgrade
from router.router import Router, Mode
from config.configmanager import ConfigManager
from network.nv_assist import NVAssistent
from pyroute2 import netns


class TestRouterFlashFirmware(TestCase):
    """
    This TestModule tests functionality of the Systemupdate and Systemupgrade

        1. Create Router (Mode: configuration)
        2. Creates the firmware configuration
        3. Systemupdate
        4. Create NVAssistent
        5. Systemupgrade
    """""

    def test_flash_firmware(self):
        router = self._create_router()

        # Create firware configuration
        firmware_config = ConfigManager.get_firmware_dict()[0]

        # Download firmare-image from UpdateServer
        sysupdate = Sysupdate(router, firmware_config)
        sysupdate.start()
        sysupdate.join()

        # NVAssisten
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan(router)
        # Set netns for the current process
        netns.setns(router.namespace_name)
        # The IP where the Router can download the firmware image (should be the frameworks IP)
        web_server_ip = nv_assist.get_ip_address(router.namespace_name, router.vlan_iface_name)[0]

        try:
            # Copy firmware-image to the Router (/tmp/image)
            sysupgrade = Sysupgrade(router, n=True, web_server_ip=web_server_ip, debug=True)
            sysupgrade.start()
            sysupgrade.join()
        except Exception:
            raise
        finally:
            nv_assist.close()

    def _create_router(self):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.configuration
        assert isinstance(router, Router)
        return router
