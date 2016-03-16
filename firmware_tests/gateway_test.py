from server.test import FirmwareTest
from network.network_ctrl import NetworkCtrl
from typing import List


class GatewayTest(FirmwareTest):
    """
    Shouldn't work, because the processes of a Test have no internet access.
    Test if an internet-connection exists.
    Therefore two PINGs are send one to "google (8.8.8.8)" and one to "freifunk.net"
    """""

    def test_connection(self):
        network_ctrl = NetworkCtrl(self.remote_system)
        ping_result1 = network_ctrl.send_command("ping -c 5 8.8.8.8 | grep received")
        ping_result2 = network_ctrl.send_command("ping -c 5 freifunk.net | grep received")
        assert (self._ping_successful(ping_result1) or self._ping_successful(ping_result2))

    def _ping_successful(self, ping_result_lst: List)->bool:
        i = 5
        for ping_result in ping_result_lst:
            if str(i) + " received" in ping_result:
                return True
            i -= 1
        return False