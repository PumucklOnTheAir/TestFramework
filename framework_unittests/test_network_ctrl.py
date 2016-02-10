from unittest import TestCase
from network.network_ctrl import NetworkCtrl
from network.nv_assist import NVAssistent
from router.router import Router, Mode
from pyroute2 import netns
import os


class TestNetworkCtrl(TestCase):
    """
    This TestModule tests the functionality of the NetworkCtrl.

        1. Create Router (Mode: normal)
        2. Try to connect via SSH
        3. Try to send a command "uname"
        4. Try to send Data via wget
    """""

    @classmethod
    def setUpClass(cls):
        cls.router = cls._create_router()
        # NVAssisten
        cls.nv_assist = NVAssistent("eth0")
        cls.nv_assist.create_namespace_vlan(cls.router)
        # Set netns for the current process
        netns.setns(cls.router.namespace_name)
        # Create NetworkCrtl
        cls.network_ctrl = NetworkCtrl(cls.router)
        assert isinstance(cls.network_ctrl, NetworkCtrl)

    def test_network_ctrl(self):
        try:
            self._test_connection()
            self._test_send_command()
            self._test_router_wget()
        except Exception as e:
            raise
        finally:
            self.nv_assist.close()

    def _test_connection(self):
        # Test if a ssh connection is possible
        self.assertRaises(Exception, self.network_ctrl.connect_with_remote_system())

    def _test_send_command(self):
        # Test if the command 'uname' could be send via ssh
        output = self.network_ctrl.send_command("uname")
        self.assertEqual(str(output), "['Linux\\n']")

    def _test_router_wget(self):
        # Create test file 'test_wget.txt'
        path = os.path.dirname(__file__)
        open(path + '/test_wget.txt', 'w+')
        # The Router downloads this file via wget from the raspberryPi
        self.network_ctrl.remote_system_wget(path + '/test_wget.txt', '/tmp/',
                                             self.nv_assist.get_ip_address(self.router.namespace_name,
                                                                           self.router.vlan_iface_name)[0])
        # Tests if the file has successful downloaded
        output = self.network_ctrl.send_command("test -f '/tmp/test_wget.txt' && echo True")
        self.assertEqual(str(output), "['True\\n']")

    @classmethod
    def _create_router(cls):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.configuration
        assert isinstance(router, Router)
        return router
