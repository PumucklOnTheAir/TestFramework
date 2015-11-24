from unittest import TestCase
from server.ipc import IPC
from server.serverproxy import ServerProxy
from server.proxyobject import ProxyObject
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

        #assert issubclass(server_proxy, ServerProxy) it's not - it is a proxy model

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
        #print(rep)
        assert rep[0] == rep[1].get_id()
        assert rep[2] == rep[1].get_id()
        assert rep[1].text == "test"

        ipc_server.shutdown()
        pass


class DummyServer(ServerProxy):
    def start_test(self, router_id, test_id):
        pass

    def get_running_tests(self) -> []:
        pass

    def get_routers(self) -> []:
        return ["lol"]

    def get_reports(self) -> []:
        d = DummyObject("test")
        return [id(d), d, d.get_id()]

    def get_tests(self) -> []:
        pass

    def get_firmwares(self) -> []:
        pass


class DummyObject(ProxyObject):
    def __init__(self, input_text):
        ProxyObject.__init__(self)
        self.text = input_text
