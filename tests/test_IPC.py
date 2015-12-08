from unittest import TestCase
from server.ipc import IPC
from server.serverproxy import ServerProxy
from server.proxyobject import ProxyObject
from multiprocessing.managers import BaseProxy
import time


class TestIPC(TestCase):
    def test_start_ipc_server(self):

        dummy_runtime_server = DummyServer

        ipc_server = IPC()
        ipc_server.start_ipc_server(dummy_runtime_server)

        time.sleep(5)

        ipc_client = IPC()
        ipc_client.connect()
        server_proxy = ipc_client.get_server_proxy()

        assert not issubclass(server_proxy, ServerProxy)
        assert isinstance(server_proxy, BaseProxy)

        routers = server_proxy.get_routers()
        assert routers[0] == "lol"

        ipc_server.shutdown()

    def test_proxy_object(self):
        dummy_runtime_server = DummyServer

        ipc_server = IPC()
        ipc_server.start_ipc_server(dummy_runtime_server)

        time.sleep(5)

        ipc_client = IPC()
        ipc_client.connect()
        server_proxy = ipc_client.get_server_proxy()

        rep = server_proxy.get_reports()
        #  print(rep)
        assert rep[0] == rep[1].get_id()
        assert rep[2] == rep[1].get_id()
        assert rep[1].text == "test"

        ipc_server.shutdown()
        pass


class DummyServer(ServerProxy):
    @classmethod
    def start_test(cls, router_id, test_id):
        pass

    @classmethod
    def get_running_tests(cls) -> []:
        pass

    @classmethod
    def get_routers(cls) -> []:
        return ["lol"]

    @classmethod
    def get_reports(cls) -> []:
        d = DummyObject("test")
        return [id(d), d, d.get_id()]

    @classmethod
    def get_tests(cls) -> []:
        pass

    @classmethod
    def get_firmwares(cls) -> []:
        pass


class DummyObject(ProxyObject):
    def __init__(self, input_text):
        ProxyObject.__init__(self)
        self.text = input_text
