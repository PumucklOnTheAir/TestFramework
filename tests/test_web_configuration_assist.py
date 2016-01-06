from unittest import TestCase

from network.network_ctrl import NetworkCtrl
from server.router import Router
from network.web_config_assist import WebConfigurationAssist
from log.logger import Logger



class TestWebConfigurationAssist(TestCase):
    def test_setup_wizard(self):
        # Create router
        router = Router(1, "vlan1", 20, "192.168.2.13", 24, "bananapi", "bananapi", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)
        # Create NetworkCrtl
        network_ctrl = NetworkCtrl(router)
        #assert isinstance(network_ctrl, NetworkCtrl)

        wizard_conf = {'url': 'http://192.168.2.13:8000/index.xhtml',
                       'node_name': '64293-testframework1',
                       'mesh_vpn': True,
                       'limit_bandwidth': False,
                       'show_location': True,
                       'latitude': '49.872160',
                       'longitude': '8.635345',
                       'altitude': '140.5',
                       'contact': 'ops@darmstadt.freifunk.net'}

        network_ctrl.wca_setup_wizard(wizard_conf)

        network_ctrl.exit()
