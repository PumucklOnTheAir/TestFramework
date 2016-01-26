import unittest
from server.server import Server
from server.router import Router
from multiprocessing import Process
from server.ipc import IPC
import time


class ServerTestCase2(unittest.TestCase):

    proc = None

    @classmethod
    def setUpClass(cls):
        #  starts the IPC server in another(!) process
        cls.proc = Process(target=ServerTestCase2.serverStartWithParams, args=()).start()

        # wait until server is started
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        print("Shutdown server")
        ipc_client = IPC()
        ipc_client.connect()
        server_proxy = ipc_client.get_server_proxy()
        server_proxy.stop()

    @staticmethod
    def serverStartWithParams():
        Server.start()

    def setUp(self):
        self.ipc_client = IPC()
        self.ipc_client.connect()
        self.server_proxy = self.ipc_client.get_server_proxy()

        # wait until server has all tasks before executed
        for i in range(2):  # do it two times to be sure
            routers = self.server_proxy.get_routers()
            for router in routers:
                while len(self.server_proxy.get_routers_task_queue(router.id)):
                    time.sleep(2)
    '''
    def test_get_routers(self):
        routers = self.server_proxy.get_routers()
        assert len(routers) != 0
        assert isinstance(routers[0], Router)
    '''
    def test_little_self_check(self):
        print("Test")
        '''
        started = self.server_proxy.start_test(0, "ConnectionTest")
        assert started

        # wait until tests are done
        while not self.server_proxy.get_reports():
            time.sleep(2)

        reports = self.server_proxy.get_reports()
        assert len(reports) != 0
        assert len(reports[-1].errors) == 0  # check last report
        '''
    '''
    def test_long_self_check(self):
        started = self.server_proxy.start_test(0, "VeryLongTest")
        assert started
        time.sleep(5)

        self.server_proxy.stop_all_tasks()

        time.sleep(2)

        reports = self.server_proxy.get_reports()
        assert len(reports) != 0
        assert reports[-1].wasSuccessful()  # check last report
    '''
