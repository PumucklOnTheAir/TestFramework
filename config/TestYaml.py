from config.ConfigManager import *
import unittest


class TestingYaml(unittest.TestCase):

    def test_load(self):
        print(ConfigManager.read_file("C:\\Temp\\test.yaml"))
        self.assertTrue(1, 1)

    def test_dump(self):
        ConfigManager.write_file("test", "C:\\Temp\\out.yaml")
        self.assertTrue(1, 1)

    def test_config(self):
        data = ConfigManager.get_v_lan(4)
        self.assertTrue(1, 1)

    if __name__ == '__main__':
        unittest.main()
