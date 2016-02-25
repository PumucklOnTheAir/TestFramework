import hashlib
import logging
from log.loggersetup import LoggerSetup


class Firmware:
    """
    Represents a router firmware version.

    """""

    def __init__(self, name: str, version: str, freifunk_verein: str, release_model: str, file: str, url: str):
        """

        :param name: including router_model_name, router_model_version, firmware_version, freifunk_verein
        :param version: version of the firmware (not version of router !!!)
        :param freifunk_verein: like 'ffda'
        :param release_model: used in the url
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
        Checks whether the excepted Hash equals the actual Hash of the Firmware.

        :param excep_hash:
        :return:
        """
        logging.debug("%sCheck Hash of the Firmware(" + self.name + ") ...", LoggerSetup.get_log_deep(3))
        self.calc_hash()
        if self.hash == excep_hash:
            logging.debug("%s[+] The Hash is correct", LoggerSetup.get_log_deep(4))
            return True
        logging.debug("%s[-] The Hash is incorrect", LoggerSetup.get_log_deep(4))
        logging.debug("%sHash of the Firmware: " + self.hash, LoggerSetup.get_log_deep(4))
        logging.debug("%sExcepted Hash: " + excep_hash, LoggerSetup.get_log_deep(4))
        return False

    def calc_hash(self):
        """
        Calculate the Hash of the Firmware and sets it as an attribute.

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
