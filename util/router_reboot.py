from threading import Thread
from network.network_ctrl import NetworkCtrl
from router.router import Router, Mode
from log.logger import Logger
from network.remote_system import RemoteSystemJob


class RouterReboot(Thread):
    """
    The RouterInfo collects in a new Thread informations about the Routers
    """""

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
        Logger().info("Reboot the Router(" + str(self.router.id) + ") ...", 1)
        network_ctrl = NetworkCtrl(self.router)
        try:
            network_ctrl.connect_with_remote_system()
        except Exception as e:
            Logger().warning("[-] Couldn't reboot Router(" + str(self.router.id) + ")")
            Logger().warning(str(e))
            return
        if self.configmode:
            if self.router.mode == Mode.configuration:
                Logger().info("[+] Router is already in configuration mode", 2)
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
                Logger().info("[+] Router is already in normal mode", 2)
                return
            try:
                network_ctrl.send_command("reboot")
                self.router.mode = Mode.normal
                Logger().info("[+] Router was set into normal mode", 2)
            except Exception as e:
                Logger().warning("[-] Couldn't set Router into normal mode", 2)
                Logger().error(str(e), 2)


class RouterRebootJob(RemoteSystemJob):
    """
    Encapsulate  RouterReboot as a job for the Server
    """""
    def __init__(self, configmode: bool):
        super().__init__()
        self.configmode = configmode

    def run(self):
        router = self.remote_system
        router_info = RouterReboot(router, self.configmode)
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
