from threading import Thread
from network.network_ctrl import NetworkCtrl
from server.router import Router
from log.logger import Logger


class RouterReboot:
    """
    The RouterInfo collects in a new Thread informations about the Routers
    """

    @staticmethod
    def configmode(router: Router):
        """
        Reboots the Router into the configmode
        :param router: Router objects
        """
        Logger().info("Reboot the Router(" + str(router.id) + ") into Configmode ...", 1)
        worker = Worker(router, True)
        worker.start()
        worker.join()

    @staticmethod
    def normal(router: Router):
        """
        Reboots the router
        :param router: Router objects
        """
        Logger().info("Reboot the Router(" + str(router.id) + ") ...", 1)
        worker = Worker(router, False)
        worker.start()
        worker.join()


class Worker(Thread):

    def __init__(self, router: Router, configmode: bool):
        Thread.__init__(self)
        self.router = router
        self.configmode = configmode
        self.daemon = True

    def run(self):
        """
        Runs new thread and gets the information from the router via ssh
        :return:
        """
        network_ctrl = NetworkCtrl(self.router)
        network_ctrl.connect_with_router()
        if self.configmode:
            network_ctrl.send_router_command("uci set 'gluon-setup-mode.@setup_mode[0].enable=1'")
            network_ctrl.send_router_command("uci commit")
        network_ctrl.send_router_command("reboot")
        network_ctrl.exit()

    def join(self):
        Thread.join(self)