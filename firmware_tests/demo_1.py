from server.test import FirmwareTest
import os


class ConnectionTest(FirmwareTest):
    """
    This is a demo test - only to test the functionality of the framework itself.
    """""
    def test_self_router(self):
        assert self.remote_system.id == 0

    def test_ping_local(self):
        response = os.system("ping -t 5 -c 1 " + "localhost")
        assert response == 0
