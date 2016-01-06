from unittest import TestCase

from network.network_ctrl import NetworkCtrl
from server.router import Router
from network.web_config_assist import WebConfigurationAssist
from log.logger import Logger



class TestWebConfigurationAssist(TestCase):
    def test_setup_wizard(self):
        # Create router
        router = Router(1, "vlan1", 21, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)
        # Create NetworkCrtl
        network_ctrl = NetworkCtrl(router, 'enp0s25')
        #assert isinstance(network_ctrl, NetworkCtrl)

        wizard_config = {'url': 'http://192.168.1.1/cgi-bin/luci',
                       'node_name': '64293-testframework1',
                       'mesh_vpn': True,
                       'limit_bandwidth': False,
                       'show_location': True,
                       'latitude': '49.872160',
                       'longitude': '8.635345',
                       'altitude': '140.5',
                       'contact': 'ops@darmstadt.freifunk.net'}

        network_ctrl.wca_setup_wizard(wizard_config)

        network_ctrl.exit()
