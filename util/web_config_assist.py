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
        # TODO: On raspberry pi necessary: create virtual display
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
        NODE_NAME_FIELD_ID = "cbid.wizard.1._hostname"
        MESH_VPN_FIELD_ID = "cbid.wizard.1._meshvpn"
        LIMIT_BANDWIDTH_FIELD_ID = "cbid.wizard.1._limit_enabled"
        SHOW_LOCATION_FIELD_ID = "cbid.wizard.1._location"
        LATITUDE_FIELD_ID = "cbid.wizard.1._latitude"
        LONGITUDE_FIELD_ID = "cbid.wizard.1._longitude"
        ALTITUDE_FIELD_ID = "cbid.wizard.1._altitude"
        CONTACT_FIELD_ID = "cbid.wizard.1._contact"
        SAFE_RESTART_BUTTON_XPATH = "/html/body/div[2]/div/form/div[3]/input"

        NODE_NAME_FIELD_ELEMENT = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(NODE_NAME_FIELD_ID))
        MESH_VPN_FIELD_ELEMENT  = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(MESH_VPN_FIELD_ID))
        LIMIT_BANDWIDTH_FIELD_ELEMENT = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(LIMIT_BANDWIDTH_FIELD_ID))
        SHOW_LOCATION_FIELD_ELEMENT = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(SHOW_LOCATION_FIELD_ID))
        LATITUDE_FIELD_ELEMENT = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(LATITUDE_FIELD_ID))
        LONGITUDE_FIELD_ELEMENT = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(LONGITUDE_FIELD_ID))
        ALTITUDE_FIELD_ELEMENT = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(ALTITUDE_FIELD_ID))
        CONTACT_FIELD_ELEMENT = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_id(CONTACT_FIELD_ID))
        SAFE_RESTART_BUTTON_ELEMENT = WebDriverWait(self.browser, 10).\
            until(lambda driver: driver.find_element_by_xpath(SAFE_RESTART_BUTTON_XPATH))

        NODE_NAME_FIELD_ELEMENT.clear()
        NODE_NAME_FIELD_ELEMENT.send_keys(wizard_config['node_name'])

        if wizard_config['mesh_vpn']:
            MESH_VPN_FIELD_ELEMENT.click()
            if wizard_config['limit_bandwidth']:
                LIMIT_BANDWIDTH_FIELD_ELEMENT.click()

        if wizard_config['show_location']:
            SHOW_LOCATION_FIELD_ELEMENT.click()
            LATITUDE_FIELD_ELEMENT.clear()
            LATITUDE_FIELD_ELEMENT.send_keys(wizard_config['latitude'])
            LONGITUDE_FIELD_ELEMENT.clear()
            LONGITUDE_FIELD_ELEMENT.send_keys(wizard_config['longitude'])
            ALTITUDE_FIELD_ELEMENT.clear()
            ALTITUDE_FIELD_ELEMENT.send_keys(wizard_config['altitude'])

        CONTACT_FIELD_ELEMENT.send_keys(wizard_config['contact'])

        SAFE_RESTART_BUTTON_ELEMENT.click()

    #def setup_expert_mode(self):
        # TODO

    def exit(self):
        self.browser.close()
        # TODO:
        #self.display.stop()