from server.test import FirmwareTest
import os
import time


class ConnectionTest(FirmwareTest):
    """
    This is a demo test - only to test the functionality of the framework itself.
    """""

    @classmethod
    def setUpClass(cls):
        assert cls.remote_system.id == 0

    def test_self_router(self):
        assert self.remote_system.id == 0

    def test_ping_local(self):
        response = os.system("ping -t 5 -c 1 " + "localhost")
        time.sleep(3)
        assert response == 0
