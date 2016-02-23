from server.test import FirmwareTest
import os


class ConnectionTest(FirmwareTest):
    """
    This is a demo test - only to test the functionality of the framework itself.
    """""
    def test_self_router(self):
        # print(str(self.router))
        assert self.remote_system.id == 0

    def test_ping_static(self):
        # print("connection test: " + str(getpid()))
        # os.system("ip a")
        response = os.system("ping -t 5 -c 1 " + "www.p8h.de")
        assert response == 0  # not working because no normal eth0 stack available
        # from subprocess import Popen, PIPE
        # process = Popen(["ip", "a"], stdout=PIPE, stderr=PIPE)
        # stdout, sterr = process.communicate()
        # print(str(stdout.decode('utf-8')))
        # response = os.system("ping -c 1 " + "p8h.de")
        # assert response == #0

    def test_ping_router(self):
        hostname = self.remote_system.ip
        response = os.system("ping -t 5 -c 1 " + hostname)
        print(hostname)
        assert response == 0


class VeryLongTest(FirmwareTest):

    def test_very_long_test(self):
        lol = True
        assert lol
        assert not not lol

    def test_buzz1(self):
        lol = True
        assert lol
        assert not not lol

    def test_foo2(self):
        lol = True
        assert lol
        assert not not lol
