import unittest
from server.server import Server
from router.router import Router
from threading import Timer
import time
import os


class ServerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #  starts the IPC server in the same process
        t = Timer(0.0, ServerTestCase.serverStartWithParams)
        t.start()  # but in other thread
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        Server.stop()

    @staticmethod
    def serverStartWithParams():
        base_dir = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
        config_path = os.path.join(base_dir, 'tests/configs/config_no_vlan')  # Join Project Root with config
        Server.start(config_path=config_path)

    def test_get_routers(self):
        routers = Server.get_routers()
        assert len(routers) != 0
        assert isinstance(routers[0], Router)
