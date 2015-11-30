import yaml
import io
import logging
import os.path
from server.router import *


class ConfigManager:

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
    CONFIG_PATH = os.path.join(BASE_DIR, 'config')  # Join Project Root with config
    VLAN_CONFIG_PATH = os.path.join(CONFIG_PATH, 'vlan_config.yaml')
    SERVER_CONFIG_PATH = os.path.join(CONFIG_PATH, 'server_config.yaml')
    TEST_CONFIG_PATH = os.path.join(CONFIG_PATH, 'test_config.yaml')

    @staticmethod
    def read_file(path) -> []:
        try:
            file_stream = io.open(path, "r", encoding="utf-8")
            output = yaml.safe_load(file_stream)
            file_stream.close()
            return output
        except IOError as ex:
            logging.error("Error at read the file at path: {0}\nError: {1}".format(path, ex))
        except yaml.YAMLError as ex:
            logging.error("Error at safe load the Yaml-File\nError: {0}".format(ex))

    @staticmethod
    def write_file(data, path) -> None:
        try:
            file_stream = io.open(path, "w", encoding="utf-8")
            yaml.safe_dump(data, file_stream)
            file_stream.flush()
            file_stream.close()
        except IOError as ex:
            logging.error("Error at read the file at path: {0}\nError: {1}".format(path, ex))
        except yaml.YAMLError as ex:
            logging.error("Error at safe dump the Yaml-File\nError: {0}".format(ex))

    @staticmethod
    def get_vlan_config() -> []:
        return ConfigManager.read_file(ConfigManager.VLAN_CONFIG_PATH)

    @staticmethod
    def get_vlan_list(vlan_count=0) -> []:
        output = ConfigManager.get_vlan_config()

        if not len(output) == 7:
            logging.error("List must be length of 7 but has a length of {0}".format(len(output)))
            return

        router_count = output[0]
        v_name = output[1]
        v_id = output[2]
        v_ip = output[3]
        v_mask = output[4]
        username = output[5]
        password = output[6]

        try:
            i = v_id['default_Start_Id']
            vlan_list = []

            if vlan_count <= 0:
                count = router_count['Router_Count']
            else:
                count = vlan_count

            for x in range(0, count):
                v = Router(v_name['default_Name'] + "{0}".format(i), i, v_ip['default_IP'], v_mask['default_Mask'],
                           username['default_Username'], password['default_Password'])
                vlan_list.append(v)
                i += 1

            return vlan_list
        except Exception as ex:
            logging.error("Error at building the list of VLan's\nError: {0}".format(ex))

    @staticmethod
    def get_server_config() -> []:
        return ConfigManager.read_file(ConfigManager.SERVER_CONFIG_PATH)

    @staticmethod
    def get_server_property_list() -> []:
        output = ConfigManager.get_server_config()
        return output

    @staticmethod
    def get_test_config() -> []:
        return ConfigManager.read_file(ConfigManager.TEST_CONFIG_PATH)

    @staticmethod
    def get_test_list() -> []:
        output = ConfigManager.get_test_config()
        return output
