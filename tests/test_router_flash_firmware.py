from util.router_flash_firmware import RouterFlashFirmware
from server.router import Router
from config.configmanager import ConfigManager
from server.router import Mode

# Create router
router = Router(1, "vlan1", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
router.model = "TP-LINK TL-WR841N/ND v9"
router.mac = "e8:de:27:b7:7c:e2"
router.mode = Mode.configuration
# Create firware configuration
firmware_config = ConfigManager.get_firmware_dict()[0]

RouterFlashFirmware.sysupdate(router, firmware_config)
RouterFlashFirmware.sysupgrade(router, n=True)
