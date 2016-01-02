from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from pyvirtualdisplay import Display
from log.logger import Logger


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

    def setup_wizard(self, wizard_config):
        """
        Sets the values provided by the wizard (in the WebConfiguration)
        :param wizard_config: {node_name, mesh_vpn, limit_bandwidth, show_location, latitude, longitude, altitude,contact}
        """
        Logger().debug("Setup 'wizard' with: " + str(wizard_config), 3)
        self.browser.get(wizard_config['url'])
        node_name_field_id = "cbid.wizard.1._hostname"
        mesh_vpn_field_id = "cbid.wizard.1._meshvpn"
        limit_bandwidth_field_id = "cbid.wizard.1._limit_enabled"
        show_location_field_id = "cbid.wizard.1._location"
        latitude_field_id = "cbid.wizard.1._latitude"
        longitude_field_id = "cbid.wizard.1._longitude"
        altitude_field_id = "cbid.wizard.1._altitude"
        contact_field_id = "cbid.wizard.1._contact"
        safe_restart_button_xpath = "/html/body/div[2]/div/form/div[3]/input"

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

        node_name_field_element.clear()
        node_name_field_element.send_keys(wizard_config['node_name'])

        if wizard_config['mesh_vpn']:
            mesh_vpn_field_element.click()
            if wizard_config['limit_bandwidth']:
                limit_bandwidth_field_element.click()

        if wizard_config['show_location']:
            show_location_field_element.click()
            latitude_field_element.clear()
            latitude_field_element.send_keys(wizard_config['latitude'])
            longitude_field_element.clear()
            longitude_field_element.send_keys(wizard_config['longitude'])
            altitude_field_element.clear()
            altitude_field_element.send_keys(wizard_config['altitude'])

        contact_field_element.send_keys(wizard_config['contact'])

        safe_restart_button_element.click()

    #def setup_expert_mode(self):
        # TODO

    def exit(self):
        self.browser.close()
        # TODO:
        #self.display.stop()