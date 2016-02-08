import unittest
from server.server import Server
from router.router import Router
from multiprocessing import Process
from server.ipc import IPC
import time
import os
import socket


def block_until_server_is_online():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while sock.connect_ex(('localhost', 5000)):
        time.sleep(3)
    sock.close()


class ServerTestCase2(unittest.TestCase):

    proc = None

    @classmethod
    def setUpClass(cls):
        #  starts the IPC server in another(!) process
        cls.proc = Process(target=ServerTestCase2.serverStartWithParams, args=()).start()
        block_until_server_is_online()

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
        base_dir = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
        config_path = os.path.join(base_dir, 'framework_unittests/configs/config_no_vlan')
        Server.start(config_path=config_path)

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

        # wait until tests are done
        while not self.server_proxy.get_reports():
            time.sleep(2)

        reports = self.server_proxy.get_reports()
        assert len(reports) != 0
        assert len(reports[-1].errors) == 0  # check last report

    def test_long_self_check(self):
        started = self.server_proxy.start_test(0, "VeryLongTest")
        assert started
        if started:
            #time.sleep(2)

            self.server_proxy.stop_all_tasks()

            time.sleep(2)

            reports = self.server_proxy.get_reports()
            assert len(reports) != 0
            assert reports[-1].wasSuccessful()  # check last report
