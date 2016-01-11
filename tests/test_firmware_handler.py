from unittest import TestCase
from firmware.firmware_handler import FirmwareHandler
from firmware.firmware import Firmware
from server.router import Router


class TestFirmwareHandler(TestCase):

    def test_get_signle_firmware(self):
        # Create router
        router = Router(0, "vlan20", 20, "192.168.2.13", 24, "bananapi", "bananapi", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)

        # Create firmware_handler
        release_model = "stable"
        url = "https://firmware.darmstadt.freifunk.net"
        download_all = False
        firmware_handler = FirmwareHandler(url)
        assert isinstance(firmware_handler, FirmwareHandler)

        # Imports the Firmware if already existing or downlaods it
        firmware = firmware_handler.get_firmware(router.model, release_model, download_all)
        assert isinstance(firmware, Firmware)
        assert firmware.name == "gluon-ffda-0.7.3-tp-link-tl-wr841n-nd-v9-sysupgrade.bin"
        assert firmware.version == "0.7.3"
        assert firmware.freifunk_verein == "ffda"
        assert firmware.release_model == "stable"
        assert firmware.file == (firmware_handler.FIRMWARE_PATH +
                                 '/stable/sysupgrade/gluon-ffda-0.7.3-tp-link-tl-wr841n-nd-v9-sysupgrade.bin')
