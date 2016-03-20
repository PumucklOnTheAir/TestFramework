from server.test import FirmwareTest
from network.network_ctrl import NetworkCtrl


class TestGateway(FirmwareTest):
    """
    Test if an internet-connection exists.
    Therefore two PINGs are send one to "google (8.8.8.8)" and one to "freifunk.net"
    """""

    def test_connection(self):
        network_ctrl = NetworkCtrl(self.remote_system)
        network_ctrl.connect_with_remote_system()
        ping_result1 = network_ctrl.send_command("ping -c 5 8.8.8.8 | grep received")
        ping_result2 = network_ctrl.send_command("ping -c 5 freifunk.net | grep received")
        assert (self._ping_successful(ping_result1[0]) or self._ping_successful(ping_result2[0]))
        network_ctrl.exit()

    def _ping_successful(self, ping_result: str)->bool:
        for i in range(0, 5):
            tmp = str(5 - i) + " packets received"
            if tmp in ping_result:
                return True
        return False
