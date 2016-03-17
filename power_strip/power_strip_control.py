from threading import Thread
from network.network_ctrl import NetworkCtrl
from network.remote_system import RemoteSystemJob
from power_strip.ubnt import Ubnt
import logging


class PowerStripControl(Thread):

    def __init__(self, power_strip: Ubnt, on_or_off: bool, port: int):
        Thread.__init__(self)
        self.power_strip = power_strip
        self.on_or_off = on_or_off
        self.port = port
        self.network_ctrl = NetworkCtrl(self.power_strip)
        self.daemon = True

    def run(self):
        """
        Runs new thread
        """
        self.network_ctrl.connect_with_remote_system()
        cmd = self.create_command(self.on_or_off, self.port)
        self.network_ctrl.send_command(cmd)

        check = self._port_status(self.port)
        result = self.network_ctrl.send_command(check)
        result = result[0]
        if self.on_or_off:
            if result == "1":
                logging.info("[+] Successfully switched on port " + str(self.port))
            else:
                logging.info("[-] Error switching on port " + str(self.port))
        else:
            if result == "0":
                logging.info("[+] Successfully switched off port " + str(self.port))
            else:
                logging.info("[-] Error switching off port " + str(self.port))

        self.network_ctrl.exit()

    def create_command(self, on_or_off: bool, port: int):
        return self.power_strip.create_command(port, on_or_off)

    def _port_status(self, port: int):
        return self.power_strip.port_status(port)


class PowerStripControlJob(RemoteSystemJob):
    """
    Encapsulate  PowerStripControl as a job for the Server
    """""
    def __init__(self, on_or_off: bool, port: int):
        super().__init__()
        self.on_or_off = on_or_off
        self.port = port

    def run(self):
        power_strip = self.remote_system
        power_strip_ = PowerStripControl(power_strip, self.on_or_off, self.port)
        power_strip_.start()
        power_strip_.join()
        return {'powerstrip': power_strip}

    def pre_process(self, server) -> {}:
        return None

    def post_process(self, data: {}, server) -> None:
        return None
