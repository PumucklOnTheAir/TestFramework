from abc import ABCMeta
from unittest import TestCase
from network.remote_system import RemoteSystem
from network.remote_system import RemoteSystemJob
from unittest.result import TestResult
#RemoteSystemJob


class FirmwareTest(TestCase, RemoteSystemJob, metaclass=ABCMeta):

    def run(self, result=None) -> TestResult:
        return TestCase.run(result)

    def pre_process(self, server):
        pass

    def post_process(self, data) -> None:
        pass


