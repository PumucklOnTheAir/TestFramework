from threading import Thread
from firmware.firmware_handler import FirmwareHandler
from log.logger import Logger
from network.network_ctrl import NetworkCtrl
from router.router import Router
from network.remote_system import RemoteSystemJob


class Sysupdate(Thread):
    """
    Downloads the firmware image from an update-server
    """""

    def __init__(self, router: Router, firmware_config: dict):
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


class SysupdateJob(RemoteSystemJob):
    """
    Encapsulate  Sysupdate as a job for the Server
    """""
    def __init__(self, firmware_config: dict):
        super().__init__()
        self.firmware_config = firmware_config

    def run(self):
        router = self.remote_system
        router_info = Sysupdate(router, self.firmware_config)
        router_info.start()
        router_info.join()
        self.return_data({'router': router})

    def pre_process(self, server) -> {}:
        return None

    def post_process(self, data: {}, server) -> None:
        """
        Updates the router in the Server with the new information

        :param data: result from run()
        :param server: the Server
        :return:
        """
        ref_router = server.get_router_by_id(data['router'].id)
        ref_router.update(data['router'])  # Don't forget to update this method


class Sysupgrade(Thread):
    """
    Copy the firmware via SSH to the Router(/tmp/<firmware_name>.bin)
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
        try:
            network_ctrl.connect_with_remote_system()
        except Exception as e:
            Logger().warning("[-] Couldn't sysupgrade the Router(" + str(self.router.id) + ")")
            Logger().warning(str(e))
            return
        network_ctrl.remote_system_wget(self.router.firmware.file, '/tmp/', self.web_server_ip)
        # sysupgrade -n <firmware_name> // -n verwirft die letzte firmware
        arg = '-n' if self.n else ''
        if not self.debug:
            network_ctrl.send_command('sysupgrade ' + arg + ' ' + '/tmp/' + self.router.firmware.name)


class SysupgradeJob(RemoteSystemJob):
    """
    Encapsulate  Sysupgrade as a job for the Server
    """""
    def __init__(self, n: bool, web_server_ip: str, debug: bool= False):
        super().__init__()
        self.n = n
        self.web_server_ip = web_server_ip
        self.debug = debug

    def run(self):
        router = self.remote_system
        router_info = Sysupgrade(router, self.n, self.web_server_ip, self.debug)
        router_info.start()
        router_info.join()
        self.return_data({'router': router})

    def pre_process(self, server) -> {}:
        return None

    def post_process(self, data: {}, server) -> None:
        """
        Updates the router in the Server with the new information

        :param data: result from run()
        :param server: the Server
        :return:
        """
        ref_router = server.get_router_by_id(data['router'].id)
        ref_router.update(data['router'])  # Don't forget to update this method
