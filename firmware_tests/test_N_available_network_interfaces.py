from server.test import FirmwareTest
from router.router import Mode
import logging
from log.loggersetup import LoggerSetup


class TestAvailableNetworkInterfaces(FirmwareTest):
    """
    Tests the availability of specific network-interfaces in the normal-mode.
    (bat0, br-client, br-wan, client0, eth0, eth1, lo, local-node, mesh-vpn, mesh0)
    """""

    def test_availability(self):
        """
        Test:
            1. Router is in normal-mode
            2. All necessary network-interfaces exist
        """
        necessary_network_interfaces = ["bat0", "br-client", "br-wan", "client0", "eth0",
                                        "eth1", "lo", "local-node", "mesh-vpn", "mesh0"]
        logging.debug("%sTest: Following Network-Interfaces have to exist in normal-mode: " +
                      str(necessary_network_interfaces), LoggerSetup.get_log_deep(1))
        assert self.remote_system.mode == Mode.normal
        logging.debug("%s[" + u"\u2714" + "] Correct Mode", LoggerSetup.get_log_deep(2))
        existing_network_interfaces = self.remote_system.network_interfaces.values()
        existing_network_interfaces = [interface.name for interface in existing_network_interfaces]
        common_network_interfaces = list(set(necessary_network_interfaces) & set(existing_network_interfaces))
        self.assertTrue(len(common_network_interfaces) >=
                        len(necessary_network_interfaces), "Some Network-Interfaces are missing")
        logging.debug("%s[" + u"\u2714" + "] All specified Network-Interfaces exist", LoggerSetup.get_log_deep(2))
