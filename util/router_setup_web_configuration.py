from threading import Thread
from router.router import Router
from log.logger import Logger
from network.network_ctrl import NetworkCtrl
from network.web_config_assist import WebConfigurationAssist


# TODO: Die einzelnen Funktionen sollen später nicht in einem Thread ausgeführt werden.
# TODO: Im Moment stürtzt allerdings der Server noch ab wenn der NetworkCrtl nicht in einem eigenen Thread läuft
'''
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
'''


class RouterWebConfiguration(Thread):

    def __init__(self, router: Router, webinterface_config, wizard: bool):
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
        Logger().info("Sysupdate Firmware for Router(" + str(self.router.id) + ") ...")
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

    def join(self):
        Thread.join(self)
