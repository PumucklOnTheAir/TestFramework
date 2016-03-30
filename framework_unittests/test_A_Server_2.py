import unittest
from server.server import Server
from router.router import Router
from multiprocessing import Process
from server.ipc import IPC
import time
import os
import socket
import datetime


def block_until_server_is_online():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("wait", flush=True)
    while sock.connect_ex(('localhost', 5000)):
        time.sleep(3)
        print('.', end="", flush=True)
    sock.close()
    print("server is online", flush=True)


class ServerCore(object):

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        print("Shutdown server")
        ipc_client = IPC()
        ipc_client.connect()
        server_proxy = ipc_client.get_server_proxy()

        # wait until server has all tasks before executed
        for i in range(2):  # do it two times to be sure
            routers = server_proxy.get_routers()
            for router in routers:
                while server_proxy.get_routers_task_queue_size(router.id):
                    time.sleep(2)
                    print('.', end="", flush=True)

        server_proxy.stop()

    def setUp(self):
        self.ipc_client = IPC()
        self.ipc_client.connect()
        self.server_proxy = self.ipc_client.get_server_proxy()

        # wait until server has all tasks before executed
        for i in range(2):  # do it two times to be sure
            routers = self.server_proxy.get_routers()
            for router in routers:
                while self.server_proxy.get_routers_task_queue_size(router.id):
                    time.sleep(2)
                    print('.', end="", flush=True)

    def tearDown(self):
        assert not len(self.server_proxy.get_task_errors())  # check if an error happens

    def test_get_routers(self):
        routers = self.server_proxy.get_routers()
        assert len(routers) != 0
        assert isinstance(routers[0], Router)

    def test_test_set(self):
        started = self.server_proxy.start_test_set(0, "set_1")

        assert started

        # wait until tests are done, assumes that exactly two tests are already finished
        while not len(self.server_proxy.get_test_results()) == 2:
            time.sleep(2)
            print('.', end="", flush=True)

        reports = self.server_proxy.get_test_results()
        assert len(reports) == 2
        assert len(reports[-1][2].errors) == 0  # check last report

        started = self.server_proxy.start_test_set(0, "set_0")

        assert started

        # wait until tests are done, assumes that exactly two tests are already finished
        while not len(self.server_proxy.get_test_results()) == 3:
            time.sleep(2)
            print('.', end="", flush=True)

        reports = self.server_proxy.get_test_results()
        assert len(reports) == 3
        assert len(reports[2][-1].errors) == 0  # check last report

    def test_test_results(self):
        self.server_proxy.delete_test_results()

        started = self.server_proxy.start_test_set(0, "set_1")
        assert started

        while not len(self.server_proxy.get_test_results()) == 2:
            time.sleep(2)
            print('.', end="", flush=True)

        reports = self.server_proxy.get_test_results()

        for report in reports:
            assert report[0] == 0
            assert report[1] != ""
            assert len(report[2].errors) == 0

        removed_results = self.server_proxy.delete_test_results()
        assert len(reports) == removed_results
        time.sleep(0.5)
        assert not len(self.server_proxy.get_test_results())

    def test_blocked_execution(self):
        self.server_proxy.delete_test_results()
        start = datetime.datetime.now()
        started = self.server_proxy.start_test_set(0, "set_1", 300)
        assert started
        stop = datetime.datetime.now()

        # magic value - we assume that non-blocking execution of the method would be faster
        assert stop - start > datetime.timedelta(seconds=2)


class ServerTestCase2(ServerCore, unittest.TestCase):
    proc = None

    @classmethod
    def setUpClass(cls):
        #  starts the IPC server in another(!) process
        cls.proc = Process(target=ServerTestCase2.serverStartWithParams, args=()).start()
        block_until_server_is_online()

    @staticmethod
    def serverStartWithParams():
        base_dir = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
        config_path = os.path.join(base_dir, 'framework_unittests/configs/config_no_vlan')
        Server.start(config_path=config_path)
