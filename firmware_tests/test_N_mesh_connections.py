from server.test import FirmwareTest
from router.router import Mode
import logging
from log.loggersetup import LoggerSetup


class TestMeshConnections(FirmwareTest):
    """
    Tests if the Router sees other mesh-nodes.
    """""

    def test_meshing(self):
        """
        Test:
            1. Router is in normal-mode
            2. Mesh-connections exist
        """
        logging.debug("%sTest: Existence of Mesh-Connections", LoggerSetup.get_log_deep(1))
        assert self.remote_system.mode == Mode.normal
        logging.debug("%s[" + u"\u2713" + "] Correct Mode", LoggerSetup.get_log_deep(2))
        bat_originators = self.remote_system.bat_originators
        assert len(bat_originators) > 0
        logging.debug("%s[" + u"\u2713" + "] Connected Mesh-Nodes exist", LoggerSetup.get_log_deep(2))
