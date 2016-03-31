from log.loggersetup import LoggerSetup
import hashlib
import logging


class Firmware:
    """
    Represents a FreiFunk-Firmware, that can be flashed on a router.

    """""

    def __init__(self, name: str, version: str, freifunk_verein: str, release_model: str, file: str, url: str):
        """
        :param name: Including router_model_name, router_model_version, firmware_version, freifunk_verein
        :param version: Version of the firmware (not version of router !!!)
        :param freifunk_verein: Like 'ffda'
        :param release_model: Can be set to: 'stable', 'beta' or 'experimental'. Used in the url
        :param file: Path/file where the firmware-image is stored on the device.
        :param url: URL of the server where the firmware-image can be downloaded
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
        Creates and returns a Firmware-Obj which can be used as a default value, if the firmware isn't known already.

        :return: Default Frimware-Obj
        """
        return Firmware('Firmware not known', '0.0.0', 'ffxx', 'stable', '', '')

    def check_hash(self, excep_hash: str) -> bool:
        """
        Checks whether the excepted hash equals the actual Hash of the Firmware.

        :param excep_hash: Hash excepted/ correct hash
        :return: 'True' if Hash is correct
        """
        logging.debug("%sCheck Hash of the Firmware(" + self.name + ") ...", LoggerSetup.get_log_deep(3))
        self.calc_hash()
        if self.hash == excep_hash:
            logging.debug("%s[+] The Hash is correct", LoggerSetup.get_log_deep(4))
            return True
        logging.warning("%s[-] The Hash is incorrect", LoggerSetup.get_log_deep(4))
        logging.warning("%sHash of the Firmware: " + self.hash, LoggerSetup.get_log_deep(4))
        logging.warning("%sExcepted Hash: " + excep_hash, LoggerSetup.get_log_deep(4))
        return False

    def calc_hash(self):
        """
        Calculate the hash of the Firmware and sets it as an attribute.
        """
        hasher = hashlib.sha512()
        with open(self.file, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        self._hash = hasher.hexdigest()

    @property
    def name(self) -> str:
        """
        Name of the Firmware, including: router_model_name, router_model_version, firmware_version, freifunk_verein.

        :return: Firmware_name
        """
        return self._name

    @name.setter
    def name(self, value: str):
        """
        Sets the name of the Firmware, including: router_model_name, router_model_version,
        firmware_version, freifunk_verein.

        :param value: Firmware_name
        """
        assert isinstance(value, str)
        self._name = value

    @property
    def version(self) -> str:
        """
        Version of the firmware. (not version of router !!!)

        :return: Firmware_version
        """
        return self._version

    @version.setter
    def version(self, value: str):
        """
        Sets the version of the firmware. (not version of router !!!)

        :param value: Firmware_version
        """
        assert isinstance(value, str)
        self._version = value

    @property
    def freifunk_verein(self) -> str:
        """
        Like 'ffda' which stands for 'freifunkdarmstadt'.

        :return: Firmware_freifunk_verein
        """
        return self._freifunk_verein

    @freifunk_verein.setter
    def freifunk_verein(self, value: str):
        """
        Like 'ffda' which stands for 'freifunkdarmstadt'-

        :param value: Firmware_freifunk_verein
        """
        assert isinstance(value, str)
        self._freifunk_verein = value

    @property
    def release_model(self) -> str:
        """
         Can be: 'stable', 'beta' or 'experimental'. Used in the url.

        :return: Firmware_release_model
        """
        return self._release_model

    @release_model.setter
    def release_model(self, value: str):
        """
        Can be set to: 'stable', 'beta' or 'experimental'. Used in the url.

        :param value: Firmware_release_model
        """
        assert isinstance(value, str)
        self._release_model = value

    @property
    def file(self) -> str:
        """
        Path/file where the firmware-image is stored on the device.

        :return: Firmware_file
        """
        return self._file

    @file.setter
    def file(self, value: str):
        """
        Sets the path/file, where the firmware-image is stored on the device.

        :param value: Firmware_file
        """
        assert isinstance(value, str)
        self._file = value

    @property
    def url(self) -> str:
        """
        URL of the server where the firmware-image can be downloaded.

        :return: Firmware_url
        """
        return self._url

    @url.setter
    def url(self, value: str):
        """
        Sets the URL of the server where the firmware-image can be downloaded.

        :param value: Firmware_url
        """
        assert isinstance(value, str)
        self._url = value

    @property
    def hash(self) -> str:
        """
        Hash of the firware-image.

        :return: Firmware_hash
        """
        return self._hash
