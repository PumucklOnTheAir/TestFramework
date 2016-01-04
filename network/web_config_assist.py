from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from pyvirtualdisplay import Display
from log.logger import Logger
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains, keys
import time


class WebConfigurationAssist:
    """
    To use this class the following has to be installed: 'sudo apt-get install iceweasel xvfb'
    """

    def __init__(self):
        Logger().debug("Create WebConfigurationAssist ...", 2)
        # todO: On raspberry pi necessary: create virtual display
        #self.display = Display(visible=0, size=(800, 600))
        #self.display.start()

        self.browser = webdriver.Firefox()

    def setup_wizard(self, config):
        """
        Sets the values provided by the wizard (in the WebConfiguration)
        :param config: {node_name, mesh_vpn, limit_bandwidth, show_location, latitude, longitude, altitude,contact}
        """
        Logger().debug("Setup 'wizard' with: " + str(config), 3)
        self.browser.get(config['url'])

        node_name_field_id = "cbid.wizard.1._hostname"
        mesh_vpn_field_id = "cbid.wizard.1._meshvpn"
        limit_bandwidth_field_id = "cbid.wizard.1._limit_enabled"
        show_location_field_id = "cbid.wizard.1._location"
        latitude_field_id = "cbid.wizard.1._latitude"
        longitude_field_id = "cbid.wizard.1._longitude"
        altitude_field_id = "cbid.wizard.1._altitude"
        contact_field_id = "cbid.wizard.1._contact"
        safe_restart_button_xpath = "//*[@class='cbi-button cbi-button-save']"

        node_name_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(node_name_field_id))
        mesh_vpn_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(mesh_vpn_field_id))
        limit_bandwidth_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(limit_bandwidth_field_id))
        show_location_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(show_location_field_id))
        latitude_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(latitude_field_id))
        longitude_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(longitude_field_id))
        altitude_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(altitude_field_id))
        contact_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(contact_field_id))
        safe_restart_button_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_xpath(safe_restart_button_xpath))

        # The checkboxes are set to 'display = none' via css.
        # Because selenium can't see them we have to set the checkboxes to 'display = inline'
        self.browser.execute_script("arguments[0].style.display = 'inline';",mesh_vpn_field_element)
        self.browser.execute_script("arguments[0].style.display = 'inline';",limit_bandwidth_field_element)
        self.browser.execute_script("arguments[0].style.display = 'inline';",show_location_field_element)

        node_name_field_element.clear()
        node_name_field_element.send_keys(config['node_name'])

        if config['mesh_vpn']:
            if not mesh_vpn_field_element.is_selected():
                mesh_vpn_field_element.click()
            if config['limit_bandwidth']:
                if not limit_bandwidth_field_element.is_selected():
                    limit_bandwidth_field_element.click()
            else:
                if limit_bandwidth_field_element.is_selected():
                    limit_bandwidth_field_element.click()
        else:
            if mesh_vpn_field_element.is_selected():
                mesh_vpn_field_element.click()

        if config['show_location']:
            if not show_location_field_element.is_selected():
                show_location_field_element.click()
            latitude_field_element.clear()
            latitude_field_element.send_keys(config['latitude'])
            longitude_field_element.clear()
            longitude_field_element.send_keys(config['longitude'])
            altitude_field_element.clear()
            altitude_field_element.send_keys(config['altitude'])
        else:
            if show_location_field_element.is_selected():
                show_location_field_element.click()

        contact_field_element.send_keys(config['contact'])

        safe_restart_button_element.click()

    def setup_expert_private_wlan(self, config):
        """
        Extend your private network by bridging the WAN interface with a seperate WLAN
        :param config: {url, private_wlan, reset}
        """
        Logger().debug("Setup 'Private WLAN' with: " + str(config), 3)
        self.browser.get(config['url'])

        private_wlan_field_id = "cbid.wifi.1.enabled"
        safe_button_xpath = "//*[@class='cbi-button cbi-button-save']"
        reset_button_xpath = "//*[@class='cbi-button cbi-button-reset']"

        private_wlan_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(private_wlan_field_id))
        safe_button_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_xpath(safe_button_xpath))
        reset_button_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_xpath(reset_button_xpath))

        # The checkboxes are set to 'display = none' via css.
        # Because selenium can't see them we have to set the checkboxes to 'display = inline'
        self.browser.execute_script("arguments[0].style.display = 'inline';",private_wlan_field_element)

        if config['private_wlan']:
            if not private_wlan_field_element.is_selected():
                private_wlan_field_element.click()
        else:
            if private_wlan_field_element.is_selected():
                private_wlan_field_element.click()

        if config['reset']:
            reset_button_element.click()

        safe_button_element.click()

    def setup_expert_remote_access(self, config):
        Logger().debug("Setup 'Private WLAN' with: " + str(config), 3)
        self.browser.get(config['url'])

        ssh_keys_field_id = "cbid.system._keys._data"
        ssh_password_field_id = "cbid.system._pass.pw1"
        ssh_password_confirm_field_id = "cbid.system._pass.pw1"
        # TODO beide haben den gleichen xpath
        safe_button_xpath1 = "//*[@class='cbi-button cbi-button-save']"
        safe_button_xpath2 = "//*[@class='cbi-button cbi-button-save']"
        reset_button_xpath = "//*[@class='cbi-button cbi-button-reset']"

        ssh_keys_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(ssh_keys_field_id))
        ssh_password_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(ssh_password_field_id))
        ssh_password_confirm_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(ssh_password_confirm_field_id))
        safe_button_element1 = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_xpath(safe_button_xpath1))
        safe_button_element2 = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_xpath(safe_button_xpath2))
        reset_button_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_xpath(reset_button_xpath))

        if config['ssh_keys']:
            ssh_keys_field_element.send_keys(config['ssh_keys'])
            safe_button_element1.click()
        if config['password']:
            ssh_password_field_element.clear()
            ssh_password_field_element.send_keys(config['password'])
            ssh_password_confirm_field_element.clear()
            ssh_password_confirm_field_element.send_keys(config['password'])
            safe_button_element2.click()
        if config['reset']:
            reset_button_element.click()

    def setup_expert_network(self, config):
        Logger().debug("Setup 'Private WLAN' with: " + str(config), 3)
        self.browser.get(config['url'])

        ipv4_automatic_field_id = "cbi-portconfig-1-ipv4-dhcp"
        ipv4_static_field_id = "cbi-portconfig-1-ipv4-static"
        ipv4_none_field_id = "cbi-portconfig-1-ipv4-none"
        ipv6_automatic_field_id = "cbi-portconfig-1-ipv6-dhcp"
        ipv6_static_field_id = "cbi-portconfig-1-ipv6-static"
        ipv6_none_field_id = "cbi-portconfig-1-ipv6-none"
        mesh_wan_field_id = "cbid.portconfig.1.mesh_wan"
        mesh_lan_field_id = "cbid.portconfig.1.mesh_lan"
        safe_button_xpath = "//*[@class='cbi-button cbi-button-save']"
        reset_button_xpath = "//*[@class='cbi-button cbi-button-reset']"
        # a number has to be added.(like: "cbid.portconfig.1.dns1")
        static_dns_server_fiel_id = "cbid.portconfig.1.dns"
        static_dns_server_field_ids = []
        # the config has to look like server1, server2
        static_dns_server = config['static_dns_server'].split(', ')
        for i, server in enumerate(static_dns_server):
            static_dns_server_field_ids.append(static_dns_server_fiel_id + str(i))


        ipv4_automatic_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(ipv4_automatic_field_id))
        ipv4_static_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(ipv4_static_field_id))
        ipv4_none_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(ipv4_none_field_id))
        ipv6_automatic_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(ipv6_automatic_field_id))
        ipv6_static_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(ipv6_static_field_id))
        ipv6_none_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(ipv6_none_field_id))
        mesh_wan_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(mesh_wan_field_id))
        mesh_lan_field_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(mesh_lan_field_id))
        safe_button_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_xpath(safe_button_xpath))
        reset_button_element = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_xpath(reset_button_xpath))
        static_dns_server_field_elements = []

        # The checkboxes are set to 'display = none' via css.
        # Because selenium can't see them we have to set the checkboxes to 'display = inline'
        self.browser.execute_script("arguments[0].style.display = 'inline';",mesh_wan_field_element)
        self.browser.execute_script("arguments[0].style.display = 'inline';",mesh_lan_field_element)

        if config['ipv4'] == "automatic":
            ipv4_automatic_field_element.click()
        elif config['ipv4'] == "static":
            ipv4_static_field_element.click()
        else:
            ipv4_none_field_element.click()

        if config['ipv6'] == "automatic":
            ipv6_automatic_field_element.click()
        elif config['ipv6'] == "static":
            ipv6_static_field_element.click()
        else:
            ipv6_none_field_element.click()

        for i, server in enumerate(static_dns_server):
            static_dns_server_field_elements[i].send_keys(server)
            # TODO hier muss noch das Klicken des Add-Buttons hinzugefügt werden

        # Enable meshing on the WAN interface
        if config['mesh_wan']:
            if not mesh_wan_field_element.is_selected():
                mesh_wan_field_element.click()
        else:
            if mesh_wan_field_element.is_selected():
                mesh_wan_field_element.click()

        # Enable meshing on the LAN interface
        if config['mesh_lan']:
            if not mesh_lan_field_element.is_selected():
                mesh_lan_field_element.click()
        else:
            if mesh_lan_field_element.is_selected():
                mesh_lan_field_element.click()

        if config['reset']:
            reset_button_element.click()

        safe_button_element.click()



    def exit(self):
        self.browser.close()
        # TODO:
        #self.display.stop()