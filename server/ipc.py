from multiprocessing.managers import BaseManager
from server.serverproxy import ServerProxy
from multiprocessing import Process


class IPC(BaseManager):
    """Inter-process communication server and client.
    This class is used to exchange data between the test server runtime and
    clients like user interfaces such as CLI and WebServer.
    """""

    ipc_server_thread = object
    ipc_server_server = object

    def __init__(self):
        BaseManager.__init__(self, address=('127.0.0.1', 5000), authkey=b'abc42')

    def start_ipc_server(self, server):
        """Start the ipc server to allow clients to connect
        :param server: The running server to represent
        """
        assert issubclass(server, ServerProxy)
        self.register('get_server_proxy', server)

        p = Process(target=self.__start_ipc_server, args=())
        p.start()

        self.ipc_server_thread = p

    def __start_ipc_server(self):
        server = self.get_server()
        server.serve_forever()
        self.ipc_server_server = server
        print("IPC Server started")

    def shutdown(self):
        #self.ipc_server_server.shutdown()
        print("Not implemented!")
    def get_server_proxy(self) -> ServerProxy:
        """Returns a proxy model for the test server """
        pass




