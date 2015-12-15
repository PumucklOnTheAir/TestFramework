from abc import ABCMeta
from unittest import TestCase
from .router import Router
from network.network_ctrl import NetworkCtrl
from server.server import Server


class AbstractTest(metaclass=ABCMeta, TestCase):
    def __init__(self):
        self.thread = None

    def prepare(self, router: Router):
        self.__router = router

        if Server.VLAN:
            self.__prepare_vlan()

    def __prepare_vlan(self):
        # TODO proof if this is right
        NetworkCtrl(self.__router)
        # network_ctrl.connect_with_router()

