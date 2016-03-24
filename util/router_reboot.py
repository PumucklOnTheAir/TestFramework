from threading import Thread
from network.network_ctrl import NetworkCtrl
from router.router import Router, Mode
from log.loggersetup import LoggerSetup
from network.remote_system import RemoteSystemJob
from util.dhclient import Dhclient
import logging
import time


class RouterReboot(Thread):
    """
    Reboots the Router into normal-mode or configuration-mode.
    """""

    def __init__(self, router: Router, configmode: bool):
        """
        :param router: Router Object
        :param configmode: 'True' if the Router should reboot in the configuration mode
        """
        Thread.__init__(self)
        self.router = router
        self.configmode = configmode
        self.daemon = True

    def run(self):
        """
        Runs new thread and trys to send a command via ssh to reboot the Router.
        """
        logging.info("%sReboot the Router(" + str(self.router.id) + ") ...", LoggerSetup.get_log_deep(1))
        network_ctrl = NetworkCtrl(self.router)
        try:
            network_ctrl.connect_with_remote_system()
        except Exception as e:
            logging.error("%s" + str(e), LoggerSetup.get_log_deep(2))
            logging.error("%s[-] Couldn't reboot Router(" + str(self.router.id) + ")", LoggerSetup.get_log_deep(2))
            network_ctrl.exit()
            return
        # Reboot Router into configuration-mode
        if self.configmode:
            if self.router.mode == Mode.configuration:
                logging.info("%s[+] Router is already in " + str(Mode.configuration), LoggerSetup.get_log_deep(2))
                network_ctrl.exit()
                return
            try:
                network_ctrl.send_command("uci set 'gluon-setup-mode.@setup_mode[0].enabled=1'")
                network_ctrl.send_command("uci commit")
                network_ctrl.send_command("reboot")
                logging.info("%sWait until Router rebooted (60sec) ...", LoggerSetup.get_log_deep(2))
                time.sleep(60)
                Dhclient.update_ip(self.router.vlan_iface_name)
                self._success_handling()
            except FileExistsError:
                self._success_handling()
                pass
            except Exception as e:
                self._execption_hanling()
        # Reboot Router into normal-mode
        else:
            if self.router.mode == Mode.normal:
                logging.info("%s[+] Router is already in " + str(Mode.normal), LoggerSetup.get_log_deep(2))
                network_ctrl.exit()
                return
            try:
                network_ctrl.send_command("reboot")
                logging.info("%sWait until Router rebooted (90sec) ...", LoggerSetup.get_log_deep(2))
                time.sleep(90)
                Dhclient.update_ip(self.router.vlan_iface_name)
                self._success_handling()
            except FileExistsError:
                self._success_handling()
                pass
            except Exception as e:
                self._execption_hanling()
        network_ctrl.exit()

    def _success_handling(self):
        """
        Sets the Router in config/normal-mode depending on given mode.
        """
        mode = Mode.configuration if self.configmode else Mode.normal
        logging.info("%s[+] Router was set into " + str(mode), LoggerSetup.get_log_deep(2))
        self.router.mode = mode

    def _execption_hanling(self):
        """
        Sets the Router in unkknown-mode.
        """
        logging.warning("%s[!] The mode of the Router is unknown", LoggerSetup.get_log_deep(2))
        self.router.mode = Mode.unknown


class RouterRebootJob(RemoteSystemJob):
    """
    Encapsulate RouterReboot as a job for the Server.
    """""
    def __init__(self, configmode: bool):
        super().__init__()
        self.configmode = configmode

    def run(self):
        """
        Starts RotuerReboot in a new thread.

        :return: Router-Obj in a dictionary
        """
        router = self.remote_system
        router_info = RouterReboot(router, self.configmode)
        router_info.start()
        router_info.join()
        return {'router': router}

    def pre_process(self, server) -> {}:
        return None

    def post_process(self, data: {}, server) -> None:
        """
        Updates the router in the Server with the new information

        :param data: Result from run()
        :param server: The Server
        """
        ref_router = server.get_router_by_id(data['router'].id)
        # Don't forget to update this method
        ref_router.update(data['router'])
