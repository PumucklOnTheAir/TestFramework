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
        self.assertFalse(args.router)
        self.assertEquals(args.mode, "status", "Wrong Mode")

        args = self.parser.parse_args(["status", "-r", "1"])
        self.assertTrue(args.router)
        self.assertEquals(args.mode, "status", "Wrong Mode")
        self.assertEquals(args.router, [1], "Wrong Router")

    def test_sysupgrade(self):
        args = self.parser.parse_args(["sysupgrade"])
        self.assertFalse(args.routers)
        self.assertFalse(args.n)
        self.assertEquals(args.mode, "sysupgrade", "Wrong Mode")

        args = self.parser.parse_args(["sysupgrade", "-r", "1", "2", "3", "-n"])
        self.assertEquals(args.routers, [1, 2, 3], "Wrong Routers")
        self.assertTrue(args.n)
        self.assertEquals(args.mode, "sysupgrade", "Wrong Mode")

    def test_sysupdate(self):
        args = self.parser.parse_args(["sysupdate", "-r", "1", "2", "3"])
        self.assertEquals(args.routers, [1, 2, 3], "Wrong Routers")
        self.assertEquals(args.mode, "sysupdate", "Wrong Mode")

        args = self.parser.parse_args(["sysupdate"])
        self.assertFalse(args.routers)
        self.assertEquals(args.mode, "sysupdate", "Wrong Mode")

    def test_reboot(self):
        args = self.parser.parse_args(["reboot", "-c"])
        self.assertFalse(args.routers)
        self.assertTrue(args.config)
        self.assertEquals(args.mode, "reboot", "Wrong Mode")

        args = self.parser.parse_args(["reboot"])
        self.assertFalse(args.routers)
        self.assertFalse(args.config)
        self.assertEquals(args.mode, "reboot", "Wrong Mode")

        args = self.parser.parse_args(["reboot", "-c"])
        self.assertTrue(args.config)
        self.assertEquals(args.mode, "reboot", "Wrong Mode")

        args = self.parser.parse_args(["reboot", "-r", "1", "2", "3", "-c"])
        self.assertTrue(args.config)
        self.assertEquals(args.routers, [1, 2, 3], "Wrong Routers")
        self.assertEquals(args.mode, "reboot", "Wrong Mode")

    def test_webconfig(self):
        args = self.parser.parse_args(["webconfig", "-r", "1", "2", "3"])
        self.assertEquals(args.routers, [1, 2, 3], "Wrong Routers")
        self.assertEquals(args.mode, "webconfig", "Wrong Mode")
        self.assertFalse(args.wizard)

        args = self.parser.parse_args(["webconfig", "-w"])
        self.assertFalse(args.routers)
        self.assertEquals(args.mode, "webconfig", "Wrong Mode")
        self.assertTrue(args.wizard)

    def test_update_info(self):
        args = self.parser.parse_args(["info", "-r", "1", "2", "3"])
        self.assertEquals(args.routers, [1, 2, 3], "Wrong Routers")
        self.assertEquals(args.mode, "info", "Wrong Mode")

        args = self.parser.parse_args(["info"])
        self.assertFalse(args.routers)
        self.assertEquals(args.mode, "info", "Wrong Mode")

    def test_online(self):
        args = self.parser.parse_args(["online", "-r", "1", "2", "3"])
        self.assertEquals(args.routers, [1, 2, 3], "Wrong Routers")
        self.assertEquals(args.mode, "online", "Wrong Mode")

        args = self.parser.parse_args(["online"])
        self.assertFalse(args.routers)
        self.assertEquals(args.mode, "online", "Wrong Mode")

    def test_power(self):
        args = self.parser.parse_args(["power", "-r", "0", "--off"])
        self.assertEquals(args.routers, [0], "Not router 0")
        self.assertEquals(args.mode, "power", "Wrong Mode")
        self.assertTrue(args.off)

        args = self.parser.parse_args(["power", "--on"])
        self.assertFalse(args.routers)
        self.assertTrue(args.on)

    def test_start(self):
        args = self.parser.parse_args(["start", "-s", "set_1", "-b"])
        self.assertEquals(args.mode, "start", "Wrong Mode")
        self.assertFalse(args.routers)
        self.assertTrue(args.blocking)
        self.assertEquals(args.set, "set_1", "Wrong Set")

        args = self.parser.parse_args(["start", "-s", "set_2", "-r", "5"])
        self.assertEquals(args.set, "set_2", "Wrong Set")
        self.assertFalse(args.blocking)
        self.assertEquals(args.routers, [5], "Wrong Router")

    def test_results(self):
        args = self.parser.parse_args(["results"])
        self.assertEquals(args.mode, "results", "Wrong Mode")
        self.assertFalse(args.router)

        args = self.parser.parse_args(["results", "-d"])
        self.assertTrue(args.remove)
        self.assertFalse(args.router)

        args = self.parser.parse_args(["results", "-e", "0"])
        self.assertFalse(args.router)
        self.assertEquals(args.errors, [0], "Wrong List Index")

        args = self.parser.parse_args(["results", "-f", "1"])
        self.assertFalse(args.router)
        self.assertEquals(args.failures, [1], "Wrong List Index")

    def test_register_key(self):
        args = self.parser.parse_args(["register", "-r", "0"])
        self.assertEquals(args.mode, "register", "Wrong Mode")
        self.assertEquals(args.routers, [0], "Routers not correct")

        args = self.parser.parse_args(["register"])
        self.assertEquals(args.mode, "register", "Wrong Mode")
        self.assertFalse(args.routers)

    def test_show_jobs(self):
        args = self.parser.parse_args(["jobs", "-r", "0"])
        self.assertEquals(args.router, [0], "Wrong Router")
        self.assertEquals(args.mode, "jobs")

        args = self.parser.parse_args(["jobs"])
        self.assertFalse(args.router)
        self.assertEquals(args.mode, "jobs")


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

    def test_test_sets(self):
        response = os.system(self.path_cli + " sets")
        assert response == 0
        response = os.system(self.path_cli + " sets -s set_0")
        assert response == 0

    def test_cli_start_test_set(self):
        response = os.system(self.path_cli + " start -s set_0 -r 0")
        assert response == 0

        # assumes that there is only one test in the set
        while self.server_proxy.get_routers_task_queue_size(0):
                    time.sleep(2)
                    print('.', end="", flush=True)
        assert len(self.server_proxy.get_test_results())

        os.system(self.path_cli + " results -d")
        response = os.system(self.path_cli + " start -s set_0")
        assert response == 0

        routers = self.server_proxy.get_routers()
        for router in routers:
            while self.server_proxy.get_routers_task_queue_size(router.id):
                    time.sleep(2)
                    print('.', end="", flush=True)
        assert len(self.server_proxy.get_test_results()) == len(routers)

        os.system(self.path_cli + " results -d")
        response = os.system(self.path_cli + " start -s set_0 -r 0 -b")
        assert response == 0
        assert len(self.server_proxy.get_test_results()) == 1

    def test_cli_test_results(self):
        assert not os.system(self.path_cli + " results -d")
        os.system(self.path_cli + " start -s set_0")

        routers = self.server_proxy.get_routers()
        for router in routers:
            while self.server_proxy.get_routers_task_queue_size(router.id):
                    time.sleep(2)
                    print('.', end="", flush=True)

        response = os.system(self.path_cli + " results -r 0")
        assert response == 0
        response = os.system(self.path_cli + " results")
        assert response == 0

        response = os.system(self.path_cli + " results -d")
        assert response == 0
        response = os.system(self.path_cli + " results -d")
        assert response == 0
        response = os.system(self.path_cli + " results -d -r 0")
        assert response == 0
        assert not len(self.server_proxy.get_test_results())

    def test_get_version(self):
        version = self.server_proxy.get_server_version()
        assert version == Server.VERSION
