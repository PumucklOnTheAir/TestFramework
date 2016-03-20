from server.test import FirmwareTest
from router.router import Mode


class TestAvailableNetworkInterfaces(FirmwareTest):
    """
    Test the availability of specific network-interfaces in the configuration-mode.
    ()
    """""

    def test_availability(self):
        assert self.remote_system.mode == Mode.configuration
