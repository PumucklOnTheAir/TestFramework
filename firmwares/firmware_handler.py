import urllib.request
from enum import Enum


class ReleaseModel(Enum):
    stable = 1
    beta = 2
    experimental = 3


class FirmwareHandler:
    def __init__(self, freifunk_verein: str, release_model: ReleaseModel, url: str):
        self.freifunk_verein = freifunk_verein
        self.release_model = release_model
        self.url = url
        self.MANIFEST_FILE = "manifest.txt"
        self.FIRMWARE_FILE = "firmware"

    def download_firmware(self, router_model_name: str, router_model_version: str, firmware_version: str, factory: bool):
        firmware_name = 'gluon-'+self.freifunk_verein+'-'+firmware_version+'-' + router_model_name + '-' + router_model_version
        if factory:
            firmware_name = firmware_name + '.bin'
            tmp = 'factory'
        else:
            firmware_name = firmware_name + '-sysupgrade.bin'
            tmp = 'sysupgrade'
        url = self.url+'/'+self.release_model.name+'/'+tmp+'/'+firmware_name
        # Download the file from `url` and save it locally under `file_name`:
        urllib.request.urlretrieve(url, self.FIRMWARE_FILE+'/'+self.release_model.name+'/'+tmp+'/'+firmware_name)

    def download_manifest(self):
        url = self.url+'/'+self.release_model.name+'/sysupgrade/'+self.release_model.name+'.manifest'
        # Download the file from `url` and save it locally under `file_name`:
        urllib.request.urlretrieve(url, self.MANIFEST_FILE)

    def parse_router_model_name(self, router_model_name):
        router_model_name = router_model_name.lower()
