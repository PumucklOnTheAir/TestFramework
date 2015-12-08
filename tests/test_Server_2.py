import unittest
from server.server import Server
from server.router import Router
from multiprocessing import Process
from server.ipc import IPC
import time


class ServerTestCase2(unittest.TestCase):

    proc = None

    @classmethod
    def setUpClass(cls):
        #  starts the IPC server in other(!) process
        cls.proc = Process(target=ServerTestCase2.serverStartWithParams, args=()).start()
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        ipc_client = IPC()
        ipc_client.connect()
        server_proxy = ipc_client.get_server_proxy()
        server_proxy.stop()

    @staticmethod
    def serverStartWithParams():
        Server.start(debug_mode=True, config_path="../tests/config", vlan_activate=False)

    def setUp(self):
        self.ipc_client = IPC()
        self.ipc_client.connect()
        self.server_proxy = self.ipc_client.get_server_proxy()

    def test_get_routers(self):
        print(self.server_proxy)
        print(repr(self.server_proxy))
        print(self.ipc_client.get_server_proxy())


        routers = self.server_proxy.get_routers()
        assert len(routers) != 0
        assert isinstance(routers[0], Router)
