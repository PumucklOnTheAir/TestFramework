from unittest import TestCase
from firmware.firmware_handler import FirmwareHandler
from firmware.firmware import Firmware
from router.router import Router
import logging


class TestFirmwareHandler(TestCase):

    def test_get_single_firmware(self):
        """
        Downloads a single firmware-image.
        """
        logging.debug("Test FirmwareHandler: get_single_firmware ...")
        # Create router
        router = Router(1, "vlan1", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
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

    def test_import_firmware(self):
        """
        Try's to get the firmware-image two times. At least the second try the firmware should be stored on the device
        and imported.
        """
        logging.debug("Test FirmwareHandler: import_firmware ...")
        # Create router
        router = Router(1, "vlan1", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)

        # Create firmware_handler
        release_model = "stable"
        url = "https://firmware.darmstadt.freifunk.net"
        download_all = False
        firmware_handler = FirmwareHandler(url)
        assert isinstance(firmware_handler, FirmwareHandler)

        # Downlaods the firmware-image
        firmware_handler.download_firmware(router.model, release_model)

        # Imports the firmware-image from the local storage
        firmware = firmware_handler.get_firmware(router.model, release_model, download_all)
        assert isinstance(firmware, Firmware)
        assert firmware.name == "gluon-ffda-0.7.3-tp-link-tl-wr841n-nd-v9-sysupgrade.bin"
        assert firmware.version == "0.7.3"
        assert firmware.freifunk_verein == "ffda"
        assert firmware.release_model == "stable"
        assert firmware.file == (firmware_handler.FIRMWARE_PATH +
                                 '/stable/sysupgrade/gluon-ffda-0.7.3-tp-link-tl-wr841n-nd-v9-sysupgrade.bin')

    def test_check_hash_firmware(self):
        """
        Downloads a single firmware-image.
        """
        logging.debug("Test FirmwareHandler: check_hash_firmware ...")
        # Create router
        router = Router(1, "vlan1", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)

        # Create firmware_handler
        release_model = "stable"
        url = "https://firmware.darmstadt.freifunk.net"
        download_all = False
        firmware_handler = FirmwareHandler(url)
        assert isinstance(firmware_handler, FirmwareHandler)

        # Imports the Firmware if already existing or downloads it
        firmware = firmware_handler.get_firmware(router.model, release_model, download_all)
        assert isinstance(firmware, Firmware)

        incorrect_hash = "2b83a03e961f2e0a7fe1817e86e9caf248fbe440d12acda5a5c78de8a7d4f25ec48282cb8562d4b3b5e3c0"
        assert not firmware.check_hash(incorrect_hash)

        assert firmware.check_hash(firmware.hash)
