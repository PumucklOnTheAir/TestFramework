from server.test import FirmwareTest
from network.network_ctrl import NetworkCtrl
from log.loggersetup import LoggerSetup
from router.router import Mode
import logging


class TestGateway(FirmwareTest):
    """
    Tests if an internet-connection exists.
    Therefore two PINGs are send one to "google (8.8.8.8)" and one to "freifunk.net"
    """""

    def test_connection(self):
        """
        Test:
            1. Google or FreiFunk is reachable via a Ping
        """
        logging.debug("%sTest: Existence of an Internet-Connection", LoggerSetup.get_log_deep(1))
        assert self.remote_system.mode == Mode.normal
        logging.debug("%s[" + u"\u2714" + "] Correct Mode", LoggerSetup.get_log_deep(2))
        network_ctrl = NetworkCtrl(self.remote_system)
        network_ctrl.connect_with_remote_system()
        ping_result1 = network_ctrl.send_command("ping -c 5 8.8.8.8 | grep received")
        ping_result2 = network_ctrl.send_command("ping -c 5 freifunk.net | grep received")
        self.assertTrue(self._ping_successful(ping_result1[0]) or self._ping_successful(ping_result2[0]),
                        "No Internet-Connection")
        logging.debug("%s[" + u"\u2714" + "] At least one Ping was successful => An Internet-Connection exist",
                      LoggerSetup.get_log_deep(2))
        network_ctrl.exit()

    def _ping_successful(self, ping_result: str)->bool:
        """
        Tests if at least one of the fife Pings was successful

        :param ping_result: Is a string that contains the Output of ping:
                            '5 packets transmitted, 5 packets received, 0% packet loss, time 4005ms'
        :return: 'True' if one ping was successful
        """
        for i in range(0, 5):
            tmp = str(5 - i) + " packets received"
            if tmp in ping_result:
                return True
        return False
