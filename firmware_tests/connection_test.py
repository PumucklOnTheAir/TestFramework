from server.test import FirmwareTest
import time

class ConnectionTest(FirmwareTest):

    def test_buzz1(self):
        # print("buzz1")
        lol = True
        assert lol
        assert not not lol
        assert not lol

    def test_foo2(self):
        # print("foo2")
        lol = True
        assert lol
        assert not not lol
        assert not lol

    def test_self_router(self):
        # print(str(self.router))
        assert self.router.id != 0


class VeryLongTest(FirmwareTest):

    def test_very_long_test(self):
        lol = True
        assert lol
        time.sleep(5)
        assert not not lol
        assert not lol

