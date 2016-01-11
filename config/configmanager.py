import yaml
import io
from log.logger import Logger
import os.path
from server.router import *


class ConfigManager:
    """
    Manager who handles the config files
    """

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
    CONFIG_PATH = os.path.join(BASE_DIR, 'config')  # Join Project Root with config
    ROUTER_AUTO_CONFIG_PATH = os.path.join(CONFIG_PATH, 'router_auto_config.yaml')
    ROUTER_MANUAL_CONFIG_PATH = os.path.join(CONFIG_PATH, 'router_manual_config.yaml')
    SERVER_CONFIG_PATH = os.path.join(CONFIG_PATH, 'server_config.yaml')
    TEST_CONFIG_PATH = os.path.join(CONFIG_PATH, 'test_config.yaml')
    FIRMWARE_CONFIG_PATH = os.path.join(CONFIG_PATH, 'firmware_config.yaml')

    @staticmethod
    def read_file(path: str = "") -> []:
        """
        Read a config file from the path
        :param path: File path
        :return: Array with the output from the file
        """
        try:
            if path == "":
                Logger().error("Path is an empty string")
                return
            file_stream = io.open(path, "r", encoding="utf-8")
            output = yaml.safe_load(file_stream)
            file_stream.close()
            return output
        except IOError as ex:
            Logger().error("Error at read the file at path: {0}\nError: {1}".format(path, ex))
        except yaml.YAMLError as ex:
            Logger().error("Error at safe load the YAML-File\nError: {0}".format(ex))

    @staticmethod
    def write_file(data: str = "", path: str = "") -> None:
        """
        Write a config file on the path
        :param data: String of data to write in the file
        :param path: File path
        :return: None
        """
        try:
            if path == "":
                Logger().error("Path is an empty string")
                return
            file_stream = io.open(path, "w", encoding="utf-8")
            yaml.safe_dump(data, file_stream)
            file_stream.flush()
            file_stream.close()
        except IOError as ex:
            Logger().error("Error at read the file at path: {0}\nError: {1}".format(path, ex))
        except yaml.YAMLError as ex:
            Logger().error("Error at safe dump the YAML-File\nError: {0}".format(ex))

    @staticmethod
    def get_router_auto_config() -> []:
        """
        Read the Router Auto Config file
        :return: Array with the output from the file
        """
        return ConfigManager.read_file(ConfigManager.ROUTER_AUTO_CONFIG_PATH)

    @staticmethod
    def get_router_auto_list(count: int = 0) -> []:
        """
        Read the Router Manual Config file
        :param count: Count of the Router
        :return: List with a specific output from the file
        """
        output = ConfigManager.get_router_auto_config()

        if not len(output) == 10:
            Logger().error("List must be length of 10 but has a length of {0}".format(len(output)))
            return

        try:
            router_count = output[0]
            name = output[1]
            identifier = output[2]
            ip = output[3]
            ip_mask = output[4]
            config_ip = output[5]
            config_ip_mask = output[6]
            username = output[7]
            password = output[8]
            power_socket = output[9]

            i = identifier['default_Start_Id']
            socket_id = power_socket['powerSocket_Start_Id']
            router_list = []

            if count <= 0:
                count = router_count['router_Count']
            else:
                count = count

            for x in range(0, count):
                v = Router(x, name['default_Name'] + "{0}".format(i), i, ip['default_IP'], ip_mask['default_IP_Mask'],
                           config_ip['default_CONFIG_IP'], config_ip_mask['default_CONFIG_IP_MASK'],
                           username['default_Username'], password['default_Password'], socket_id)
                router_list.append(v)
                i += 1
                socket_id += 1

            return router_list

        except Exception as ex:
            Logger().error("Error at building the list of Router's\nError: {0}".format(ex))

    @staticmethod
    def get_router_manual_config() -> []:
        """
        Read the Router Manual Config file
        :return: Array with the output from the file
        """
        return ConfigManager.read_file(ConfigManager.ROUTER_MANUAL_CONFIG_PATH)

    @staticmethod
    def get_router_manual_list() -> []:
        """
        Read the Router Manual Config file
        :return: List with a specific output from the file
        """
        output = ConfigManager.get_router_manual_config()

        router_list = []

        for i in range(0, len(output)):
            router_info = output[i]

            if not len(router_info) == 9:
                Logger().error("List must be length of 9 but has a length of {0}".format(len(output)))
                return

            try:
                v = Router(i, router_info['Name'], router_info['Id'], router_info['IP'], router_info['IP_Mask'],
                           router_info['CONFIG_IP'], router_info['CONFIG_IP_MASK'],
                           router_info['Username'], router_info['Password'], router_info['PowerSocket'])
                router_list.append(v)

            except Exception as ex:
                Logger().error("Error at building the list of Router's\nError: {0}".format(ex))

        return router_list

    @staticmethod
    def get_server_config() -> []:
        """
        Read the Server Config file
        :return: Array with the output from the file
        """
        return ConfigManager.read_file(ConfigManager.SERVER_CONFIG_PATH)

    @staticmethod
    def get_server_property_list() -> []:
        """
        Read the Server Config file
        :return: List with a specific output from the file
        """
        output = ConfigManager.get_server_config()
        return output

    @staticmethod
    def get_test_config() -> []:
        """
        Read the Test Config file
        :return: Array with the output from the file
        """
        return ConfigManager.read_file(ConfigManager.TEST_CONFIG_PATH)

    @staticmethod
    def get_test_list() -> []:
        """
        Read the Test Config file
        :return: List with a specific output from the file
        """
        output = ConfigManager.get_test_config()
        return output

    @staticmethod
    def get_firmware_config() -> []:
        """
        Read the Firmware Config file
        :return: Array with the output from the file
        """
        return ConfigManager.read_file(ConfigManager.FIRMWARE_CONFIG_PATH)

    @staticmethod
    def get_firmware_list() -> []:
        """
        Read the Firmware Config file
        :return: List with a specific output from the file
        """
        output = ConfigManager.get_firmware_config()
        firmware_list = []
        for x in output:
            for v in x.values():
                firmware_list.append(v)
        return firmware_list

    @staticmethod
    def get_firmware_property(prop: str = "") -> object:
        """
        Read the Firmware Config file and give the property back
        :param prop: Property from Firmware file
        :return: Value of the property from the file
        """
        dic_keys = {"URL", "Release_Model", "Firmware_Version"}

        if prop in dic_keys:
            output = ConfigManager.get_firmware_config()
            for x in output:
                if prop in x.keys():
                    return x[prop]

        return None
