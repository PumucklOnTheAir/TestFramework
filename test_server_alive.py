#!/usr/bin/env python3

import unittest
from server.server import Server
from multiprocessing import Process
from server.ipc import IPC
from framework_unittests.test_Server_2 import block_until_server_is_online
import time


server_already_started = False


class ServerAlive(unittest.TestCase):
    """
    Little test which tests if it is possible to connect as a client to the test server.
    If you are running this module standalone it will try to connect to an all ready started server.
    If not it creates his own server instance.
    """""
    proc = None

    @classmethod
    def setUpClass(cls):
        if not server_already_started:
            #  starts the IPC server in another(!) process
            cls.proc = Process(target=ServerAlive.serverStartWithParams, args=()).start()
            block_until_server_is_online()

    @classmethod
    def tearDownClass(cls):
        if not server_already_started:
            ipc_client = IPC()
            ipc_client.connect()
            server_proxy = ipc_client.get_server_proxy()
            server_proxy.stop()

    @staticmethod
    def serverStartWithParams():
        Server.start(config_path='framework_unittests/configs/config_no_vlan')

    def setUp(self):
        self.ipc_client = IPC()
        self.ipc_client.connect()
        self.server_proxy = self.ipc_client.get_server_proxy()

        if not server_already_started:
            # wait until server has all tasks before executed
            for i in range(2):  # do it two times to be sure
                routers = self.server_proxy.get_routers()
                for router in routers:
                    while not not self.server_proxy.get_routers_task_queue_size(router.id):
                        time.sleep(2)
                        print('.', end="", flush=True)

    def test_get_version(self):
        version = self.server_proxy.get_server_version()
        assert version == Server.VERSION

if __name__ == '__main__':
    server_already_started = True
    unittest.main(verbosity=2)
