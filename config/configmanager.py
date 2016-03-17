import yaml
import io
import logging
from os import path
from router.router import Router


class ConfigManager:
    """
    Manager which handles the config files for the TestServer.
    """

    BASE_DIR = path.dirname(path.dirname(__file__))  # This is your Project Root
    CONFIG_PATH = path.join(BASE_DIR, 'config')  # Join Project Root with config
    FRAMEWORK_CONFIG_FILE = 'framework_config.yml'

    @classmethod
    def set_config_path(cls, config_path: str = "") -> None:
        """
        Set the path from the files

        :param config_path: where the files are
        :return: None
        """
        cls.CONFIG_PATH = config_path

    @staticmethod
    def read_file(file_path: str = "") -> []:
        """
        Read a config file from the path

        :param file_path: File path
        :return: Array with the output from the file
        """
        try:
            if file_path == "":
                logging.error("Path is an empty string")
                return None
            file_stream = io.open(file_path, "r", encoding="utf-8")
            output = yaml.safe_load(file_stream)
            file_stream.close()
            return output
        except IOError as ex:
            logging.error("Error at read the file at path: {0}\nError: {1}".format(file_path, ex))
            return None
        except yaml.YAMLError as ex:
            logging.error("Error at safe load the YML-File\nError: {0}".format(ex))
            return None

    # config
    @staticmethod
    def get_framework_config() -> []:
        """
        Read the framework config file

        :return: Dictionary with the output from the file
        """
        file_path = path.join(ConfigManager.CONFIG_PATH, ConfigManager.FRAMEWORK_CONFIG_FILE)
        return ConfigManager.read_file(file_path)

    # router
    @staticmethod
    def get_routers_dict() -> dict:
        """
        Read the routers from config file

        :return: Dictionary with all routers
        """
        config = ConfigManager.get_framework_config()
        return config['routers']

    @staticmethod
    def get_routers_list() -> []:
        """
        Read the routers from the config

        :return: List with any router objects from the file
        """
        output = ConfigManager.get_routers_dict()

        routers = []

        # i must defined before 'for', because 'default' increase i and then the router.id has wrong count
        i = 0
        for data in output.items():

            name, router_info = data

            if 'default' in name:
                continue

            if len(router_info) != 9:  # FixMe ist eher eine schlechte idee
                logging.error("List must be length of 9 but has a length of {0}".format(len(output)))
                return None

            # TODO:
            # wenn die keys im "router_info" dict mit den argument namen von `Router` passt kann man das so machen:
            # router = Router(i, **router_info)

            try:
                router = Router(i, router_info['Name'], router_info['Id'], router_info['IP'], router_info['IP_Mask'],
                                router_info['CONFIG_IP'], router_info['CONFIG_IP_MASK'],
                                router_info['Username'], router_info['Password'], router_info['PowerSocket'])
                routers.append(router)
                i += 1

            except KeyError as ex:
                logging.error("Error at building the list of Router's\nError: {0}".format(ex))
                return None

        if len(routers) > 0:
            routers = sorted(routers, key=lambda e: e.id)

        return routers

    # server
    @staticmethod
    def get_server_dict() -> dict:
        """
        Read the server config from the file

        :return: Dictionary with all server properties from the file
        """
        config = ConfigManager.get_framework_config()
        return config['server']

    @staticmethod
    def get_server_list() -> []:
        """
        Read the server config from the file

        :return: List with all server properties from the file
        """
        server = ConfigManager.get_server_dict()
        server_list = []
        for x in server:
            props = server[x]
            for entry in props:
                server_list.append(props[entry])
        return server_list

    @staticmethod
    def get_server_property(prop: str = "") -> object:
        """
        Read the server config from the file and give the property back

        :param prop: Property from server
        :return: Value of the property from server
        """
        server = ConfigManager.get_server_dict()
        for value in server.values():
            if prop in value:
                return value[prop]

        return None

    # firmware
    @staticmethod
    def get_firmware_dict() -> dict:
        """
        Read the firmware config from the file

        :return: Dictionary with all firmware properties from the file
        """
        config = ConfigManager.get_framework_config()
        return config['firmware']

    @staticmethod
    def get_firmware_list() -> []:
        """
        Read the firmware config from the file

        :return: List with all firmware properties from the file
        """
        firmware = ConfigManager.get_firmware_dict()
        firmware_list = []
        for x in firmware:
            props = firmware[x]
            for entry in props:
                firmware_list.append(props[entry])
        return firmware_list

    @staticmethod
    def get_firmware_property(prop: str = "") -> object:
        """
        Read the firmware config from the file and give the property back

        :param prop: Property from firmware
        :return: Value of the property from firmware
        """
        firmware = ConfigManager.get_firmware_dict()
        for value in firmware.values():
            if prop in value:
                return value[prop]

        return None

    # web interface
    @staticmethod
    def get_web_interface_dict() -> dict:
        """
        Read the web interface config from the file
        :return: Dictionary with all web interface properties from the file
        """
        config = ConfigManager.get_framework_config()
        return config['webconfigs']

    @staticmethod
    def get_web_interface_list() -> []:
        """
        Read the web interface config from the file
        :return: List with all web interface properties from the file, have intern dictionaries
        """
        interface = ConfigManager.get_web_interface_dict()

        web_list = []
        for x in interface:

            if 'default' in x:
                continue

            props = interface[x]
            web_list.append(props)

        if web_list:
            if 'node_name' in web_list[0].keys():
                web_list = sorted(web_list, key=lambda e: e['node_name'])

        return web_list

    @staticmethod
    def get_web_interface_property(prop: str = "") -> object:
        """
        Read the web interface config from the file and give the property back

        :param prop: Property from web interface
        :return: Value of the property from web interface
        """
        interface = ConfigManager.get_web_interface_dict()
        for value in interface.values():
            if prop in value:
                return value[prop]

        return None

    # power strip
    @staticmethod
    def get_power_strip_dict() -> dict:
        """
        Read the power strip config from the file
        :return: Dictionary with all power strip properties from the file
        """
        config = ConfigManager.get_framework_config()
        return config['powerstrip']

    @staticmethod
    def get_power_strip_list() -> []:
        """
        Read the power strip config file
        :return: List with any power strips objects from the file
        """
        power_strip = ConfigManager.get_power_strip_dict()
        power_strip = power_strip['powerstripdefault']

        if len(power_strip) != 8:  # FixME: nicht so die gute idee
            logging.error("List must be length of 8 but has a length of {0}".format(len(power_strip)))
            return None

        try:
            count = power_strip['Power_Strip_Count']

            power_strip_list = []

            # TODO:
            # wenn die keys im "power_strip" dict mit den argument namen von `Ubnt` passt kann man das so machen:
            # u = Ubnt(i, **power_strip)

            for i in range(0, count):
                """
                u = Ubnt(i, power_strip['default_Name'], power_strip['default_vlan_Id'], power_strip['default_IP'],
                         power_strip['default_Mask'], power_strip['default_Username'], power_strip['default_Password'],
                         power_strip['default_Ports'])
                """
                u = None
                power_strip_list.append(u)

            # if power_strip_list:
            #    power_strip_list = sorted(power_strip_list, key=lambda e: e.id)

            return power_strip_list

        except KeyError as ex:
            logging.error("Error at building the list of Router's\nError: {0}".format(ex))
            return None

    @staticmethod
    def get_test_dict() -> []:
        """
        Read the test config from the file

        :return: Dictionary with all test properties from the file
        """
        config = ConfigManager.get_framework_config()
        return config['tests']

    @staticmethod
    def get_test_sets() -> []:
        """
        Read the test config from the file

        :return: List with all test properties from the file
        """
        tests = ConfigManager.get_test_dict()
        return tests
