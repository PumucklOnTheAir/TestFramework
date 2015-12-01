from threading import Thread
from network.network_ctrl import NetworkCtrl
from typing import List
from server.router import Router


class RouterInfo:

    @staticmethod
    def update(routers: List[Router]):
        """
        : Desc : starts a thread for each router and stores new information
        :param routers: list of router objects
        :return:
        """
        for router in routers:
            worker = Worker(router)
            worker.start()
            router = worker.join()


class Worker(Thread):

    def __init__(self, router: Router):
        Thread.__init__(self)
        self.router = router
        self.daemon = True

    def run(self):
        """
        : Desc : runs new thread and gets the information from the router via ssh
        :return:
        """
        print("run new thread ...")
        network_ctrl = NetworkCtrl(self.router)
        network_ctrl.connect_with_router()
        # Model
        self.router.model = network_ctrl.send_router_command(
            'cat /proc/cpuinfo | grep machine').split(":")[1][:-4]
        # MAC
        self.router.mac = network_ctrl.send_router_command(
            'uci show network.client.macaddr').split('=')[1][:-4]
        # SSID
        self.router.ssid = network_ctrl.send_router_command(
            'uci show wireless.client_radio0.ssid').split('=')[1][:-4]
        network_ctrl.exit()

    def join(self):
        Thread.join(self)
        return self.router
