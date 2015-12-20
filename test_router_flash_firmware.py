from util.router_flash_firmware import RouterFlashFirmware
from server.router import Router
from config.configmanager import ConfigManager

 # Create router
router = Router(1, "vlan20", 20, "192.168.2.13", 24, "bananapi", "bananapi", 1)
router.model = "TP-LINK TL-WR841N/ND v9"
router.mac = "e8:de:27:b7:7c:e2"
# Create firware configuration
firmware_config = ConfigManager.get_firmware_list()

RouterFlashFirmware.sysupdate(router, firmware_config)
RouterFlashFirmware.sysupgrade(router, n=True)