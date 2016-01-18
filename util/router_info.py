from threading import Thread
from network.network_ctrl import NetworkCtrl
from server.router import Router
from log.logger import Logger


class RouterInfo:
    """
    The RouterInfo collects in a new Thread informations about the Routers
    """

    @staticmethod
    def update(router: Router):
        """
        Starts a thread for a router and stores new information
        :param router: Router objects
        """
        # TODO: wird anstelle des threadings benutzt. Führt allerdings zu abstürtzen beim icp-server
        '''
        RouterInfo.update_single_router(router)
        '''
        Logger().info("Update the Infos of the Router(" + str(router.id) + ") ...", 1)
        worker = Worker(router)
        worker.start()
        worker.join()

    # TODO: ohne threads
    '''
    @staticmethod
    def update_single_router(router: Router):
        network_ctrl = NetworkCtrl(router)
        network_ctrl.connect_with_router()
        # Model
        router.model = network_ctrl.send_router_command(
            'cat /proc/cpuinfo | grep machine').split(":")[1][:-4]
        # MAC
        router.mac = network_ctrl.send_router_command(
            'uci show network.client.macaddr').split('=')[1][:-4]
        # SSID
        router.ssid = network_ctrl.send_router_command(
            'uci show wireless.client_radio0.ssid').split('=')[1][:-4]
        network_ctrl.exit()
    '''


class Worker(Thread):

    def __init__(self, router: Router):
        Thread.__init__(self)
        self.router = router
        self.daemon = True

    def run(self):
        """
        Runs new thread and gets the information from the router via ssh
        :return:
        """
        network_ctrl = NetworkCtrl(self.router, 'eth0')
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
        network_ctrl.exit()

    def join(self):
        Thread.join(self)
