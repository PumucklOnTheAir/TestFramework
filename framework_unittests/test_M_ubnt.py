from unittest import TestCase
from pyroute2 import netns
from network.nv_assist import NVAssistent
from multiprocessing import Process, Queue
from power_strip.power_strip_control import PowerStripControl
from power_strip.ubnt import Ubnt
from network.network_ctrl import NetworkCtrl


class TestUbnt(TestCase):
    """
    This TestCase checks the functionality of the power strip Ubiquiti mPower Pro(EU)
    """

    def test_power(self):
        ps = self.create_powerstrip()
        global network_ctrl
        network_ctrl = NetworkCtrl(ps)
        # Port
        port = 1
        q = Queue()
        p = Process(target=self._power_off, args=(ps, q, port))
        p.start()
        print("Turn off the power...")
        p.join()

        result = self._check_port(ps, port)
        print("Port " + str(port) + " is switched to " + str(result))

        p2 = Process(target=self._power_on, args=(ps, q, port))
        p2.start()
        print("Turn on the power...")
        p2.join()

    def _check_port(self, ps: Ubnt, port: int):
        network_ctrl.connect_with_remote_system()
        cmd = ps.port_status(port)
        result = network_ctrl.send_command(cmd)
        return result

    def _power_on(self, ps: Ubnt, q: Queue, port: int):
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan(ps)
        netns.setns(ps.namespace_name)

        power_on = PowerStripControl(ps, True, port)
        power_on.start()
        power_on.join()

        nv_assist.close()
        q.put(ps)

    def _power_off(self, ps: Ubnt, q: Queue, port: int):
        nv_assist = NVAssistent("eth0")
        nv_assist.create_namespace_vlan(ps)
        netns.setns(ps.namespace_name)

        power_on = PowerStripControl(ps, True, port)
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
