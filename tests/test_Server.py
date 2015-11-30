import unittest
from server.server import Server
from server.router import Router


class MyTestCase(unittest.TestCase):
    s = None

    def setUp(self):
        self.s = Server()
        self.s.start(True, "../tests/config")
        pass

    def tearDown(self):
        self.s.stop()
        pass

    def test_get_routers(self):
        routers = self.s.get_routers()
        assert len(routers) != 0
        assert isinstance(routers[0], Router)
