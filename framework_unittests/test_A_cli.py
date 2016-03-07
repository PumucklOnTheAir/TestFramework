import unittest
from cli import create_parsers
import time
from server.server import Server
from multiprocessing import Process
from server.ipc import IPC
import os


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
        assert args.mode is None
        assert not args.verbose

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
        assert not args.wizard

        args = self.parser.parse_args(["webconfig", "-a", "-w"])
        assert args.all
        assert args.mode == "webconfig"
        assert args.wizard

    def test_update_info(self):
        args = self.parser.parse_args(["update_info", "-r", "1", "2", "3"])
        assert not args.all
        assert args.routers == [1, 2, 3]
        assert args.mode == "update_info"

        args = self.parser.parse_args(["update_info", "-a"])
        assert args.all
        assert args.mode == "update_info"


class TestCLItoServerConnection(unittest.TestCase):
    path_cli = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cli.py')

    proc = None

    @classmethod
    def setUpClass(cls):
        #  starts the IPC server in another(!) process
        cls.proc = Process(target=TestCLItoServerConnection.serverStartWithParams, args=()).start()
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        ipc_client = IPC()
        ipc_client.connect()
        server_proxy = ipc_client.get_server_proxy()
        server_proxy.stop()

    @staticmethod
    def serverStartWithParams():
        base_dir = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
        config_path = os.path.join(base_dir, 'tests/configs/config_no_vlan')  # Join Project Root with config
        Server.start(config_path=config_path)

    def setUp(self):
        self.ipc_client = IPC()
        self.ipc_client.connect()
        self.server_proxy = self.ipc_client.get_server_proxy()

    def test_cli_connected(self):
        response = os.system(self.path_cli)
        assert response == 0

    def test_cli_start_test_set(self):
        response = os.system(self.path_cli + " start -s set_1 -r 0")
        assert response == 0

    def test_get_version(self):
        version = self.server_proxy.get_server_version()
        assert version == Server.VERSION
