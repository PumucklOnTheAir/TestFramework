import unittest
import Server


class MyTestCase(unittest.TestCase):

    def setUp(self):
        Server.start(True, "../tests/config")
        pass

    def tearDown(self):
        Server.stop()
        pass

    def test_get_routers(self):
        routers = Server.get_routers()
        assert len(routers) != 0
