from multiprocessing.managers import BaseManager, Server
from server.serverproxy import ServerProxy


class IPC(BaseManager):
    """Inter-process communication server and client.
    This class is used to exchange data between the test server runtime and
    clients like user interfaces such as CLI and WebServer.
    """""

    _server_object = None  # docs.python.org/3.5/library/multiprocessing.html#multiprocessing.managers.BaseManager

    def __init__(self):
        BaseManager.__init__(self, address=('127.0.0.1', 5000), authkey=b'abc42')

    def start_ipc_server(self, server, serve_forever: bool=False):
        """Start the ipc server to allow clients to connect
        :param server: The running test server to represent
        :param serve_forever: The true, the statement is
            blocking until the shutdown() method was called
        """
        assert issubclass(server, ServerProxy)
        self.register('get_server_proxy', server)

        if serve_forever:
            self._server_object = self.get_server()
            self._server_object.serve_forever()
        else:
            self.start()

    def __prepare_client(self):
        self.register('get_server_proxy')
        pass

    def connect(self, prepare_client=True):
        if prepare_client:
            self.__prepare_client()

        super(IPC, self).connect()

    def get_server_proxy(self) -> ServerProxy:
        """Returns a proxy model for the test server"""
        pass

    def shutdown(self):
        if self._server_object is None:
            super.shutdown()
        else:
            self._server_object.stop_event.set()
            # purpose to include this function into the main python lib...

