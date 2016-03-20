from server.test import FirmwareTest
from router.router import Mode
import logging


class TestAvailableNetworkInterfaces(FirmwareTest):
    """
    Test the availability of specific network-interfaces in the configuration-mode.
    (br-setup, eth1, lo)
    """""

    def test_availability(self):
        assert self.remote_system.mode == Mode.configuration

        logging.debug("Test ......")
        necessary_network_interfaces = ["br-setup", "eth1", "lo"]
        logging.debug("necessary_network_interfaces: " + str(necessary_network_interfaces))
        existing_network_interfaces = self.remote_system.interfaces.values()
        logging.debug("existing_network_interfaces: " + str(existing_network_interfaces))
        existing_network_interfaces = [interface.name for interface in existing_network_interfaces]
        logging.debug("existing_network_interfaces2: " + str(existing_network_interfaces))
        common_network_interfaces = list(set(necessary_network_interfaces) & set(existing_network_interfaces))
        logging.debug("common_network_interfaces: " + str(common_network_interfaces))
        assert len(common_network_interfaces) >= len(necessary_network_interfaces)
