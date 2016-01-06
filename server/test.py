from abc import ABCMeta
from unittest import TestCase
from .router import RouterTask


class FirmwareTest(TestCase, RouterTask, metaclass=ABCMeta):
    pass
