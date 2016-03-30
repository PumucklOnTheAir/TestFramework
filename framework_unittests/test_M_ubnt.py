from unittest import TestCase
from pyroute2 import netns
from network.nv_assist import NVAssistent
from multiprocessing import Process, Queue
from power_strip.power_strip_control import PowerStripControl
from power_strip.ubnt import Ubnt
from network.network_ctrl import NetworkCtrl
from router.router import Router, Mode


class TestUbnt(TestCase):
    """
    This TestCase checks the functionality of the power strip Ubiquiti mPower Pro(EU)
    """

    def test_power(self):
        ps = self.create_powerstrip()
        self.router = self._create_router()
        global network_ctrl
        network_ctrl = NetworkCtrl(ps)
        # Port
        port = 1
        q = Queue()
        p = Process(target=self._power_off, args=(ps, q, port))
        p.start()
        print("Turn off the power...")
        p.join()

        p2 = Process(target=self._power_on, args=(ps, q, port))
        p2.start()
        print("Turn on the power...")
        p2.join()

    def _power_on(self, ps: Ubnt, q: Queue, port: int):
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan(ps)
        netns.setns(ps.namespace_name)

        power_on = PowerStripControl(self.router, ps, True, port)
        power_on.start()
        power_on.join()

        nv_assist.close()
        q.put(ps)

    def _power_off(self, ps: Ubnt, q: Queue, port: int):
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan(ps)
        netns.setns(ps.namespace_name)

        power_on = PowerStripControl(self.router, ps, False, port)
        power_on.start()
        power_on.join()

        nv_assist.close()
        q.put(ps)

    def create_powerstrip(self) -> Ubnt:
        # Create powerstrip
        ps = Ubnt(0, "vlan20", 20, "192.168.1.20", 24, "ubnt", "ubnt", 6)
        assert isinstance(ps, Ubnt)
        assert ps.id == 0
        assert ps.vlan_iface_name == "vlan20"
        assert ps.vlan_iface_id == 20
        assert ps.ip == "192.168.1.20"
        assert ps.ip_mask == 24
        assert ps.usr_name == "ubnt"
        assert ps.usr_password == "ubnt"
        assert ps.n_ports == 6
        return ps

    def _create_router(self):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.normal
        assert isinstance(router, Router)
        return router
