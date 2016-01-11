from threading import Thread

from firmware.firmware_handler import FirmwareHandler
from log.logger import Logger
from network.network_ctrl import NetworkCtrl
from server.router import Router


# TODO: Die einzelnen Funktionen sollen später nicht in einem Thread ausgeführt werden.
# TODO: Im Moment stürtzt allerdings der Server noch ab wenn der NetworkCrtl nicht in einem eigenen Thread läuft
class RouterFlashFirmware:

    @staticmethod
    def sysupdate(router: Router, firmware_config):
        """
        Instantiate a NetworkCtrl and copy the firmware via SSH to the Router(/tmp/<firmware_name>.bin)
        :param router:
        :param firmware_config:
        """
        worker = SysupdateWorker(router, firmware_config)
        worker.start()
        worker.join()

    @staticmethod
    def sysupgrade(router: Router, n: bool):
        """
        Instantiate a NetworkCtrl, proves if the firmware is on the Router(/tmp/<firmware_name>.bin)
        and does a Sysupgrade.
        :param router:
        :param n: If n is True the upgrade discard the last firmware
        """
        worker = SysupgradeWorker(router, n)
        worker.start()
        worker.join()


class SysupdateWorker(Thread):

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
        firmware_handler = FirmwareHandler(self.firmware_config[0])
        firmware = firmware_handler.get_firmware(self.router.model, self.firmware_config[1], self.firmware_config[3])
        self.router.firmware = firmware

    def join(self):
        Thread.join(self)


class SysupgradeWorker(Thread):

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
        network_ctrl.connect_with_router()
        network_ctrl.router_wget(self.router.firmware.file, '/tmp/')
        # sysupgrade -n <firmware_name> // -n verwirft die letzte firmware
        arg = '-n' if self.n else ''
        network_ctrl.send_router_command('sysupgrade ' + arg + ' ' + '/tmp/' + self.router.firmware.name)
        network_ctrl.exit()

    def join(self):
        Thread.join(self)
