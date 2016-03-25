from server.test import FirmwareTest
from router.router import Mode
from log.loggersetup import LoggerSetup
import logging


class TestCorrectMeshConnections(FirmwareTest):
    """
    This Firmware-Test tests if the known Routers are connected inside the mesh.
    """""

    def test_meshing(self):
        """
        Test:
            1. Router is in normal-mode
            2. Mesh-connections exist
            3. All known Routers that are in normal-mode are connected with the tested Router
        """
        logging.debug("%sTest: Correctness of the Mesh-Connections", LoggerSetup.get_log_deep(1))
        assert self.remote_system.mode == Mode.normal
        logging.debug("%s[" + u"\u2714" + "] Correct Mode", LoggerSetup.get_log_deep(2))
        bat_originators = self.remote_system.bat_originators
        self.assertTrue(len(bat_originators) > 0, "No connected Mesh-Nodes exist")
        logging.debug("%s[" + u"\u2714" + "] Connected Mesh-Nodes exist", LoggerSetup.get_log_deep(2))

        my_bat__originators = self.remote_system.bat_originators
        my_bat__originators_macs = [originator.mac for originator in my_bat__originators]

        for router in self.all_routers:
            if router.id == self.remote_system.id or router.mode == Mode.configuration:
                continue
            known_router_mac = router.network_interfaces["mesh0"].mac
            cnt = my_bat__originators_macs.count(known_router_mac)
            self.assertTrue(cnt >= 1, "Not connected with  known Router(" + str(router.id) + ")")
            logging.debug("%s[" + u"\u2713" + "] Connected with known Router(" + str(router.id) + ")",
                          LoggerSetup.get_log_deep(2))
