from enum import Enum


class ReleaseModel(Enum):
    stable = 1
    beta = 2
    experimental = 3


class UpdateType(Enum):
    factory = 1
    sysupgrade = 2


class Firmware:

    def __init__(self, name: str, version: str, freifunk_verein: str, release_model: ReleaseModel,
                 update_type: UpdateType, file: str, url: str):
        """
        :param name: including router_model_name, router_model_version, firmware_version, freifunk_verein
        :param version: version of the firmware (not version of router !!!)
        :param freifunk_verein: like 'ffda'
        :param release_model: used in the url
        :param update_type:
        :param file: used in the url
        :return:
        """
        self.name = name
        self.version = version
        self.freifunk_verein = freifunk_verein
        self.release_model = release_model
        self.update_type = update_type
        self.file = file
        self.url = url
