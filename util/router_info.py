from threading import Thread
from network.network_ctrl import NetworkCtrl
from server.router import Router
from log.logger import Logger


class RouterInfo(Thread):

    def __init__(self, router: Router):
        Thread.__init__(self)
        self.router = router
        self.daemon = True

    def run(self):
        """
        Runs new thread and gets the information from the router via ssh

        :return:
        """
        Logger().info("Update the Infos of the Router(" + str(self.router.id) + ") ...", 1)
        network_ctrl = NetworkCtrl(self.router)
        network_ctrl.connect_with_remote_system()
        # Model
        self.router.model = network_ctrl.send_command(
            'cat /proc/cpuinfo | grep machine').split(":")[1][:-4]
        # MAC
        self.router.mac = network_ctrl.send_command(
            'uci show network.client.macaddr').split('=')[1][:-4]
        # SSID
        self.router.ssid = network_ctrl.send_command(
            'uci show wireless.client_radio0.ssid').split('=')[1][:-4]

    def join(self):
        Thread.join(self)
