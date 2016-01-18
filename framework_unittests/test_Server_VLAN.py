import unittest
from server.server import Server
from server.router import Router
from multiprocessing import Process
from server.ipc import IPC
import time
import os


class ServerTestCase2(unittest.TestCase):

    proc = None

    @classmethod
    def setUpClass(cls):
        #  starts the IPC server in another(!) process
        cls.proc = Process(target=ServerTestCase2.serverStartWithParams, args=()).start()
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        print("Shutdown server")
        ipc_client = IPC()
        ipc_client.connect()
        server_proxy = ipc_client.get_server_proxy()
        server_proxy.stop()

    @staticmethod
    def serverStartWithParams():
        # base_dir = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
        # config_path = os.path.join(base_dir, 'framework_unittests/configs/config_no_vlan')
        Server.start()

    def setUp(self):
        self.ipc_client = IPC()
        self.ipc_client.connect()
        self.server_proxy = self.ipc_client.get_server_proxy()

    def test_get_routers(self):
        routers = self.server_proxy.get_routers()
        assert len(routers) != 0
        assert isinstance(routers[0], Router)

    def test_little_self_check(self):
        started = self.server_proxy.start_test(0, "ConnectionTest")
        assert started
        time.sleep(5)
        reports = self.server_proxy.get_reports()
        assert len(reports) != 0

    def test_long_self_check(self):
        started = self.server_proxy.start_test(0, "VeryLongTest")
        assert started
        time.sleep(5)

        self.server_proxy.stop_all_tasks()

        time.sleep(2)

        routers = self.server_proxy.get_routers()
        for router in routers:
            assert router.running_task is None
