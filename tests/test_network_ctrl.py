from unittest import TestCase
from network.network_ctrl import NetworkCtrl
from server.router import Router
from server.router import Mode
import os


class TestNetworkCtrl(TestCase):

    def test_connection(self):
        # Create router
        router = Router(1, "vlan1", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.configuration
        assert isinstance(router, Router)
        # Create NetworkCrtl
        network_ctrl = NetworkCtrl(router, 'eth0')
        assert isinstance(network_ctrl, NetworkCtrl)
        # network_ctrl.connect_with_router()
        network_ctrl.exit()

    def test_send_command(self):
        # Create router
        router = Router(1, "vlan1", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.configuration
        assert isinstance(router, Router)
        # Create NetworkCrtl
        network_ctrl = NetworkCtrl(router, 'eth0')
        assert isinstance(network_ctrl, NetworkCtrl)
        # Test if the command 'uname' could be send via ssh
        self.assertRaises(Exception, network_ctrl.connect_with_remote_system())
        output = network_ctrl.send_command("uname")
        self.assertEqual(output, "['Linux\\n']")
        network_ctrl.exit()

    def test_router_wget(self):
        # Create router
        router = Router(1, "vlan1", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.configuration
        assert isinstance(router, Router)
        # Create NetworkCrtl
        network_ctrl = NetworkCtrl(router, 'eth0')
        assert isinstance(network_ctrl, NetworkCtrl)
        self.assertRaises(Exception, network_ctrl.connect_with_remote_system())
        # Create test file 'test_wget.txt'
        path = os.path.dirname(__file__)
        file = open(path + '/test_wget.txt', 'w+')
        # The Router downloads this file via wget from the raspberryPi
        network_ctrl.remote_system_wget(path + '/test_wget.txt', '/tmp/')
        # Tests if the file has successful downloaded
        output = network_ctrl.send_command("test -f '/tmp/test_wget.txt' && echo True")
        self.assertEqual(output, "['True\\n']")
        # Test
        output = network_ctrl.send_command("rm '/tmp/test_wget.txt' && echo True")
        self.assertEqual(output, "['True\\n']")
        file.close()
        network_ctrl.exit()
