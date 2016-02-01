from unittest import TestCase

from network.network_ctrl import NetworkCtrl
from router.router import Router, Mode
from config.configmanager import ConfigManager
from util.router_setup_web_configuration import RouterWebConfiguration
from log.logger import Logger


class TestWebConfigurationAssistWizard(TestCase):

    def test_setup_expert(self):
        """
        This UnitTest executes the wca_setup_expert-function with the given config-file.
        It sets the values of all the  from WebInterface of the Router.
        """
        # Create router
        router = Router(1, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        router.mode = Mode.configuration
        assert isinstance(router, Router)
        # Config
        config = ConfigManager().get_web_interface_dict()[0]
        self.assertEqual(len(config), 30, "Wrong size of the Config-Directory")
        # Create NetworkCrtl
        network_ctrl = NetworkCtrl(router, 'eth0')
        assert isinstance(network_ctrl, NetworkCtrl)

        try:
            RouterWebConfiguration.setup(router, config, wizard=True)
        except Exception as e:
            Logger().error(str(e))
        finally:
            assert router.mode == Mode.normal
            network_ctrl.exit()
