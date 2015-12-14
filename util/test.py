from util.router_flash_firmware import RouterFlashFirmware
from server.router import Router
from firmware.firmware import ReleaseModel, UpdateType

 # Create router
router = Router("vlan21", 21, "192.168.1.1", 24, "root", "root", 1)
router.model = "TP-LINK TL-WR841N/ND v9"
router.mac = "e8:de:27:b7:7c:e2"
# Create firware configuration
url = "https://firmware.darmstadt.freifunk.net"
release_model = ReleaseModel.stable
update_type = UpdateType.sysupgrade
freifunk_verein = "ffda"
firmware_version = "0.7.3"

RouterFlashFirmware.configuration([router],[url,release_model,update_type,freifunk_verein,firmware_version])
RouterFlashFirmware.sysupgrade([router], n=True)