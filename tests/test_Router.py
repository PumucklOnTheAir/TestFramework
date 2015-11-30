import unittest

from server.router import Router

class MyTestCase(unittest.TestCase):
    def test_create_Router(self):
        r1 = Router("VLAN Name1", 42, "192.168.0.99", 43)
        assert isinstance(r1, Router)



if __name__ == '__main__':
    unittest.main()
