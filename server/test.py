from abc import ABCMeta
from unittest import TestCase
from network.remote_system import RemoteSystemJob


class FirmwareTest(TestCase, RemoteSystemJob, metaclass=ABCMeta):

    def __init__(self, methodName='runTest'):
        TestCase.__init__(self, methodName)
        RemoteSystemJob.__init__(self)

    def pre_process(self, server):
        pass

    def post_process(self, data) -> None:
        pass


