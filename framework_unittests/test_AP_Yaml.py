from config.configmanager import ConfigManager
import unittest
from os import path


class MyTestCase(unittest.TestCase):

    # framework config
    def test_get_config_framework(self):
        """
        Tests the framework config
        :return: Tests results
        """
        data = ConfigManager.get_framework_config()
        self.assertEqual(True, (data is not None), "Wrong data")

    # schema
    def test_get_schema_framework(self):
        """
        Tests the framework schema
        :return: Tests results
        """
        schema = ConfigManager.get_framework_schema()
        self.assertEqual(True, (schema is not None), "Wrong schema")

    # check config against schema
    def test_check(self):
        """
        Test config vs. schema
        :return: Test results
        """
        data = ConfigManager.get_framework_config()
        result = ConfigManager.check(data)
        self.assertEqual(True, result, "Wrong schema or data")

    # config path test
    def test_set_config_path(self):
        """
        Tests to set the config path
        :return: Tests results
        """
        base_dir = path.dirname(path.dirname(__file__))  # This is your Project Root

        config_path = path.join(base_dir, 'framework_unittests/configs/config_no_vlan')
        ConfigManager.set_config_path(config_path)
        self.assertEqual(ConfigManager.CONFIG_PATH, config_path, "Wrong path")

        config_path = path.join(base_dir, 'config')  # Join Project Root with config
        ConfigManager.set_config_path(config_path)
        self.assertEqual(ConfigManager.CONFIG_PATH, config_path, "Wrong path")

    # test read
    def test_read_file(self):
        """
        Read a file
        :return: Tests results
        """
        output = ConfigManager.read_file("")
        self.assertEqual(output, None, "Wrong output")

        output = ConfigManager.read_file(ConfigManager.CONFIG_PATH)
        self.assertEqual(output, None, "Wrong output")

        file_path = path.join(ConfigManager.CONFIG_PATH, ConfigManager.FRAMEWORK_CONFIG_FILE)
        output = ConfigManager.read_file(file_path)

        self.assertEqual((output is not None), True, "Wrong output")

    # router tests
    def test_get_routers_dict(self):
        """
        Tests the router config
        :return: Tests results
        """
        data = ConfigManager.get_routers_dict()
        self.assertEqual(True, data[0], "Routers: Wrong config")

    def test_get_routers_list(self):
        """
        Tests the router config
        :return: Tests results
        """
        data = ConfigManager.get_routers_list()
        self.assertEqual(True, len(data) > 0, "Routers: Wrong size of the List")

    # server tests
    def test_server_dict(self):
        """
        Tests the server config
        :return: Tests results
        """
        data = ConfigManager.get_server_dict()
        self.assertEqual(True, data[0], "Server: Wrong config")

    def test_server_list(self):
        """
        Tests the server config
        :return: Tests results
        """
        data = ConfigManager.get_server_list()
        self.assertEqual(True, len(data) > 0, "Server: Wrong size of the List")

    def test_server_prop(self):
        """
        Tests the server config with a property
        :return: Tests results
        """
        data = ConfigManager.get_server_property("Server_Name")
        self.assertEqual(True, type(data) == str, "Server: Wrong property")

    # firmware tests
    def test_firmware_dict(self):
        """
        Tests the firmware config
        :return: Tests results
        """
        data = ConfigManager.get_firmware_dict()
        self.assertEqual(True, data[0], "Firmware: Wrong config")

    def test_firmware_list(self):
        """
        Tests the firmware config
        :return: Tests results
        """
        data = ConfigManager.get_firmware_list()
        self.assertEqual(True, len(data) > 0, "Firmware: Wrong size of the List")

    def test_firmware_property(self):
        """
        Tests the firmware config with property
        :return: Tests results
        """
        data = ConfigManager.get_firmware_property("Firmware_Version")
        self.assertEqual(True, type(data) == str, "Firmware: Wrong property")

    # web interface
    def test_web_interface_dict(self):
        """
        Tests the web interface config
        :return: Tests results
        """
        data = ConfigManager.get_web_interface_dict()
        self.assertEqual(True, data[0], "web_interface: Wrong config")

    def test_web_interface_list(self):
        """
        Tests the web interface config
        :return: Tests results
        """
        data = ConfigManager.get_web_interface_list()
        self.assertEqual(True, len(data) > 0, "web_interface: Wrong size of the List")

    def test_web_interface_property(self):
        """
        Tests the web interface config with property
        :return: Tests results
        """
        data = ConfigManager.get_web_interface_property("auto_update")
        self.assertEqual(data, False, "web_interface: Wrong property")

    # power strip
    def test_power_strip_dict(self):
        """
        Tests the power strip config
        :return: Tests results
        """
        data = ConfigManager.get_power_strip_dict()
        self.assertEqual(True, data[0], "power_strip: Wrong config")

    def test_power_strip_list(self):
        """
        Tests the power strip config
        :return: Tests results
        """
        data = ConfigManager.get_power_strip_list()
        self.assertEqual(True, len(data) > 0, "power_strip: Wrong size of the List")

        # tests
    def test_test_dict(self):
        """
        Tests the test config
        :return: Tests results
        """
        data = ConfigManager.get_test_dict()
        self.assertEqual(True, data[0], "test: Wrong config")

    def test_test_set(self):
        """
        Tests the test config
        :return: Tests results
        """
        data = ConfigManager.get_test_sets()
        self.assertEqual(True, len(data) > 0, "test: Wrong size of the List")

    if __name__ == '__main__':
        unittest.main()
