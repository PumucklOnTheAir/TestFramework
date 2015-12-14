import urllib.request
import re
import os
import errno
from firmware.firmware import Firmware, ReleaseModel, UpdateType
from typing import List
from log.logger import Logger


class FirmwareHandler:

    FIRMWARE_FILE = "firmwares"

    def __init__(self, release_model: ReleaseModel, url: str):
        """
        :param release_model: stable, beta, experimental
        :param url: alike "https://firmware.darmstadt.freifunk.net"
        :return:
        """
        self.url = url
        self.release_model = release_model

    def get_firmware(self, update_type: UpdateType, router_model: str, freifunk_verein: str, firmware_version: str) \
            -> Firmware:
        """
        Downloads and saves the firmware(sysupgrade), then returns a firmware-object.
        It is posible to chose between three different firmware sources (automatically, manifest, url).
        :param update_type: factory, sysupgrade
        :param router_model: alike "TP-LINK TL-WR841N/ND v9"
        :param freifunk_verein: alike "ffda"
        :param firmware_version: alike "0.7.3"
        :return: Firmware
        """
        firmware = None
        valid_download = False
        while not valid_download:
            Logger().info("Get firmware ", 1)
            Logger().info("[1] automatically", 1)
            Logger().info("[2] from the manifest", 1)
            Logger().info("[3] via URL", 1)
            val = 1 # TODO int(input("Select number: "))
            Logger().info("<== " + str(val), 1)
            if val == 1:
                firmware = self._get_firmware_info_auto(update_type, router_model, freifunk_verein, firmware_version)
            elif val == 2:
                firmware, hash = self._get_firmware_info_manifest(update_type)
                if not firmware.check_hash(hash):
                    valid_download = False
                    continue
            elif val == 3:
                firmware = self._get_firmware_info_manually()
                if not self._verify_release_model(firmware.release_model):
                    valid_download = False
                    continue
            else:
                valid_download = False
                continue
            valid_download = self._download_firmware(firmware.url, firmware.file, firmware.update_type)
        return firmware


    def _get_firmware_info_auto(self, update_type: UpdateType, router_model: str, freifunk_verein: str, firmware_version: str) -> Firmware:
        """
        Creates a firmware, with the url and the save-file.
        The firmware url is automatically determined.
        :param update_type: factory, sysupgrade
        :param router_model: alike "TP-LINK TL-WR841N/ND v9"
        :param freifunk_verein: alike "ffda"
        :param firmware_version: alike "0.7.3"
        :return: Firmware
        """
        Logger().debug("The firmware url will be automatically determined ...", 2)
        router_model_name, router_model_version = self._parse_router_model(router_model)
        tmp = "-sysupgrade.bin" if (update_type.name == "sysupgrade") else ".bin"
        firmware_name = 'gluon-'+freifunk_verein+'-'+firmware_version+'-' + router_model_name + '-' \
                        + router_model_version+tmp
        file = self.FIRMWARE_FILE + '/' + self.release_model.name + '/' + update_type.name + '/' + firmware_name
        url = self.url + '/' + self.release_model.name + '/' + update_type.name + '/' + firmware_name
        return Firmware(firmware_name, firmware_version, freifunk_verein, self.release_model, update_type, file, url)

    def _get_firmware_info_manifest(self, update_type: UpdateType):
        """
        Creates a firmware, with the url and the save-file.
        The User can chose a firmware from the manifest.
        :param update_type: factory, sysupgrade
        :return: Firmware, hash
        """
        Logger().debug("The firmware will be choosen from the manifest ...", 2)
        firmware_name, hash = self._chose_firmware_from_manifest(update_type)
        freifunk_verein = firmware_name.split('-')[1]
        firmware_version = firmware_name.split('-')[2]
        file = self.FIRMWARE_FILE + '/' + self.release_model.name + '/' + update_type.name + '/' + firmware_name
        url = self.url + '/' + self.release_model.name + '/' + update_type.name + '/' + firmware_name
        return [Firmware(firmware_name, firmware_version, freifunk_verein, self.release_model, update_type, file, url), hash]

    def _get_firmware_info_manually(self) -> Firmware:
        """
        Creates a firmware, with the url and the save-file.
        The User can input a url, where the firmware should downloaded from.
        :return: Firmware
        """
        Logger().debug("The firmware will be choosen by the given url ...", 2)
        url = input("URL of the firmware: ")
        firmware_name = url.split('/')[:-1]
        update_type = url.split('/')[-2]
        release_model = url.split('/')[-3]
        freifunk_verein = firmware_name.split('-')[1]
        firmware_version = firmware_name.split('-')[2]
        file = self.FIRMWARE_FILE + '/' + release_model.name + '/' + update_type.name + '/' + firmware_name
        return Firmware(firmware_name, firmware_version, freifunk_verein, release_model, update_type, file, url)

    def _verify_release_model(self, release_model: ReleaseModel) -> bool:
        """
        If the firmware is created manually via url, it could be that the release_model changed.
        The function checks this possibility.
        :param release_model: stable, beta, experimental
        :return: bool
        """
        if self.release_model.name != release_model.name:
            Logger().warning("The release_model of the selected(" + self.release_model.name
                 + ") and the given(" + release_model.name + ") are different", 2)
            val = input("Keep going? [y/n]:")
            Logger().info("<== " + val, 1)
            if val == "y":
                self.release_model = release_model
                return True
            return False
        return True

    def _download_firmware(self, url: str, file: str, update_type: UpdateType):
        """
        Downloads the firmware from the url and saves it into the given file
        :param url:
        :param file:
        :param update_type:
        :return:
        """
        Logger().info("Download " + url + " ...", 2)
        self._create_path(self.FIRMWARE_FILE + '/' + self.release_model.name + '/' + update_type.name)
        try:
            # Download the file from `url` and save it locally under `file_name`:
            urllib.request.urlretrieve(url, file)
            Logger().debug("[+] Successfully downloaded firmware", 3)
            return True
        except Exception as e:
            Logger().debug("[-] Couldn't download firmware", 3)
            Logger().error(str(e), 3)
            return False

    def _download_manifest(self) -> str:
        """
        Downloads the manifest and saves it
        :return:
        """
        url = self.url + '/'+self.release_model.name + '/' + UpdateType.sysupgrade.name + '/' + self.release_model.name + '.manifest'
        file = self.FIRMWARE_FILE + '/' + self.release_model.name + '/' + UpdateType.sysupgrade.name + '/' + self.release_model.name + '.manifest'
        self._create_path(self.FIRMWARE_FILE + '/' + self.release_model.name + '/' + UpdateType.sysupgrade.name)
        try:
            Logger().info("Download " + url, 2)
            # Download the file from `url` and save it locally under `file_name`:
            urllib.request.urlretrieve(url, file)
            Logger().debug("[+] Successfully downloaded manifest", 3)
            return file
        except Exception as e:
            Logger().debug("[-] Couldn't download manifest", 3)
            Logger().error(str(e), 2)
            return ""

    def _chose_firmware_from_manifest(self, update_type: UpdateType):
        """
        Gives the possibility to select a firmware from a list of firmwares.
        :param update_type: factory, sysupgrade
        :return: firmware_name, hash of the firmware
        """
        firmwares = self._get_firmwares_from_manifest()
        Logger().info("Manifest ------------------------------------")
        for i in range(0, len(firmwares)):
            Logger().info(firmwares[i])
        Logger().info("---------------------------------------------")
        valid_input = False
        val = 0
        while not valid_input:
            Logger().info("Which firmware should be downloaded?")
            val = 24 # TODO int(input("Select a number: "))
            Logger().info("<== " + str(val))
            valid_input = True if (val >= 0) and (val < len(firmwares)) else False
        tmp = "-sysupgrade.bin" if (update_type.name == "sysupgrade") else ".bin"
        firmware_name = "gluon" + firmwares[val].split("gluon")[1].split("-sysupgrade")[0]+tmp
        hash = firmwares[val].split(' ')[3]
        return [firmware_name, hash]

    def _get_firmwares_from_manifest(self) -> str:
        """
        Creates a list of firmwares from the manifest.
        :return: list of firmwares
        """
        Logger().debug("Create a list of firmwares from the manifest ...", 4)
        file = self._download_manifest()
        firmwares = []
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                if i >= 4:
                    firmware = "[" + str(i-4) + "]  " + line
                    firmwares.append(firmware)
            firmwares = firmwares[:-3]
            f.close()
        return firmwares

    def firmware_available_in_manifest(self, firmware_name: str) -> bool:
        """
        Checks if the given firmware is written inside the manifest
        :param firmware_name:
        :return: bool
        """
        file = self.FIRMWARE_FILE + '/' + self.release_model.name + '/' + UpdateType.sysupgrade.name + '/' + self.release_model.name + '.manifest'
        with open(file, 'r') as f:
            for line in f:
                if firmware_name in line:
                    return True
        return False

    def _parse_router_model(self, router_model: str):
        """
        Transform a str like "TP-LINK TL-WR841N/ND v9" into "tp-link-tl-wr841n-nd-v9"
        :param router_model:
        :return: router_model_name and router_model_version
        """
        Logger().debug("Parse RouterModel ...", 3)
        tmp = router_model.split(' v')
        router_model_name = tmp[0]
        router_model_version = 'v'+tmp[1]
        router_model_name = router_model_name.lower()
        # replace all symbols with a minus
        router_model_name = re.sub(r'(?:[^\w])', '-', router_model_name)
        Logger().debug("'" + router_model + "' into '" + router_model_name + " " + router_model_version + "'", 4)
        return [router_model_name, router_model_version]

    def _create_path(self, path: str):
        """
        Creates directories if necessary
        :param path:
        :return:
        """
        try:
            Logger().debug("Create path " + path + " ...", 3)
            os.makedirs(path)
            Logger().debug("[+] Path successfully created", 4)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
