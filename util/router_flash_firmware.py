from threading import Thread

from firmware.firmware_handler import FirmwareHandler
from log.logger import Logger
from network.network_ctrl import NetworkCtrl
from router.router import Router


class Sysupdate(Thread):
    """
    Instantiate a NetworkCtrl and copy the firmware via SSH to the Router(/tmp/<firmware_name>.bin)
    """""

    def __init__(self, router: Router, firmware_config):
        Thread.__init__(self)
        self.router = router
        self.firmware_config = firmware_config
        self.daemon = True

    def run(self):
        """
        Instantiate a NetworkCtrl and copy the firmware via SSH to the Router(/tmp/<firmware_name>.bin)
        :return:
        """
        Logger().info("Sysupdate Firmware for Router(" + str(self.router.id) + ") ...")
        firmware_handler = FirmwareHandler(self.firmware_config['URL'])
        firmware = firmware_handler.get_firmware(self.router.model, self.firmware_config['Release_Model'],
                                                 self.firmware_config['Download_All'])
        self.router.firmware = firmware


class Sysupgrade(Thread):
    """
    Instantiate a NetworkCtrl, proves if the firmware is on the Router(/tmp/<firmware_name>.bin)
    and does a Sysupgrade.
    """""
    def __init__(self, router: Router, n: bool, web_server_ip: str, debug: bool= False):
        """
        :param router: Router object
        :param n: reject the last firmware configurations
        :param web_server_ip: the IP where the Router can download the firmware image (should be the frameworks IP)
        :param debug: if we don't want to realy sysupgrade the firmware
        """
        Thread.__init__(self)
        Logger().info("Sysupgrade of Firmware from Router(" + str(router.id) + ") ...")

        self.router = router
        self.n = n
        self.web_server_ip = web_server_ip
        self.debug = debug
        self.daemon = True

    def run(self):
        """
        Copies the firmware image onto the Router, proves if the firmware is in the right file(/tmp/<firmware_name>.bin)
        and does a Sysupgrade.
        :return:
        """
        network_ctrl = NetworkCtrl(self.router)
        network_ctrl.connect_with_remote_system()
        network_ctrl.remote_system_wget(self.router.firmware.file, '/tmp/', self.web_server_ip)
        # sysupgrade -n <firmware_name> // -n verwirft die letzte firmware
        arg = '-n' if self.n else ''
        if not self.debug:
            network_ctrl.send_command('sysupgrade ' + arg + ' ' + '/tmp/' + self.router.firmware.name)
