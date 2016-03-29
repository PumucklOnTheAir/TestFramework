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

    def test_status(self):
        args = self.parser.parse_args(["status"])
        assert not args.routers
        assert args.mode == "status"

        args = self.parser.parse_args(["status", "-r", "1"])
        assert args.router
        assert args.mode == "status"
        assert args.router == [1]

    def test_sysupgrade(self):
        args = self.parser.parse_args(["sysupgrade"])
        assert not args.routers
        assert not args.n
        assert args.mode == "sysupgrade"

        args = self.parser.parse_args(["sysupgrade", "-r", "1", "2", "3", "-n"])
        assert args.routers == [1, 2, 3]
        assert args.n
        assert args.mode == "sysupgrade"

    def test_sysupdate(self):
        args = self.parser.parse_args(["sysupdate", "-r", "1", "2", "3"])
        assert args.routers == [1, 2, 3]
        assert args.mode == "sysupdate"

        args = self.parser.parse_args(["sysupdate"])
        assert not args.routers
        assert args.mode == "sysupdate"

    def test_reboot(self):
        args = self.parser.parse_args(["reboot", "-c"])
        assert not args.routers
        assert args.config
        assert args.mode == "reboot"

        args = self.parser.parse_args(["reboot"])
        assert not args.routers
        assert not args.config
        assert args.mode == "reboot"

        args = self.parser.parse_args(["reboot", "-c"])
        assert args.config
        assert args.mode == "reboot"

        args = self.parser.parse_args(["reboot", "-r", "1", "2", "3", "-c"])
        assert args.config
        assert args.routers == [1, 2, 3]
        assert args.mode == "reboot"

    def test_webconfig(self):
        args = self.parser.parse_args(["webconfig", "-r", "1", "2", "3"])
        assert args.routers == [1, 2, 3]
        assert args.mode == "webconfig"
        assert not args.wizard

        args = self.parser.parse_args(["webconfig", "-w"])
        assert not args.routers
        assert args.mode == "webconfig"
        assert args.wizard

    def test_update_info(self):
        args = self.parser.parse_args(["update_info", "-r", "1", "2", "3"])
        assert args.routers == [1, 2, 3]
        assert args.mode == "update_info"

        args = self.parser.parse_args(["update_info"])
        assert not args.routers
        assert args.mode == "update_info"

    def test_online(self):
        args = self.parser.parse_args(["online", "-r", "1", "2", "3"])
        assert args.routers == [1, 2, 3]
        assert args.mode == "online"

        args = self.parser.parse_args(["online"])
        assert not args.routers
        assert args.mode == "online"

    def test_power(self):
        args = self.parser.parse_args(["power", "-r", "0", "-off"])
        self.assertFalse(args.all)
        self.assertEquals(args.routers, [0], "Not router 0")
        self.assertEquals(args.mode, "power", "Wrong Mode")
        self.assertTrue(args.off)

        args = self.parser.parse_args(["power", "-on"])
        self.assertTrue(args.all)
        self.assertTrue(args.on)

    def test_start(self):
        pass

    def test_results(self):
        pass

    def test_register_key(self):
        args = self.parser.parse_args(["register_key", "-r", "0", "1", "2"])
        self.assertEquals(args.mode, "register_key", "Wrong Mode")
        self.assertEquals(args.routers, [0, 1, 2], "Routers not correct")
        self.assertFalse(args.all)

        args = self.parser.parse_args(["register_key"])
        self.assertEquals(args.mode, "register_key", "Wrong Mode")
        self.assertTrue(args.all)

    def test_show_jobs(self):
        args = self.parser.parse_args(["show_jobs", "-r", "0"])
        self.assertFalse(args.all)
        self.assertEquals(args.router, [0], "Wrong Router")
        self.assertEquals(args.mode, "show_jobs")

        args = self.parser.parse_args(["show_jobs"])
        self.assertTrue(args.all)
        self.assertEquals(args.mode, "show_jobs")


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
        config_path = os.path.join(base_dir, 'framework_unittests/configs/config_no_vlan')
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

        # assumes that there is only one test in the set
        while self.server_proxy.get_routers_task_queue_size(0):
                    time.sleep(2)
                    print('.', end="", flush=True)
        assert len(self.server_proxy.get_test_results())

        response = os.system(self.path_cli + " start -s set_1")
        assert response == 0

        routers = self.server_proxy.get_routers()
        for router in routers:
            while self.server_proxy.get_routers_task_queue_size(router.id):
                    time.sleep(2)
                    print('.', end="", flush=True)
        assert len(self.server_proxy.get_test_results()) == len(routers) + 1

        os.system(self.path_cli + " results -rm")
        response = os.system(self.path_cli + " start -s set_1 -r 0 -b")
        assert response == 0
        assert len(self.server_proxy.get_test_results()) == 1

    def test_cli_test_results(self):
        assert not os.system(self.path_cli + " results -rm")
        os.system(self.path_cli + " start -s set_1")

        routers = self.server_proxy.get_routers()
        for router in routers:
            while self.server_proxy.get_routers_task_queue_size(router.id):
                    time.sleep(2)
                    print('.', end="", flush=True)

        response = os.system(self.path_cli + " results -r 0")
        assert response == 0
        response = os.system(self.path_cli + " results")
        assert response == 0

        response = os.system(self.path_cli + " results -rm")
        assert response == 0
        response = os.system(self.path_cli + " results -rm")
        assert response == 0
        response = os.system(self.path_cli + " results -rm -r 0")
        assert response == 0
        assert not len(self.server_proxy.get_test_results())

    def test_get_version(self):
        version = self.server_proxy.get_server_version()
        assert version == Server.VERSION
