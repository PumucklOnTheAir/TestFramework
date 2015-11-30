from multiprocessing.managers import BaseManager
from server.serverproxy import ServerProxy


class IPC(BaseManager):
    """Inter-process communication server and client.
    This class is used to exchange data between the test server runtime and
    clients like user interfaces such as CLI and WebServer.
    """""

    def __init__(self):
        BaseManager.__init__(self, address=('127.0.0.1', 5000), authkey=b'abc42')

    def start_ipc_server(self, server):
        """Start the ipc server to allow clients to connect
        :param server: The running test server to represent
        """
        assert issubclass(server, ServerProxy)
        self.register('get_server_proxy', server)

        self.start()

    def get_server_proxy(self) -> ServerProxy:
        """Returns a proxy model for the test server"""
        pass
