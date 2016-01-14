from enum import Enum
import hashlib
from log.logger import Logger


class Firmware:

    def __init__(self, name: str, version: str, freifunk_verein: str, release_model: str, file: str, url: str):
        """
        :param name: including router_model_name, router_model_version, firmware_version, freifunk_verein
        :param version: version of the firmware (not version of router !!!)
        :param freifunk_verein: like 'ffda'
        :param release_model: used in the url
        :param update_type:
        :param file: used in the url
        :return:
        """
        self._name = name
        self._version = version
        self._freifunk_verein = freifunk_verein
        self._release_model = release_model
        self._file = file
        self._url = url
        self._hash = ""

    @staticmethod
    def get_default_firmware():
        """
        :return: A firmware-obj which can be used as a default value, if the firmware isn't known already
        """
        return Firmware('Firmware not known', '0.0.0', 'ffxx', 'stable', '', '')

    def check_hash(self, excep_hash: str) -> bool:
        """
        Checks whether the excepted Hash is equal the actual of the Firmware.
        :param excep_hash:
        :return:
        """
        Logger().debug("Check Hash of the Firmware(" + self.name + ") ...", 3)
        self.calc_hash()
        if self.hash == excep_hash:
            Logger().debug("[+] The Hash is correct", 4)
            return True
        Logger().debug("[-] The Hash is incorrect", 4)
        Logger().debug("Hash of the Firmware: " + self.hash, 4)
        Logger().debug("Excepted Hash: " + excep_hash, 4)
        return False

    def calc_hash(self):
        """
        Calculate the Hash of the Firmware and sets it as a atribute.
        :return:
        """
        hasher = hashlib.sha512()
        with open(self.file, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        self._hash = hasher.hexdigest()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        assert isinstance(value, str)
        self._name = value

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str):
        assert isinstance(value, str)
        self._version = value

    @property
    def freifunk_verein(self) -> str:
        return self._freifunk_verein

    @freifunk_verein.setter
    def freifunk_verein(self, value: str):
        assert isinstance(value, str)
        self._freifunk_verein = value

    @property
    def release_model(self) -> str:
        return self._release_model

    @release_model.setter
    def release_model(self, value: str):
        assert isinstance(value, str)
        self._release_model = value

    @property
    def file(self) -> str:
        return self._file

    @file.setter
    def file(self, value: str):
        assert isinstance(value, str)
        self._file = value

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str):
        assert isinstance(value, str)
        self._url = value

    @property
    def hash(self) -> str:
        return self._hash
