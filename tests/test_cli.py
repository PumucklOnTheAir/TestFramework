import unittest
from cli import *


class TestCaseParser(unittest.TestCase):
    """
    Sets up parser to test CLI
    """
    @classmethod
    def setUpClass(cls):
        parser = create_parsers()
        cls.parser = parser


class CLITestClass(TestCaseParser):
    """
    Test class for command line interface interaction
    """
    def test_no_args(self):
        args = self.parser.parse_args([])
        assert args is None

    def test_status(self):
        args = self.parser.parse_args(["status", "-a"])
        assert args.all
        assert args.mode == "status"

        args = self.parser.parse_args(["status", "-r", "1"])
        assert args.router
        assert args.mode == "status"
        assert args.router == [1]

    def test_sysupgrade(self):
        args = self.parser.parse_args(["sysupgrade", "-a"])
        assert args.all
        assert not args.n
        assert args.mode == "sysupgrade"

        args = self.parser.parse_args(["sysupgrade", "-r", "1", "2", "3", "-n"])
        assert not args.all
        assert args.routers == [1, 2, 3]
        assert args.n
        assert args.mode == "sysupgrade"

    def test_sysupdate(self):
        args = self.parser.parse_args(["sysupdate", "-r", "1", "2", "3"])
        assert not args.all
        assert args.routers == [1, 2, 3]
        assert args.mode == "sysupdate"

        args = self.parser.parse_args(["sysupdate", "-a"])
        assert args.all
        assert args.mode == "sysupdate"

    def test_reboot(self):
        args = self.parser.parse_args(["reboot", "-a", "-c"])
        assert args.all
        assert args.config
        assert args.mode == "reboot"

        args = self.parser.parse_args(["reboot", "-a"])
        assert args.all
        assert not args.config
        assert args.mode == "reboot"

        args = self.parser.parse_args(["reboot", "-c"])
        assert args.config
        assert not args.all
        assert args.mode == "reboot"

        args = self.parser.parse_args(["reboot", "-r", "1", "2", "3", "-c"])
        assert args.config
        assert not args.all
        assert args.routers == [1, 2, 3]
        assert args.mode == "reboot"

    def test_webconfig(self):
        args = self.parser.parse_args(["webconfig", "-r", "1", "2", "3"])
        assert not args.all
        assert args.routers == [1, 2, 3]
        assert args.mode == "webconfig"

        args = self.parser.parse_args(["webconfig", "-a"])
        assert args.all
        assert args.mode == "webconfig"


if __name__ == '__main__':
    unittest.main()
