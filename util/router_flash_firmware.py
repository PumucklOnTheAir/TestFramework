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
        # TODO: Liste sollte noch in directorys geändert werden, damit per string auf Elemente zugegriffen werden kann
        firmware_handler = FirmwareHandler(self.firmware_config['URL'])
        firmware = firmware_handler.get_firmware(self.router.model, self.firmware_config['Release_Model'], self.firmware_config['Download_All'])
        self.router.firmware = firmware

    def join(self):
        Thread.join(self)


class Sysupgrade(Thread):
    """
    Instantiate a NetworkCtrl, proves if the firmware is on the Router(/tmp/<firmware_name>.bin)
    and does a Sysupgrade.
    """""
    def __init__(self, router: Router, n: bool):
        Thread.__init__(self)
        Logger().info("Sysupgrade of Firmware from Router(" + str(router.id) + ") ...")

        self.router = router
        self.n = n

        self.daemon = True

    def run(self):
        """
        Instantiate a NetworkCtrl, proves if the firmware is on the Router(/tmp/<firmware_name>.bin)
        and does a Sysupgrade.
        :return:
        """
        network_ctrl = NetworkCtrl(self.router)
        network_ctrl.connect_with_remote_system()
        network_ctrl.remote_system_wget(self.router.firmware.file, '/tmp/')
        # sysupgrade -n <firmware_name> // -n verwirft die letzte firmware
        arg = '-n' if self.n else ''
        network_ctrl.send_command('sysupgrade ' + arg + ' ' + '/tmp/' + self.router.firmware.name)

    def join(self):
        Thread.join(self)
