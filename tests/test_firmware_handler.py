from unittest import TestCase
from firmware.firmware_handler import FirmwareHandler
from firmware.firmware import ReleaseModel, Firmware, UpdateType
from server.router import Router


class TestFirmwareHandler(TestCase):
    def test_get_firmware(self):
        # Create router
        router = Router("vlan21", 21, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)

        # Create firmware_handler
        release_model = ReleaseModel.stable
        url = "https://firmware.darmstadt.freifunk.net"
        firmware_handler = FirmwareHandler(release_model, url)
        assert isinstance(firmware_handler, FirmwareHandler)

        firmware = firmware_handler.get_firmware(UpdateType.factory, router.model, "ffda", "0.7.3")
        assert isinstance(firmware, Firmware)
        assert firmware.name == "gluon-ffda-0.7.3-tp-link-tl-wr841n-nd-v9.bin"
        assert firmware.version == "0.7.3"
        assert firmware.freifunk_verein == "ffda"
        assert firmware.release_model == ReleaseModel.stable
        assert firmware.update_type == UpdateType.factory
        assert firmware.file == 'firmwares/stable/factory/gluon-ffda-0.7.3-tp-link-tl-wr841n-nd-v9.bin'

    def test_get_firmware_sysupgrade(self):
        # Create router
        router = Router("vlan21", 21, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)

        # Create firmware_handler
        release_model = ReleaseModel.stable
        url = "https://firmware.darmstadt.freifunk.net"
        firmware_handler = FirmwareHandler(release_model, url)
        assert isinstance(firmware_handler, FirmwareHandler)

        firmware = firmware_handler.get_firmware(UpdateType.sysupgrade, router.model, "ffda", "0.7.3")
        assert isinstance(firmware, Firmware)
        assert firmware.name == "gluon-ffda-0.7.3-tp-link-tl-wr841n-nd-v9-sysupgrade.bin"
        assert firmware.release_model == ReleaseModel.stable
        assert firmware.update_type == UpdateType.sysupgrade
        assert firmware.file == 'firmwares/stable/sysupgrade/gluon-ffda-0.7.3-tp-link-tl-wr841n-nd-v9-sysupgrade.bin'

