from threading import Thread
from network.network_ctrl import NetworkCtrl
from network.remote_system import RemoteSystemJob
from power_strip.ubnt import Ubnt


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

    def _get_router_model(self) -> str:
        """
        :return: the Model of the given Router object
        """
        return self.network_ctrl.send_command('cat /proc/cpuinfo | grep machine')[0].split(":")[1][1:-1]

    def _get_router_mac(self) -> str:
        """
        :return: the MAC of the given Router object
        """
        return self.network_ctrl.send_command('uci show network.client.macaddr')[0].split('=')[1][:-1]

    def _get_router_ssid(self):
        """
        :return: the SSID of the given Router object
        """
        return self.network_ctrl.send_command('uci show wireless.client_radio0.ssid')[0].split('=')[1][:-1]


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
