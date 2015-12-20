from unittest import TestCase
from network.network_ctrl import NetworkCtrl
from server.router import Router


class TestNetworkCtrl(TestCase):
    def test_connection(self):
        # Create router
        router = Router(1, "vlan20", 20, "192.168.2.13", 24, "bananapi", "bananapi", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)
        # Create NetworkCrtl
        network_ctrl = NetworkCtrl(router)
        assert isinstance(network_ctrl, NetworkCtrl)

        # network_ctrl.connect_with_router()
        network_ctrl.exit()

    """
    def test_send_command(self):
        # Create router
        router = Router("vlan21", 21, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        assert isinstance(router, Router)
        # Create NetworkCrtl
        network_ctrl = NetworkCtrl(router)
        assert isinstance(network_ctrl, NetworkCtrl)

        network_ctrl.connect_with_router()
        output = network_ctrl.send_router_command("uname")
        network_ctrl.exit()
    """