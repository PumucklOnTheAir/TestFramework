import unittest
from server.server import Server
from server.router import Router


class MyTestCase(unittest.TestCase):
    def setUp(self):
        Server.start(debug_mode=True, config_path="../tests/config", vlan_activate=False)
        pass

    def tearDown(self):
        Server.stop()
        pass

    def test_get_routers(self):
        routers = Server.get_routers()
        assert len(routers) != 0
        assert isinstance(routers[0], Router)
