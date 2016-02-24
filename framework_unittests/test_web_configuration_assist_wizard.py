from unittest import TestCase
from pyroute2 import netns
from network.nv_assist import NVAssistent
from router.router import Router, Mode
from config.configmanager import ConfigManager
from util.router_setup_web_configuration import RouterWebConfiguration


class TestWebConfigurationAssistWizard(TestCase):

    def test_setup_expert(self):
        """
        This UnitTest executes the wca_setup_expert-function with the given config-file.
        It sets the values of all the  from WebInterface of the Router.
        """
        router = self._create_router()
        # NVAssisten
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan(router)
        # Set netns for the current process
        netns.setns(router.namespace_name)

        # Config
        config = ConfigManager().get_web_interface_dict()[router.id]
        self.assertEqual(len(config), 30, "Wrong size of the Config-Directory")

        router_web_config = RouterWebConfiguration(router, config, wizard=True)
        router_web_config.start()
        router_web_config.join()

        assert router.mode == Mode.configuration

        nv_assist.close()

    def _create_router(self):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.configuration
        assert isinstance(router, Router)
        return router
