from server.test import FirmwareTest
from network.remote_system import RemoteSystemJob
import time
import os


class ConnectionTest(FirmwareTest):

    def test_self_router(self):
        # print(str(self.router))
        assert self.remote_system.id == 0

    def test_ping_static(self):
        response = os.system("ping -t 2 -c 1 " + "p8h.de")
        assert response == 0  # not working because no normal eth0 stack available
        # from subprocess import Popen, PIPE
        # process = Popen(["ip", "a"], stdout=PIPE, stderr=PIPE)
        # stdout, sterr = process.communicate()
        # print(str(stdout.decode('utf-8')))
        # response = os.system("ping -c 1 " + "p8h.de")
        # assert response == #0

    def test_ping_router(self):
        hostname = self.remote_system.ip
        response = os.system("ping -t 2 -c 1 " + hostname)
        print(hostname)
        assert response == 0


class VeryLongTest(FirmwareTest):

    def test_very_long_test(self):
        lol = True
        assert lol
        #time.sleep(20)
        assert not not lol
        # assert not lol

    def test_buzz1(self):
        # print("buzz1")
        lol = True
        assert lol
        assert not not lol
        # assert not lol

    def test_foo2(self):
        # print("foo2")
        lol = True
        assert lol
        assert not not lol
        # assert not lol


class GeneralJobTest(RemoteSystemJob):
    def run(self):
        print("Hi")

    @staticmethod
    def pre_process(self, server) -> {}:
        return None

    @staticmethod
    def post_process(self, data: {}, server) -> None:
        pass