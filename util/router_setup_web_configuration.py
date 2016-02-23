from threading import Thread
from router.router import Router, Mode
from log.logger import Logger
from network.web_config_assist import WebConfigurationAssist
from network.remote_system import RemoteSystemJob
from util.dhclient import Dhclient
import time


class RouterWebConfiguration(Thread):
    """
    The RouterWebConfiguration setup the webinterface of the Router by a given configuration-file.
    """""

    def __init__(self, router: Router, webinterface_config: dict, wizard: bool):
        """
        Instantiate a NetworkCtrl and setup the webinterface of the Router

        :param router:
        :param webinterface_config: {node_name, mesh_vpn, limit_bandwidth, show_location, latitude, longitude, ...}
        :param wizard: if the wizard page should be configured
        """
        Thread.__init__(self)
        self.router = router
        self.webinterface_config = webinterface_config
        self.wizard = wizard
        self.daemon = True

    def run(self):
        """
        Instantiate a NetworkCtrl and setup the webinterface of the Router
        """
        Logger().info("Configure the webinterface of the Router(" + str(self.router.id) + ") ...")
        if self.wizard:
            self._wca_setup_wizard(self.webinterface_config)
        else:
            self._wca_setup_expert(self.webinterface_config)

    def _wca_setup_wizard(self, config):
        """
        Starts the WebConfigurationAssist and
        sets the values provided by the wizard-mode (in the WebConfiguration)
        :param config: {node_name, mesh_vpn, limit_bandwidth, show_location, latitude, longitude, altitude, contact,...}
        """
        try:
            # remote_sytem has to be a router object
            wca = WebConfigurationAssist(config, self.router)
            wca.setup_wizard()
            wca.exit()
        except Exception as e:
            Logger().error(str(e), 2)
            raise e
        # The Router should reboot
        Logger().info("Wait until Router rebooted (45sec) ...")
        time.sleep(45)
        if Dhclient.update_ip(self.router.vlan_iface_name) == 0:
            self.router.mode = Mode.normal
            Logger().info("[+] Router was set into normal mode", 2)
        else:
            Logger().warning("[!] Couldn't get a new IP for Router(" + str(self.router.id) + ")")

    def _wca_setup_expert(self, config):
        """
        Starts the WebConfigurationAssist and
        sets the values provided by the expert-mode(in the WebConfiguration)
        :param config: {node_name, mesh_vpn, limit_bandwidth, show_location, latitude, longitude, altitude, contact,...}
        """
        try:
            # remote_sytem has to be a router object
            wca = WebConfigurationAssist(config, self.router)
            wca.setup_expert_private_wlan()
            wca.setup_expert_remote_access()
            wca.setup_expert_network()
            wca.setup_expert_mesh_vpn()
            wca.setup_expert_wlan()
            wca.setup_expert_autoupdate()
        except Exception as e:
            Logger().error(str(e), 2)
            raise e


class RouterWebConfigurationJob(RemoteSystemJob):
    """
    Encapsulate  RouterWebConfiguration as a job for the Server
    """""
    def __init__(self, webinterface_config: dict, wizard: bool):
        super().__init__()
        self.webinterface_config = webinterface_config
        self.wizard = wizard

    def run(self):
        router = self.remote_system
        router_info = RouterWebConfiguration(router, self.webinterface_config, self.wizard)
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
