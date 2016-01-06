from abc import ABCMeta
from unittest import TestCase
from .router import Router
#  from network.network_ctrl import NetworkCtrl
# from .server import Server
from log.logger import Logger


class AbstractTest(TestCase, metaclass=ABCMeta):
    def runTest(self):
        TestCase.runTest(self)


    def prepare(self, router: Router):
        #self.__router = router
        Logger().debug("TestCase prepare", 3)

        #if Server.VLAN:
        #   self.__prepare_vlan()
        # TOO get server importet

    def __prepare_vlan(self):
        return False
        # TODO proof if this is right
        # NetworkCtrl(self.__router)
        # network_ctrl.connect_with_router()


