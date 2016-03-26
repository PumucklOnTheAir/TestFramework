from unittest import TestCase
from router.bat_originator import BatOriginator


class TestBatOriginator(TestCase):

    def test_create_BatOriginator(self):
        bat_originator = BatOriginator("f6:f6:6d:85:d4:ae", 0.840, "32:b8:c3:e7:6f:f0",
                                       "mesh0", ["02:2a:1a:cc:72:ae", "32:b8:c3:e7:96:b0", "32:b8:c3:e7:6f:f0"])
        assert isinstance(bat_originator, BatOriginator)

        self.assertEqual("f6:f6:6d:85:d4:ae", bat_originator.mac)
        self.assertEqual(0.840, bat_originator.last_seen)
        self.assertEqual("32:b8:c3:e7:6f:f0", bat_originator.next_hop)
        self.assertEqual("mesh0", bat_originator.outgoing_iface)
        self.assertEqual(["02:2a:1a:cc:72:ae", "32:b8:c3:e7:96:b0", "32:b8:c3:e7:6f:f0"],
                         bat_originator.potential_next_hops)

    def test_setter(self):
        bat_originator = BatOriginator("", 0.0, "", "", [])
        assert isinstance(bat_originator, BatOriginator)

        bat_originator.mac = "f6:f6:6d:85:d4:ae"
        bat_originator.last_seen = 0.840
        bat_originator.next_hop = "32:b8:c3:e7:6f:f0"
        bat_originator.outgoing_iface = "mesh0"
        bat_originator.potential_next_hops = ["02:2a:1a:cc:72:ae", "32:b8:c3:e7:96:b0", "32:b8:c3:e7:6f:f0"]

        self.assertEqual("f6:f6:6d:85:d4:ae", bat_originator.mac)
        self.assertEqual(0.840, bat_originator.last_seen)
        self.assertEqual("32:b8:c3:e7:6f:f0", bat_originator.next_hop)
        self.assertEqual("mesh0", bat_originator.outgoing_iface)
        self.assertEqual(["02:2a:1a:cc:72:ae", "32:b8:c3:e7:96:b0", "32:b8:c3:e7:6f:f0"], bat_originator.potential_next_hops)