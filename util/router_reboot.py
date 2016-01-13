from threading import Thread
from network.network_ctrl import NetworkCtrl
from server.router import Router, Mode
from log.logger import Logger


class RouterReboot:
    """
    The RouterInfo collects in a new Thread informations about the Routers
    """

    @staticmethod
    def configmode(router: Router):
        """
        Reboots the Router into the configuration mode
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
        """
        Init the new thread which is rebooting the Router
        :param router: Router Object
        :param configmode: if the Router should reboot in the configuration mode
        """
        Thread.__init__(self)
        self.router = router
        self.configmode = configmode
        self.daemon = True

    def run(self):
        """
        Runs new thread and trys to send a command via ssh to reboot the Router.
        """
        network_ctrl = NetworkCtrl(self.router, 'enp0s25')
        network_ctrl.connect_with_remote_system()
        if self.configmode:
            if self.router.mode == Mode.configuration:
                Logger().info("[+] Router is already in configuration mode", 2)
                network_ctrl.exit()
                return
            try:
                network_ctrl.send_command("uci set 'gluon-setup-mode.@setup_mode[0].enabled=1'")
                network_ctrl.send_command("uci commit")
                network_ctrl.send_command("reboot")
                self.router.mode = Mode.configuration
            except Exception as e:
                Logger().warning("[-] Couldn't set Router into configuration mode", 2)
                Logger().error(str(e), 2)
            Logger().info("[+] Router was set into configuration mode", 2)
        else:
            if self.router.mode == Mode.normal:
                Logger().info("[+] Router is already in configuration mode", 2)
                network_ctrl.exit()
                return
            try:
                network_ctrl.send_command("reboot")
                self.router.mode = Mode.normal
                Logger().info("[+] Router was set into normal mode", 2)
            except Exception as e:
                Logger().warning("[-] Couldn't set Router into normal mode", 2)
                Logger().error(str(e), 2)

        network_ctrl.exit()

    def join(self):
        Thread.join(self)