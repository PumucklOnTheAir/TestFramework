from server.test import FirmwareTest


class StupidTest(FirmwareTest):
    """
    This is a demo test - only to test the functionality of the framework itself and it is very short..
    """""
    def test_not_very_long_test(self):
        lol = True
        assert lol
        assert not not lol

    def test_buzz1(self):
        lol = True
        assert lol
        assert not not lol

    def test_foo2(self):
        lol = True
        assert lol
        assert not not lol