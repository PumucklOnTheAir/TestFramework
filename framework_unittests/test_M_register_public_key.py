from unittest import TestCase
from router.router import Router
from util.register_public_key import RegisterPublicKey
from config.configmanager import ConfigManager


class TestRegisterPublicKey(TestCase):
    """
    This TestModule tests the functionality of Registration of the PublicKey.
    """""

    def test_registration(self):
        config = ConfigManager.get_server_dict()[1]["serverdefaults"]

        print("Test Registration Public-Key")
        router = self._create_router()
        assert config["smtp_server"] == "smtp.web.de"
        assert config["smtp_port"] == 587
        assert config["email"] == "symenschmitt_trash@web.de"
        assert config["email_password"] == "passworter"
        assert config["key_email"] == "symenschmitt@aol.com"
        reg_pub_key = RegisterPublicKey(router, config)
        reg_pub_key.start()
        reg_pub_key.join()

    def _create_router(self):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        router.node_name = "64293-testframework1"
        router.public_key = "483938492329bc12aa1212d1b"
        assert isinstance(router, Router)
        return router
