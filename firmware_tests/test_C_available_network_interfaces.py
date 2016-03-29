from server.test import FirmwareTest
from router.router import Mode
from log.loggersetup import LoggerSetup
import logging


class TestAvailableNetworkInterfaces(FirmwareTest):
    """
    Test the availability of specific network-interfaces in the configuration-mode.
    (br-setup, eth1, lo)
    """""

    def test_availability(self):
        """
        Test:
            1. Router is in configuration-mode
            2. All necessary network-interfaces exist
        """
        necessary_network_interfaces = ["br-setup", "eth1", "lo"]
        logging.debug("%sTest: Following Network-Interfaces have to exist in config-mode: " +
                      str(necessary_network_interfaces), LoggerSetup.get_log_deep(1))
        assert self.remote_system.mode == Mode.configuration
        logging.debug("%s[" + u"\u2714" + "] Correct Mode", LoggerSetup.get_log_deep(2))
        existing_network_interfaces = self.remote_system.network_interfaces.values()
        existing_network_interfaces = [interface.name for interface in existing_network_interfaces]
        common_network_interfaces = list(set(necessary_network_interfaces) & set(existing_network_interfaces))
        self.assertTrue(len(common_network_interfaces) >= len(necessary_network_interfaces),
                        "Some Network-Interfaces are missing")
        logging.debug("%s[" + u"\u2714" + "] All specified Network-Interfaces exist", LoggerSetup.get_log_deep(2))
