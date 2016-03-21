from unittest import TestCase
from router.router import Router
from util.register_public_key import RegisterPublicKey


class TestRegisterPublicKey(TestCase):
    """
    This TestModule tests the functionality of Registration of the PublicKey.
    """""

    def test_registration(self):
        # TODO: Werte ändern
        print("Test Registration Public-Key")
        router = self._create_router()
        config = {"smtp_server": "smtp.web.de",
                  "smtp_port": 587,
                  "email": "symenschmitt_trash@web.de",
                  "email_password": "passworter",
                  "key_email": "symenschmitt@aol.com"}
        reg_pub_key = RegisterPublicKey(router, config)
        reg_pub_key.start()
        reg_pub_key.join()

    def _create_router(self):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        router._public_name = "64293-testframework"
        router.public_key = "483938492329bc12aa1212d1b"
        assert isinstance(router, Router)
        return router
