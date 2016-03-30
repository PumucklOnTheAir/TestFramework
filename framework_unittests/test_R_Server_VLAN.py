
from framework_unittests.test_A_Server_2 import ServerCore, block_until_server_is_online
from server.server import Server
from multiprocessing import Process
import unittest


class ServerTestCaseVLAN(ServerCore, unittest.TestCase):

    proc = None

    @classmethod
    def setUpClass(cls):
        #  starts the IPC server in another(!) process
        cls.proc = Process(target=ServerTestCaseVLAN.serverStartWithParams, args=()).start()
        block_until_server_is_online()

    @staticmethod
    def serverStartWithParams():
        Server.start()
