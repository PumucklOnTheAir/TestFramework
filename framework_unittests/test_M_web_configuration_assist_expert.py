from unittest import TestCase
from pyroute2 import netns
from network.nv_assist import NVAssistent
from router.router import Router, Mode
from config.configmanager import ConfigManager
from util.router_setup_web_configuration import RouterWebConfiguration


class TestWebConfigurationAssistExpert(TestCase):

    def test_setup_expert(self):
        """
        This UnitTest executes the wca_setup_expert-function with the given config-file.
        It sets the values of all the  from WebInterface of the Router.
        """
        print("Test if the 'wca_setup_expert'-function is working")
        router = self._create_router()
        # NVAssisten
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan(router)
        # Set netns for the current process
        netns.setns(router.namespace_name)

        # Config
        config = ConfigManager.get_web_interface_list()[router.id]
        self.assertEqual(len(config), 30, "Wrong size of the Config-Directory")

        print("Set the following configuration: \n" + str(config))

        router_web_config = RouterWebConfiguration(router, config, wizard=False)
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
