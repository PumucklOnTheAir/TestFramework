from config.configmanager import *
import unittest


class MyTestCase(unittest.TestCase):

    # def test_load(self):
    #     print(ConfigManager.read_file("C:\\Temp\\test.yaml"))
    #     self.assertTrue(1, 1)
    #
    # def test_dump(self):
    #     ConfigManager.write_file("test", "C:\\Temp\\out.yaml")
    #     self.assertTrue(1, 1)

    def test_config_router(self):
        data = ConfigManager.get_router_auto_list(4)
        self.assertEqual(len(data), 4, "test_Yaml: Wrong size of the List")

    def test_config_router2(self):
        data = ConfigManager.get_router_auto_list()
        self.assertEqual(len(data), 1, "test_Yaml: Wrong size of the List")

    def test_config_router_manual(self):
        data = ConfigManager.get_router_manual_list()
        self.assertEqual(len(data), 3, "test_Yaml: Wrong size of the List")

    def test_config_server(self):
        data = ConfigManager.get_server_property_list()
        self.assertEqual(len(data), 1, "test_Yaml: Wrong size of the List")

    def test_config_test(self):
        data = ConfigManager.get_test_list()
        self.assertEqual(len(data), 2, "test_Yaml: Wrong size of the List")

    def test_firmware_property(self):
        data = ConfigManager.get_firmware_property("Firmware_Version")
        self.assertEqual(data, "0.7.3", "firmware_Yaml: Wrong prop from the file")

    def test_firmware_list(self):
        data = ConfigManager.get_firmware_list()
        self.assertEqual(len(data), 4, "firmware_Yaml: Wrong size of the List")

    if __name__ == '__main__':
        unittest.main()
