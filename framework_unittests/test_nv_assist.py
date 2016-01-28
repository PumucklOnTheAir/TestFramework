from unittest import TestCase
from network.nv_assist import NVAssistent
from server.router import Router, Mode
from os import getpid
import time


class TestNVAssist(TestCase):

    @staticmethod
    def use_nv_assist(router: Router):
        print(str(getpid()))
        nv_assi = NVAssistent("eth0")
        nv_assi.create_namespace_vlan_veth(router)
        nv_assi.close()

    def test_create_namespace_vlan_veth(self):
        print(getpid())
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.configuration
        assert isinstance(router, Router)

        print("Test1:")
        nv_assi = NVAssistent("eth0")
        nv_assi.create_namespace_vlan(router.namespace_name, "eth0", router.vlan_iface_name, router.vlan_iface_id)
        assert isinstance(nv_assi, NVAssistent)
        nv_assi.close()

        print("Test2:")
        nv_assi = NVAssistent("eth0")
        nv_assi.create_namespace_vlan(router.namespace_name, "eth0", router.vlan_iface_name, router.vlan_iface_id)
        assert isinstance(nv_assi, NVAssistent)
        nv_assi.close()
'''
        time.sleep(2)
        print("Test2:")
        nv_assi = NVAssistent("eth0")
        nv_assi.create_namespace_vlan_veth(router)
        assert isinstance(nv_assi, NVAssistent)
        nv_assi.close()
'''

        # Oder in einem anderen Prozess ausführbar. (beendet sich allerdings nicht automatisch)
        #from multiprocessing import Process
        #p=Process(target=self.use_nv_assist,args=(router,))
        #p.start()
        #p.join()