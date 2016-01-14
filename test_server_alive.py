#!/usr/bin/env python3

import unittest
import time
from server.server import Server
from multiprocessing import Process
from server.ipc import IPC


server_all_ready_started = False


class ServerAlive(unittest.TestCase):
    """
    Little test which tests if he can connect as a client to the server.
    If you are running this module standalone it will try to connect to an all ready started server.
    If not it creates his own server instance.
    """""

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
        Server.start(debug_mode=True, config_path="../tests/config", vlan_activate=False)

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
