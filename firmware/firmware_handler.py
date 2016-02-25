import urllib.request
import re
import os
import errno
from firmware.firmware import Firmware
from log.logger import Logger


class FirmwareHandler:
    """
    The FirmwareHandler manages:
        1. The import of existing Firmwares stored in 'TestFramework/firmware/firmwares'
        2. The correct download of the Manifest for a given release_model(stable, beta, experimental)
        3, The correct download of a single or all Firmwares for a given release_model(stable, beta, experimental)
        4. Creates the Firmware-Objects and lists them
    """

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
    FIRMWARE_PATH = os.path.join(BASE_DIR, 'firmware/firmwares')  # Join the path to the webserver files with firmwares
    UPDATE_TYPE = "sysupgrade"

    def __init__(self, url: str):
        """
        :param url: alike "https://firmware.darmstadt.freifunk.net"
        """
        self.firmwares = []
        self.url = url

    def get_firmware(self, router_model: str, release_model: str, download_all: bool) -> Firmware:
        """
        Returns the correct Firmware of a Router_Model and in the specific Release_Model
        :param router_model:
        :param release_model: stable, beta, experimental
        :param download_all: if all Firmwares in the Manifest should be downloaded
        :return: Firmware
        """
        Logger().info("Configure download of Firmware for Router(" + router_model + ")", 1)
        self.import_firmwares(release_model)

        if download_all:
            self.firmwares = self.download_all_firmwares(release_model)
        else:
            firmware = self.get_stored_firmware(router_model)
            if firmware is not None:
                return firmware
            firmware = self.download_firmware(router_model, release_model)
            if firmware is not None:
                self.firmwares.append(firmware)
        return self.get_stored_firmware(router_model)

    def get_stored_firmware(self, router_model: str) -> Firmware:
        """
        Returns the matching Firmware if stored in the list self.firmwares
        :param router_model:
        :return: Firmware
        """
        router_model_name, router_model_version = self._parse_router_model(router_model)
        parsed_router_model = router_model_name + "-" + router_model_version
        for firmware in self.firmwares:
            if parsed_router_model in firmware.name:
                return firmware
        Logger().info("[-] Couldn't found a matching Firmware to Router(" + router_model + ")", 2)
        return None

    def _verified_download(self, firmware: Firmware, hash_firmware: str, max_attempts: int) -> bool:
        """
        Downloads the given Firmware and checks if the download was correct and if the hash is matching
        :param firmware:
        :param hash_firmware:
        :param max_attempts: max number of attemps to download a firmware
        :return: bool
        """
        valid_download = False
        count = 0
        while (not valid_download) & (count < max_attempts):
            valid_download = self._download_file(firmware.url, firmware.file, firmware.release_model)
            if valid_download:
                valid_download = firmware.check_hash(hash_firmware)
            count += 1
        if count >= max_attempts:
            Logger().debug("[-] The Firmware(" + firmware.name + ") couldn't be downloaded", 3)
            return False
        else:
            Logger().debug("[+] The Firmware(" + firmware.name + ") was successfully downloaded", 3)
            return True

    def download_firmware(self, router_model: str, release_model: str, max_attemps: int=3) -> Firmware:
        """
        Downloads only one Firmware which matches a Firmware in the Manifest
        :param router_model:
        :param release_model: stable, beta, experimental
        :param max_attemps: max number of attemps to download a firmware
        :return: Firmware
        """
        Logger().debug("Download single Firmware ...", 2)
        firmwares, hashs = self._get_all_firmwares(release_model)
        router_model_name, router_model_version = self._parse_router_model(router_model)
        parsed_router_model = router_model_name + "-" + router_model_version
        for i, firmware in enumerate(firmwares):
            if parsed_router_model in firmware.name:
                self._verified_download(firmware, hashs[i], max_attemps)
                return firmware
        return None

    def download_all_firmwares(self, release_model: str, max_attemps: int=3):
        """
        Downloads all Firmwares which are found in the manifest and proves the hash.
        If a download more than 3 times fails, the file will not be downloaded
        :param release_model: stable, beta, experimental
        :param max_attemps: max number of attemps to download a firmware
        :return: A List of all Firmware-Objects
        """
        Logger().debug("Download all Firmwares ...", 2)
        firmwares, hashs = self._get_all_firmwares(release_model)
        num_firmwares = len(firmwares)
        for i, firmware in enumerate(firmwares):
            valid_download = self._verified_download(firmware, hashs[i], max_attemps)
            if not valid_download:
                del(firmwares[i])
                del(hashs[i])
        Logger().info(str(len(firmwares)) + "/" + str(num_firmwares) + " Firmwares downloaded", 3)
        return firmwares

    def _get_all_firmwares(self, release_model: str):
        """
        Creats a list of Firmwares and a list of related Hashs.
        All Firmwares are given from the Manifest which is downloaded first.
        :param release_model: stable, beta, experimental
        :return:
        """
        firmwares = []
        hashs = []
        non_parsed_firmwares = self._read_firmwares_from_manifest(release_model)
        for firmware in non_parsed_firmwares:
            firmware_name = "gluon" + firmware.split("gluon")[1].split("-sysupgrade")[0] + "-" + \
                            FirmwareHandler.UPDATE_TYPE + "." + firmware.split(".")[-1].replace("\n", "")
            hash_firmware = firmware.split(' ')[4]
            freifunk_verein = firmware_name.split('-')[1]
            firmware_version = firmware_name.split('-')[2]
            file = (self.FIRMWARE_PATH + '/' + release_model + '/' + FirmwareHandler.UPDATE_TYPE + '/' +
                    firmware_name)
            url = self.url + '/' + release_model + '/' + FirmwareHandler.UPDATE_TYPE + '/' + firmware_name
            firmwares.append(Firmware(firmware_name, firmware_version, freifunk_verein, release_model, file, url))
            hashs.append(hash_firmware)
        return [firmwares, hashs]

    def _read_firmwares_from_manifest(self, release_model: str) -> str:
        """
        Creates a list of non pared Firmware_Names from the Manifest.
        :param release_model: stable, beta, experimental
        :return: list of firmwares written like in the manifest
        """
        Logger().debug("Create a list of firmwares from the manifest ...", 4)
        file = self._download_manifest(release_model)
        firmwares = []
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                if i >= 4:
                    firmware = "[" + str(i - 4) + "]  " + line
                    firmwares.append(firmware)
            firmwares = firmwares[:-3]
            f.close()
        return firmwares

    def firmware_available_in_manifest(self, release_model: str, firmware_name: str) -> bool:
        """
        Checks if the given firmware is written inside the manifest
        :param release_model: stable, beta, experimental
        :param firmware_name:
        :return: bool
        """
        file = (self.FIRMWARE_PATH + '/' + release_model + '/' + FirmwareHandler.UPDATE_TYPE + '/' +
                release_model + '.manifest')
        with open(file, 'r') as f:
            for line in f:
                if firmware_name in line:
                    return True
        return False

    def _download_file(self, url: str, file: str, release_model: str) -> bool:
        """
        Downloads the firmware from the url and saves it into the given file
        :param url: the url to the firmware
        :param file: the path/file were the firmware should be stored on the system
        :param release_model: stable, beta, experimental
        :return: True if the firmware was successfully downloaded
        """
        Logger().info("Download " + url + " ...", 2)
        self._create_path(self.FIRMWARE_PATH + '/' + release_model + '/' + FirmwareHandler.UPDATE_TYPE)
        try:
            # Download the file from `url` and save it locally under `file_name`:
            urllib.request.urlretrieve(url, file)
            return True
        except Exception as e:
            Logger().debug("[-] Failed download", 3)
            Logger().error(str(e), 3)
            return False

    def _download_manifest(self, release_model: str, max_count: int=3) -> str:
        """
        Downloads the manifest and saves it.
        :param release_model: stable, beta, experimental
        :return: The path/file were the manifest is stored.(builds from the url a path)
        """
        url = (self.url + '/' + release_model + '/' + FirmwareHandler.UPDATE_TYPE + '/' +
               release_model + '.manifest')
        file = (self.FIRMWARE_PATH + '/' + release_model + '/' + FirmwareHandler.UPDATE_TYPE + '/' +
                release_model + '.manifest')
        valid_download = False
        count = 0
        while (not valid_download) & (count < max_count):
            valid_download = self._download_file(url, file, release_model)
            count += 1
        if count >= max_count:
            Logger().debug("[-] Couldn't download manifest", 3)
            return ""
        else:
            Logger().debug("[+] Successfully downloaded manifest", 3)
            return file

    def _parse_router_model(self, router_model: str):
        """
        Transform a str like "TP-LINK TL-WR841N/ND v9" into "tp-link-tl-wr841n-nd-v9"
        :param router_model:
        :return: router_model_name and router_model_version
        """
        Logger().debug("Parse RouterModel ...", 2)
        tmp = router_model.split(' v')
        router_model_name = tmp[0]
        router_model_version = 'v' + tmp[1]
        router_model_name = router_model_name.lower()
        # replace all symbols with a minus
        router_model_name = re.sub(r'(?:[^\w])', '-', router_model_name)
        Logger().debug("'" + router_model + "' into '" + router_model_name + " " + router_model_version + "'", 3)
        return [router_model_name, router_model_version]

    def _create_path(self, path: str):
        """
        Creates directories if necessary
        :param path:
        """
        try:
            Logger().debug("Create path " + path + " ...", 3)
            os.makedirs(path)
            Logger().debug("[+] Path successfully created", 4)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
            Logger().debug("[+] Path allready exists", 4)

    def import_firmwares(self, release_model: str):
        """
        Imports the stored Firmwares, so the firmware_handler can use them.
        :param release_model: stable, beta, experimental
        """
        path = self.FIRMWARE_PATH + '/' + release_model + '/' + self.UPDATE_TYPE + '/'
        Logger().debug("Import Firmwares from '" + path + "'", 2)
        count = 0

        try:
            files = os.listdir(path)
        except Exception:
            Logger().debug("No Firmwares available for import at path '" + path + "'", 3)
            return

        for firmware_name in files:
            try:
                freifunk_verein = firmware_name.split('-')[1]
                firmware_version = firmware_name.split('-')[2]
                file = path + firmware_name
                url = self.url + '/' + release_model + '/' + self.UPDATE_TYPE + '/' + firmware_name
                self.firmwares.append(Firmware(firmware_name, firmware_version, freifunk_verein,
                                               release_model, file, url))
                count += 1
            except Exception:
                Logger().warning("[-] Couldn't import " + firmware_name, 3)
                continue
        Logger().debug(str(count) + " Firmwares imported", 3)
