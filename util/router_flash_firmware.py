from threading import Thread
from network.network_ctrl import NetworkCtrl
from typing import List
from server.router import Router
from firmware.firmware_handler import FirmwareHandler
from firmware.firmware import Firmware, ReleaseModel, UpdateType
from log.logger import Logger


class RouterFlashFirmware:

    @staticmethod
    def configuration(routers: List[Router], firmware_config):
        """
        Instantiate a NetworkCtrl and copy the firmware via SSH to the Router(/tmp/<firmware_name>.bin)
        :param routers:
        :param firmware_config:
        :return:
        """
        for router in routers:
            worker = ConfigurationWorker(router, firmware_config)
            worker.start()
            worker.join()

    @staticmethod
    def sysupgrade(routers: List[Router], n: bool):
        """
        In a new thread.
        Instantiate a NetworkCtrl, proves if the firmware is on the Router(/tmp/<firmware_name>.bin)
        and does a Sysupgrade.
        :param routers:
        :param n:
        :return:
        """
        for router in routers:
            worker = SysupgradeWorker(router, n)
            worker.start()
            worker.join()


class ConfigurationWorker(Thread):

    def __init__(self, router: Router, firmware_config):
        Thread.__init__(self)
        Logger().info("Configure Firmware for Router(" + router.mac + ") ...")
        self.router = router
        self.firmware_handler = FirmwareHandler(firmware_config[1], firmware_config[0])
        self.firmware = self.firmware_handler.get_firmware(firmware_config[2], router.model, firmware_config[3],
                                                           firmware_config[4])
        self.daemon = True

    def run(self):
        """
        Instantiate a NetworkCtrl and copy the firmware via SSH to the Router(/tmp/<firmware_name>.bin)
        :return:
        """
        Logger().info("Copy Firmware to Router(" + self.router.mac + ") ...")
        network_ctrl = NetworkCtrl(self.router)
        network_ctrl.connect_with_router()
        network_ctrl.send_data(self.firmware.file, '/tmp/'+self.firmware.name)
        network_ctrl.exit()
        self.router.firmware_tmp = self.firmware

    def join(self):
        Thread.join(self)


class SysupgradeWorker(Thread):

    def __init__(self, router: Router, n: bool):
        Thread.__init__(self)
        Logger().info("Sysupgrade of Firmware from Router(" + router.mac + ") ...")
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
        network_ctrl.connect_with_router()
        # Validate that the firmware is in the right directory "/tmp/"
        firmware_exists = network_ctrl.send_router_command('[ -f /tmp/'+self.router.firmware_tmp.name + ' ]')
        if firmware_exists:
            # sysupgrade -n <firmware_name> // -n verwirft die letzte firmware
            arg = '-n' if self.n else ''
            network_ctrl.send_router_command('sysupgrade ' + arg + ' ' + '/tmp/' + self.router.firmware_tmp.name)
        else:
            print("The firmware " + self.router.firmware_tmp.name + " doesn't exist in /tmp/")
        network_ctrl.exit()

    def join(self):
        Thread.join(self)