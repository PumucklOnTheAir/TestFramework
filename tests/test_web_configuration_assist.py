from unittest import TestCase

from network.network_ctrl import NetworkCtrl
from server.router import Router


class TestWebConfigurationAssist(TestCase):

    CONFIG = {'node_name': '64293-testframework1',
              'mesh_vpn': True,
              'limit_bandwidth': False,
              'show_location': True,
              'latitude': '49.872161',
              'longitude': '8.635345',
              'altitude': '140.5',
              'contact': 'ops@darmstadt.freifunk.net',
              'private_wlan': False,
              'ssh_keys': '',
              'password': 'root',
              'ipv4': 'automatic',
              'ipv6': 'static',
              'static_dns_server': '8.8.8.8',
              'mesh_wan': True,
              'mesh_lan': True,
              'security_mode': False,
              'performance_mode': True,
              'client_network': False,
              'mesh_network': True,
              'transmission_power': 'default',
              'auto_update': False,
              'branch': 'stable'}

    def test_setup_wizard(self):
        # Create router
        router = Router(1, "vlan1", 21, "192.168.2.13", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)
        # Create NetworkCrtl
        network_ctrl = NetworkCtrl(router, 'enp0s25')
        assert isinstance(network_ctrl, NetworkCtrl)

        self.assertRaises(Exception, network_ctrl.wca_setup_wizard(self.CONFIG))

        network_ctrl.exit()

    def test_setup_expert(self):
        # Create router
        router = Router(1, "vlan1", 21, "192.168.2.13", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)
        # Create NetworkCrtl
        network_ctrl = NetworkCtrl(router, 'enp0s25')
        assert isinstance(network_ctrl, NetworkCtrl)

        self.assertRaises(Exception, network_ctrl.wca_setup_expert(self.CONFIG))

        network_ctrl.exit()

    def test_reset_expert_all(self):
        # Create router
        router = Router(1, "vlan1", 21, "192.168.2.13", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)
        # Create NetworkCrtl
        network_ctrl = NetworkCtrl(router, 'enp0s25')
        assert isinstance(network_ctrl, NetworkCtrl)

        self.assertRaises(Exception, network_ctrl.wca_reset_expert_all())

        network_ctrl.exit()
