from unittest import TestCase

from network.network_ctrl import NetworkCtrl
from server.router import Router


class TestWebConfigurationAssistExpert(TestCase):

    CONFIG = {'node_name': '64293-testframework1',
              'mesh_vpn': True,
              'limit_bandwidth': False,
              'show_location': True,
              'latitude': '49.872161',
              'longitude': '8.635345',
              'altitude': '140.5',
              'contact': 'ops@darmstadt.freifunk.net',
              'private_wlan': False,
              'ssid': '',
              'ssid_key': '',
              'ssh_keys': '',
              'password': 'root',
              'ipv4': 'automatic',
              'ipv4_address': '',
              'ipv4_netmask': '255.255.255.0',
              'gateway_v4': '',
              'ipv6': 'static',
              'ipv6_address': '',
              'gateway_v6': '',
              'static_dns_server': '',
              'mesh_wan': False,
              'mesh_lan': False,
              'security_mode': True,
              'performance_mode': False,
              'client_network': False,
              'mesh_network': True,
              'transmission_power': 'default',
              'auto_update': False,
              'branch': 'stable'}

    def test_setup_expert(self):
        """
        This UnitTest executes the wca_setup_expert-function with the given config-file.
        It sets the values of all the  from WebInterface of the Router.
        """
        # Create router
        router = Router(1, "vlan1", 21, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)
        # Create NetworkCrtl
        network_ctrl = NetworkCtrl(router, 'enp0s25')
        assert isinstance(network_ctrl, NetworkCtrl)

        self.assertRaises(Exception, network_ctrl.wca_setup_expert(self.CONFIG))

        network_ctrl.exit()