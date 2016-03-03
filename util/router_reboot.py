from threading import Thread
from network.network_ctrl import NetworkCtrl
from router.router import Router, Mode
from log.loggersetup import LoggerSetup
import logging
from network.remote_system import RemoteSystemJob
from util.dhclient import Dhclient
import time


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
        logging.info("%sReboot the Router(" + str(self.router.id) + ") ...", LoggerSetup.get_log_deep(1))
        network_ctrl = NetworkCtrl(self.router)
        try:
            network_ctrl.connect_with_remote_system()
        except Exception as e:
            logging.warning("[-] Couldn't reboot Router(" + str(self.router.id) + ")")
            logging.warning(str(e))
            network_ctrl.exit()
            return
        if self.configmode:
            if self.router.mode == Mode.configuration:
                logging.info("%s[+] Router is already in configuration mode", LoggerSetup.get_log_deep(2))
                network_ctrl.exit()
                return
            try:
                network_ctrl.send_command("uci set 'gluon-setup-mode.@setup_mode[0].enabled=1'")
                network_ctrl.send_command("uci commit")
                network_ctrl.send_command("reboot")
                logging.info("Wait until Router rebooted (45sec) ...")
                time.sleep(45)
                if Dhclient.update_ip(self.router.vlan_iface_name) == 0:
                    self.router.mode = Mode.configuration
                    logging.info("%s[+] Router was set into configuration mode", LoggerSetup.get_log_deep(2))
                else:
                    network_ctrl.exit()
                    raise Exception
            except Exception as e:
                logging.warning("%s[-] Couldn't set Router into configuration mode", LoggerSetup.get_log_deep(2))
                logging.error("%s" + str(e), LoggerSetup.get_log_deep(2))
        else:
            if self.router.mode == Mode.normal:
                logging.info("%s[+] Router is already in normal mode", LoggerSetup.get_log_deep(2))
                network_ctrl.exit()
                return
            try:
                network_ctrl.send_command("reboot")
                logging.info("Wait until Router rebooted (45sec) ...")
                time.sleep(45)
                if Dhclient.update_ip(self.router.vlan_iface_name) == 0:
                    self.router.mode = Mode.normal
                    logging.info("%s+] Router was set into normal mode", LoggerSetup.get_log_deep(2))
                else:
                    network_ctrl.exit()
                    raise Exception
            except Exception as e:
                logging.warning("%s[-] Couldn't set Router into normal mode", LoggerSetup.get_log_deep(2))
                logging.error("%s" + str(e), LoggerSetup.get_log_deep(2))
        network_ctrl.exit()


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
        return {'router': router}

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
