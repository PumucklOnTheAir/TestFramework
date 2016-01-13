from config.configmanager import ConfigManager
import unittest


class MyTestCase(unittest.TestCase):

    # router tests auto
    def test_get_config_router_auto(self):
        """
        Tests the router auto config
        :return: Tests results
        """
        data = ConfigManager.get_router_auto_config()
        self.assertEqual(len(data), 8, "test_Yaml: Wrong size of the List")

    def test_config_router_auto_with_length(self):
        """
        Tests the router auto config with length
        :return: Tests results
        """
        data = ConfigManager.get_router_auto_list(4)
        self.assertEqual(len(data), 4, "test_Yaml: Wrong size of the List")

    def test_config_router_auto(self):
        """
        Tests the router auto config
        :return: Tests results
        """
        data = ConfigManager.get_router_auto_list()
        self.assertEqual(len(data), 1, "test_Yaml: Wrong size of the List")

    # router tests manual
    def test_get_config_router_manual(self):
        """
        Tests the router manual config
        :return: Tests results
        """
        data = ConfigManager.get_router_manual_config()
        self.assertEqual(len(data), 3, "test_Yaml: Wrong size of the List")

    def test_config_router_manual(self):
        """
        Tests the router manual config
        :return: Tests results
        """
        data = ConfigManager.get_router_manual_list()
        self.assertEqual(len(data), 3, "test_Yaml: Wrong size of the List")

    # server tests
    def test_config_server(self):
        """
        Tests the server config
        :return: Tests results
        """
        data = ConfigManager.get_server_config()
        self.assertEqual(len(data), 1, "test_Yaml: Wrong size of the List")

    def test_config_server_dict(self):
        """
        Tests the server config
        :return: Tests results
        """
        data = ConfigManager.get_server_dict()
        self.assertEqual(len(data), 1, "test_Yaml: Wrong size of the List")

    def test_config_server_list(self):
        """
        Tests the server config
        :return: Tests results
        """
        data = ConfigManager.get_server_list()
        self.assertEqual(len(data), 3, "test_Yaml: Wrong size of the List")

    def test_config_server_prop(self):
        """
        Tests the server config with a property
        :return: Tests results
        """
        data = ConfigManager.get_server_property("Server_Name")
        self.assertEqual(data, "TestServer", "test_Yaml: Wrong size of the List")

    # test tests
    def test_config_test(self):
        """
        Tests the test config
        :return: Tests results
        """
        data = ConfigManager.get_test_config()
        self.assertEqual(len(data), 2, "test_Yaml: Wrong size of the List")

    def test_config_test_dict(self):
        """
        Tests the test config
        :return: Tests results
        """
        data = ConfigManager.get_test_dict()
        self.assertEqual(len(data), 2, "test_Yaml: Wrong size of the List")

    def test_config_test_list(self):
        """
        Tests the test config
        :return: Tests results
        """
        data = ConfigManager.get_test_list()
        self.assertEqual(len(data), 4, "test_Yaml: Wrong size of the List")

    # firmware tests
    def test_firmware_property(self):
        """
        Tests the firmware config with property
        :return: Tests results
        """
        data = ConfigManager.get_firmware_property("Firmware_Version")
        self.assertEqual(data, "0.7.3", "firmware_Yaml: Wrong prop from the file")

    def test_firmware_config(self):
        """
        Tests the firmware config
        :return: Tests results
        """
        data = ConfigManager.get_firmware_config()
        self.assertEqual(len(data), 1, "firmware_Yaml: Wrong size of the List")

    def test_firmware_dict(self):
        """
        Tests the firmware config
        :return: Tests results
        """
        data = ConfigManager.get_firmware_dict()
        self.assertEqual(len(data), 1, "firmware_Yaml: Wrong size of the List")

    def test_firmware_list(self):
        """
        Tests the firmware config
        :return: Tests results
        """
        data = ConfigManager.get_firmware_list()
        self.assertEqual(len(data), 4, "firmware_Yaml: Wrong size of the List")

    def test_power_strip_config(self):
        """
        Tests the power strip config
        :return: Tests results
        """
        data = ConfigManager.get_power_strip_config()
        self.assertEqual(len(data), 8, "power_strip_Yaml: Wrong size of the List")

    def test_power_strip_dict(self):
        """
        Tests the power strip config
        :return: Tests results
        """
        data = ConfigManager.get_power_strip_list()
        self.assertEqual(len(data), 1, "power_strip_Yaml: Wrong size of the List")

    if __name__ == '__main__':
        unittest.main()
