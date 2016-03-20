from server.test import FirmwareTest
from router.router import Mode


class TestMeshing(FirmwareTest):
    """
    Test if the Router sees other mesh-nodes.
    """""

    def test_meshing(self):
        assert self.remote_system.mode == Mode.normal
        bat_originators = self.remote_system.bat_originators()
        assert len(bat_originators) > 0
