from unittest import TestCase
from firmware.firmware import Firmware


class TestFirmware(TestCase):

    def test_create_Firmware(self):
        firmware_name = "gluon-ffda-0.7.3-tp-link-tl-wr841n-nd-v9-sysupgrade.bin"
        url = "https://firmware.darmstadt.freifunk.net"
        firmware = Firmware(firmware_name, "0.7.3", "ffda", "stable", "/folder/folder/file", url)
        assert isinstance(firmware, Firmware)

        self.assertEqual(firmware_name, firmware.name)
        self.assertEqual("0.7.3", firmware.version)
        self.assertEqual("ffda", firmware.freifunk_verein)
        self.assertEqual("stable", firmware.release_model)
        self.assertEqual("/folder/folder/file", firmware.file)
        self.assertEqual(url, firmware.url)

    def test_setter(self):
        firmware_name = "gluon-ffda-0.7.3-tp-link-tl-wr841n-nd-v9-sysupgrade.bin"
        url = "https://firmware.darmstadt.freifunk.net"
        firmware = Firmware("", "", "", "", "", "")
        assert isinstance(firmware, Firmware)

        firmware.name = firmware_name
        firmware.version = "0.7.3"
        firmware.freifunk_verein = "ffda"
        firmware.release_model = "stable"
        firmware.file = "/folder/folder/file"
        firmware.url = url

        self.assertEqual(firmware_name, firmware.name)
        self.assertEqual("0.7.3", firmware.version)
        self.assertEqual("ffda", firmware.freifunk_verein)
        self.assertEqual("stable", firmware.release_model)
        self.assertEqual("/folder/folder/file", firmware.file)
        self.assertEqual(url, firmware.url)
