#!/usr/bin/env python3

import unittest
import time
from server.server import Server
from multiprocessing import Process
from server.ipc import IPC
import os


server_all_ready_started = False


class ServerAlive(unittest.TestCase):
    """
    Little test which tests if he can connect as a client to the server.
    If you are running this module standalone it will try to connect to an all ready started server.
    If not it creates his own server instance.
    """""
    # TODO This test seems to be broken
    proc = None

    @classmethod
    def setUpClass(cls):
        if not server_all_ready_started:
            #  starts the IPC server in another(!) process
            cls.proc = Process(target=ServerAlive.serverStartWithParams, args=()).start()
            time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        if not server_all_ready_started:
            ipc_client = IPC()
            ipc_client.connect()
            server_proxy = ipc_client.get_server_proxy()
            server_proxy.stop()

    @staticmethod
    def serverStartWithParams():
        base_dir = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
        config_path = os.path.join(base_dir, 'tests/configs/config_no_vlan')  # Join Project Root with config
        Server.start(config_path=config_path)

    def setUp(self):
        self.ipc_client = IPC()
        self.ipc_client.connect()
        self.server_proxy = self.ipc_client.get_server_proxy()

    def test_get_version(self):
        version = self.server_proxy.get_server_version()
        assert len(version) != 0

if __name__ == '__main__':
    server_all_ready_started = True
    unittest.main(verbosity=2)
