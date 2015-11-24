import yaml
import io
import logging
import os.path
from config.VLan import *


class ConfigManager:

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
    CONFIG_PATH = os.path.join(BASE_DIR, 'config')  # Join Project Root with config
    V_LAN_CONFIG_PATH = os.path.join(CONFIG_PATH, 'v_lan_config.yaml')

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
    def get_v_lan_config() -> []:
        return ConfigManager.read_file(ConfigManager.V_LAN_CONFIG_PATH)

    @staticmethod
    def get_v_lan(count) -> []:
        output = ConfigManager.get_v_lan_config()

        if not len(output) == 4:
            logging.error("List must be length of 4 but has a length of {0}".format(len(output)))
            return

        v_name = output[0]
        v_id = output[1]
        v_ip = output[2]
        v_mask = output[3]

        try:
            i = v_id['default_start_Id']
            v_lan_list = []
            for x in range(0, count):
                v = VLan(v_name['default_Name'] + "{0}".format(i),
                         i,
                         v_ip['default_IP'],
                         v_mask['default_Mask'])
                v_lan_list.append(v)
                i += 1
            return v_lan_list
        except Exception as ex:
            logging.error("Error at building the list of VLan's\nError: {0}".format(ex))
