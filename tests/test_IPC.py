from unittest import TestCase
from server.ipc import IPC
from server.serverproxy import ServerProxy
import time


class TestIPC(TestCase):

  def test_start_ipc_server(self):
    dummy_runtime_server = DummyServer
    #dummy_runtime_server = ServerProxy

    ipc_server = IPC()
    ipc_server.start_ipc_server(dummy_runtime_server)

    time.sleep(2)

    ipc_client = IPC()
    ipc_client.connect()
    server_proxy = ipc_client.get_server_proxy()
    #print(server_proxy.get_routers())
    #print(server_proxy)
    #assert issubclass(server_proxy, ServerProxy)

    routers = server_proxy.get_routers()
    assert routers[0] == "lol"

    #ipc_server.shutdown()

  def test_get_server_proxy(self):
    self.fail()


class DummyServer(ServerProxy):


    def start_test(self, router_id, test_id):
        pass

    def get_running_tests(self) -> []:
        pass

    def get_routers(self):
        return ["lol"]
        pass

    def get_reports(self) -> []:
        pass


    def get_tests(self) -> []:
        pass


    def get_firmwares(self) -> []:
        pass