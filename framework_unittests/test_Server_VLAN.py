from server.server import Server
from framework_unittests.test_Server_2 import ServerTestCase2


class ServerTestCaseVLAN(ServerTestCase2):

    proc = None

    @staticmethod
    def serverStartWithParams():
        Server.start()
