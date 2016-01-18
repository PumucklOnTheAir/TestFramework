from threading import Thread
from server.router import Router
from log.logger import Logger
from network.network_ctrl import NetworkCtrl


# TODO: Die einzelnen Funktionen sollen später nicht in einem Thread ausgeführt werden.
# TODO: Im Moment stürtzt allerdings der Server noch ab wenn der NetworkCrtl nicht in einem eigenen Thread läuft
class RouterWebConfiguration:

    @staticmethod
    def setup(router: Router, webinterface_config):
        """
        Instantiate a NetworkCtrl and setup the webinterface of the Router

        :param router:
        :param webinterface_config: {node_name, mesh_vpn, limit_bandwidth, show_location, latitude, longitude, ...}
        """
        worker = SetupWorker(router, webinterface_config)
        worker.start()
        worker.join()


class SetupWorker(Thread):

    def __init__(self, router: Router, webinterface_config):
        """
        Instantiate a NetworkCtrl and setup the webinterface of the Router

        :param router:
        :param webinterface_config: {node_name, mesh_vpn, limit_bandwidth, show_location, latitude, longitude, ...}
        """
        Thread.__init__(self)
        self.router = router
        self.webinterface_config = webinterface_config
        self.daemon = True

    def run(self):
        """
        Instantiate a NetworkCtrl and setup the webinterface of the Router
        """
        Logger().info("Sysupdate Firmware for Router(" + str(self.router.id) + ") ...")
        network_ctrl = NetworkCtrl(self.router, 'eth0')
        network_ctrl.wca_setup_expert(self.webinterface_config)
        network_ctrl.wca_setup_wizard(self.webinterface_config)
        network_ctrl.exit()

    def join(self):
        Thread.join(self)
