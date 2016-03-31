from typing import List


class BatOriginator:
    """
    This class represents a node in the mesh-network, which the Router is connected to.
    """""

    def __init__(self, mac: str, last_seen: float, next_hop: str, outgoing_iface: str, potential_next_hops: List):
        """
        :param mac: address of the mesh-node
        :param last_seen: seconds since the last message-exchange
        :param next_hop: the originator is best achieved through the node with this mac-address
        :param potential_next_hops: alternative nodes the can be used if "next_hop" fails
        """
        self._mac = mac
        self._last_seen = last_seen
        self._next_hop = next_hop
        self._outgoing_iface = outgoing_iface
        self.potential_next_hops = potential_next_hops

    @property
    def mac(self) -> str:
        """
        The mac-address of the originator.

        :return: BatOriginator_mac
        """
        return self._mac

    @mac.setter
    def mac(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._mac = value

    @property
    def last_seen(self) -> float:
        """
        Seconds since the last message-exchange.

        :return: BatOriginator_last_seen
        """
        return self._last_seen

    @last_seen.setter
    def last_seen(self, value: float):
        """
        :type value: float
        """
        assert isinstance(value, float)
        self._last_seen = value

    @property
    def next_hop(self) -> str:
        """
        The originator is best achieved through the node with this mac-address.

        :return: BatOriginator_next_hop
        """
        return self._next_hop

    @next_hop.setter
    def next_hop(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._next_hop = value

    @property
    def outgoing_iface(self) -> str:
        """
        The used network interface.(like: mesh0)

        :return: BatOriginator_outgoing_iface
        """
        return self._outgoing_iface

    @outgoing_iface.setter
    def outgoing_iface(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._outgoing_iface = value

    def __str__(self):
        bat_o_str = self.mac + " " + str(self.last_seen) + "s " + self.next_hop + " " + self.outgoing_iface + " {"
        for hop in self.potential_next_hops:
            bat_o_str += " " + hop
        bat_o_str += " }"
        return bat_o_str
