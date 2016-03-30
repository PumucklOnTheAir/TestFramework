from subprocess import Popen
from selenium.webdriver.support.ui import WebDriverWait
from log.loggersetup import LoggerSetup
from .webdriver_phantomjs_extended import WebdriverPhantomjsExtended
import logging


class WebConfigurationAssist:
    """
    After a systemupgrade, the Router starts in config-mode without the possibility to connect again via SSH.
    Therefore this class uses selenium to parse the given webpage. All options given by the web interface of the Router
    can be set via the 'web_interface_config.yaml', except for the sysupgrade which isn't implemented yet.

    Info:
        - To use this class with firefox the following has to be installed: 'sudo apt-get install iceweasel xvfb'.
          Firefox needs a virtual display on a headless system.
        - At the moment PhantomJS is the used browser, 'cause the firefox throw an exception(dbus not found).
          But PhantomJS works only correctly in cooperation with namespaces,
          if a special command (ip netns exec <namespace>) is added too.
          Therefore I added a parameter to the webdriver function from selenium.
    """""

    def __init__(self, config, router):
        """
        Starts the browser Phantomjs to configure the webpage of the router in the given namespace.

        :param config: {node_name, mesh_vpn, limit_bandwidth, show_location, latitude, longitude, altitude,contact, ...}
        :param router: Router-Obj
        """

        logging.debug("%sCreate WebConfigurationAssist ...", LoggerSetup.get_log_deep(2))
        self.config = config
        self.router = router
        try:
            pre_command = ['ip', 'netns', 'exec', self.router.namespace_name]
            self.browser = WebdriverPhantomjsExtended(pre_command=pre_command)
            self.browser.get(self.router.ip)
            logging.debug("%s[+] Browser started", LoggerSetup.get_log_deep(3))
            logging.debug("%s[*] Config: " + str(self.config), LoggerSetup.get_log_deep(3))
        except Exception as e:
            logging.debug("%s[-] Couldn't start Browser", LoggerSetup.get_log_deep(3))
            raise e

    def setup_wizard(self):
        """
        Sets the values provided by the wizard (in the WebConfiguration)

        Info:
            Node name:          [text]

            MeshVPN:            [checkbox]
            Limit bandwidth:    [checkbox]

            Node on the map:    [checkbox]
                Latitude:           [text]
                Longitude:          [text]
                Altitude:           [text]

            Contact info:       [text]

            Submit:             [button]
        """
        logging.debug("%sSetup 'wizard' ...", LoggerSetup.get_log_deep(2))
        self.browser.get('http://' + self.router.ip + '/cgi-bin/luci/gluon-config-mode/')

        node_name_field_id = "cbid.wizard.1._hostname"
        mesh_vpn_field_id = "cbid.wizard.1._meshvpn"
        limit_bandwidth_field_id = "cbid.wizard.1._limit_enabled"
        show_location_field_id = "cbid.wizard.1._location"
        latitude_field_id = "cbid.wizard.1._latitude"
        longitude_field_id = "cbid.wizard.1._longitude"
        altitude_field_id = "cbid.wizard.1._altitude"
        contact_field_id = "cbid.wizard.1._contact"
        safe_restart_button_xpath = "//*[@class='cbi-button cbi-button-save']"

        node_name_field_element = self._get_element_by_id(node_name_field_id)
        mesh_vpn_field_element = self._get_element_by_id(mesh_vpn_field_id)
        show_location_field_element = self._get_element_by_id(show_location_field_id)
        contact_field_element = self._get_element_by_id(contact_field_id)
        safe_restart_button_element = self._get_element_by_xpath(safe_restart_button_xpath)

        # The checkboxes are set to 'display = none' via css.
        # Because selenium can't see them we have to set the checkboxes to 'display = inline'
        self.browser.execute_script("arguments[0].style.display = 'inline';", mesh_vpn_field_element)
        self.browser.execute_script("arguments[0].style.display = 'inline';", show_location_field_element)

        node_name_field_element.clear()
        node_name_field_element.send_keys(self.config['node_name'])

        self._click_checkbox(mesh_vpn_field_element, self.config['mesh_vpn'])

        if self.config['mesh_vpn']:
            limit_bandwidth_field_element = self._get_element_by_id(limit_bandwidth_field_id)
            self._click_checkbox(limit_bandwidth_field_element, self.config['limit_bandwidth'])

        self._click_checkbox(show_location_field_element, self.config['show_location'])

        if self.config['show_location']:
            latitude_field_element = self._get_element_by_id(latitude_field_id)
            longitude_field_element = self._get_element_by_id(longitude_field_id)
            altitude_field_element = self._get_element_by_id(altitude_field_id)
            latitude_field_element.clear()
            latitude_field_element.send_keys(self.config['latitude'])
            longitude_field_element.clear()
            longitude_field_element.send_keys(self.config['longitude'])
            altitude_field_element.clear()
            altitude_field_element.send_keys(self.config['altitude'])

        contact_field_element.clear()
        contact_field_element.send_keys(self.config['contact'])

        safe_restart_button_element.click()

        self._safe_public_key()

    def _safe_public_key(self):
        """
        Safes the public-key that is given after the wizard-configuration.

        Info:
            #<node_name>
            <public-key>
        """
        div_public_key_xpath = "//*[@class='the-key']"

        div_public_key_field_element = self._get_element_by_xpath(div_public_key_xpath)
        raw_public_key_info = div_public_key_field_element.text
        self.router.public_key = raw_public_key_info.split()[2]

    def setup_expert_private_wlan(self):
        """
        Extend your private network by bridging the WAN interface with a seperate WLAN

        Info:
            private WLAN:   [checkbox]
                ssid:           [text]
                ssid key:       [text]
            submit:         [button]
        """
        logging.debug("%sSetup 'Private WLAN' ...", LoggerSetup.get_log_deep(2))
        self.browser.get('http://' + self.router.ip + '/cgi-bin/luci/admin/privatewifi/')

        private_wlan_field_id = "cbid.wifi.1.enabled"
        ssid_field_id = "cbid.wifi.1.ssid"
        ssid_key_field_id = "cbid.wifi.1.key"
        safe_button_xpath = "//*[@class='cbi-button cbi-button-save']"

        private_wlan_field_element = self._get_element_by_id(private_wlan_field_id)
        safe_button_element = self._get_element_by_xpath(safe_button_xpath)

        # The checkboxes are set to 'display = none' via css.
        # Because selenium can't see them we have to set the checkboxes to 'display = inline'
        self.browser.execute_script("arguments[0].style.display = 'inline';", private_wlan_field_element)

        self._click_checkbox(private_wlan_field_element, self.config['private_wlan'])
        if self.config['private_wlan']:
            ssid_field_element = self._get_element_by_id(ssid_field_id)
            ssid_key_field_element = self._get_element_by_id(ssid_key_field_id)
            ssid_field_element.clear()
            ssid_field_element.send_keys(self.config['ssid'])
            ssid_key_field_element.clear()
            ssid_key_field_element.send_keys(self.config['ssid_key'])

        safe_button_element.click()

    def setup_expert_remote_access(self):
        """
        Sets the SSH-Keys and a password, given by the config

        Info:
            ssh keys:   [text]

            submit:     [button]

            password:   [text]
            confirm:    [text]

            submit:     [button]
        """
        logging.debug("%sSetup 'Remote Access' ...", LoggerSetup.get_log_deep(2))
        self.browser.get('http://' + self.router.ip + '/cgi-bin/luci/admin/remote/')

        ssh_keys_field_id = "cbid.system._keys._data"
        ssh_password_field_id = "cbid.system._pass.pw1"
        ssh_password_confirm_field_id = "cbid.system._pass.pw2"
        safe_button_xpath1 = "//*[@class='cbi-button cbi-button-save']"

        ssh_keys_field_element = self._get_element_by_id(ssh_keys_field_id)

        if self.config['ssh_keys']:
            ssh_keys_field_element.send_keys(self.config['ssh_keys'])
            safe_button_element1 = self._get_element_by_xpath(safe_button_xpath1)
            safe_button_element1.click()
        if self.config['password']:
            ssh_password_field_element = self._get_element_by_id(ssh_password_field_id)
            ssh_password_confirm_field_element = self._get_element_by_id(ssh_password_confirm_field_id)
            ssh_password_field_element.clear()
            ssh_password_field_element.send_keys(self.config['password'])
            ssh_password_confirm_field_element.clear()
            ssh_password_confirm_field_element.send_keys(self.config['password'])

            # Problem is that the two buttons on this page are identical and selenium doesn't work with a whole xpath
            safe_button_element1 = self._get_element_by_xpath(safe_button_xpath1)
            self.browser.execute_script("arguments[0].value = 'Submit1';", safe_button_element1)
            safe_button_xpath2 = "//*[@value='Submit']"
            safe_button_element2 = self._get_element_by_xpath(safe_button_xpath2)

            safe_button_element2.click()

    def setup_expert_network(self):
        """
        Sets the given network configurations

        Info:
            ipv4:       [selectbox]
                none.       [option]
                auto:       [option]
                static:     [option]
                    ip:         [text]
                    mask:       [text]
                    gw:         [text]
            ipv6:       [selectbox]
                none.       [option]
                auto:       [option]
                static:     [option]
                    ip:         [text]
                    gw:         [text]
            dns server: [text]
            wan inface: [checkbox]
            lan inface: [checkbox]

            submit:     [button]
        """
        logging.debug("%sSetup 'Network' ...", LoggerSetup.get_log_deep(2))
        self.browser.get('http://' + self.router.ip + '/cgi-bin/luci/admin/portconfig/')

        ipv4_automatic_field_id = "cbi-portconfig-1-ipv4-dhcp"
        ipv4_static_field_id = "cbi-portconfig-1-ipv4-static"
        ipv4_none_field_id = "cbi-portconfig-1-ipv4-none"
        ipv4_ip_field_id = "cbid.portconfig.1.ipv4_addr"
        ipv4_netmask_field_id = "cbid.portconfig.1.ipv4_netmask"
        ipv4_gateway_field_id = "cbid.portconfig.1.ipv4_gateway"
        ipv6_automatic_field_id = "cbi-portconfig-1-ipv6-dhcpv6"
        ipv6_static_field_id = "cbi-portconfig-1-ipv6-static"
        ipv6_none_field_id = "cbi-portconfig-1-ipv6-none"
        ipv6_ip_field_id = "cbid.portconfig.1.ipv6_addr"
        ipv6_gateway_field_id = "cbid.portconfig.1.ipv6_gateway"
        mesh_wan_field_id = "cbid.portconfig.1.mesh_wan"
        mesh_lan_field_id = "cbid.portconfig.1.mesh_lan"
        safe_button_xpath = "//*[@class='cbi-button cbi-button-save']"
        # TODO: muss noch für mehere DNS-Server angepasst werden
        static_dns_server_field_id = "cbid.portconfig.1.dns.1"

        ipv4_automatic_field_element = self._get_element_by_id(ipv4_automatic_field_id)
        ipv4_static_field_element = self._get_element_by_id(ipv4_static_field_id)
        ipv4_none_field_element = self._get_element_by_id(ipv4_none_field_id)
        ipv6_automatic_field_element = self._get_element_by_id(ipv6_automatic_field_id)
        ipv6_static_field_element = self._get_element_by_id(ipv6_static_field_id)
        ipv6_none_field_element = self._get_element_by_id(ipv6_none_field_id)
        mesh_wan_field_element = self._get_element_by_id(mesh_wan_field_id)
        mesh_lan_field_element = self._get_element_by_id(mesh_lan_field_id)
        safe_button_element = self._get_element_by_xpath(safe_button_xpath)
        # TODO: muss noch für mehere DNS-Server angepasst werden
        static_dns_server_field_element = self._get_element_by_id(static_dns_server_field_id)

        # The checkboxes are set to 'display = none' via css.
        # Because selenium can't see them we have to set the checkboxes to 'display = inline'
        self.browser.execute_script("arguments[0].style.display = 'inline';", mesh_wan_field_element)
        self.browser.execute_script("arguments[0].style.display = 'inline';", mesh_lan_field_element)

        if self.config['ipv4'] == "automatic":
            ipv4_automatic_field_element.click()
        elif self.config['ipv4'] == "static":
            ipv4_static_field_element.click()
            ipv4_ip_field_element = self._get_element_by_id(ipv4_ip_field_id)
            ipv4_netmask_field_element = self._get_element_by_id(ipv4_netmask_field_id)
            ipv4_gateway_field_element = self._get_element_by_id(ipv4_gateway_field_id)
            ipv4_ip_field_element.clear()
            ipv4_ip_field_element.send_keys(self.config['ipv4_address'])
            ipv4_netmask_field_element.clear()
            ipv4_netmask_field_element.send_keys(self.config['ipv4_netmask'])
            ipv4_gateway_field_element.clear()
            ipv4_gateway_field_element.send_keys(self.config['gateway_v4'])
        else:
            ipv4_none_field_element.click()

        if self.config['ipv6'] == "automatic":
            ipv6_automatic_field_element.click()
        elif self.config['ipv6'] == "static":
            ipv6_static_field_element.click()
            ipv6_ip_field_element = self._get_element_by_id(ipv6_ip_field_id)
            ipv6_gateway_field_element = self._get_element_by_id(ipv6_gateway_field_id)
            ipv6_ip_field_element.clear()
            ipv6_ip_field_element.send_keys(self.config['ipv6_address'])
            ipv6_gateway_field_element.clear()
            ipv6_gateway_field_element.send_keys(self.config['gateway_v6'])
        else:
            ipv6_none_field_element.click()

        # TODO: muss noch für mehere DNS-Server angepasst werden
        static_dns_server_field_element.send_keys(self.config['static_dns_server'])

        # Enable meshing on the WAN/LAN interface
        self._click_checkbox(mesh_wan_field_element, self.config['mesh_wan'])
        self._click_checkbox(mesh_lan_field_element, self.config['mesh_lan'])
        safe_button_element.click()

    def setup_expert_mesh_vpn(self):
        """
        Sets the given mesh-vpn configuration

        Info:
            security mode:  [radiobutton]
            perform. mode:  [radiobutton]

            submit:         [button]
        """
        logging.debug("%sSetup 'Mesh VPN' ...", LoggerSetup.get_log_deep(2))
        self.browser.get('http://' + self.router.ip + '/cgi-bin/luci/admin/mesh_vpn_fastd/')

        security_mode_field_id = "cbid.mesh_vpn.1.mode1"
        performance_mode_field_id = "cbid.mesh_vpn.1.mode2"
        safe_button_xpath = "//*[@class='cbi-button cbi-button-save']"

        security_mode_field_element = self._get_element_by_id(security_mode_field_id)
        performance_mode_field_element = self._get_element_by_id(performance_mode_field_id)
        safe_button_element = self._get_element_by_xpath(safe_button_xpath)

        self._click_checkbox(security_mode_field_element, self.config['security_mode'])
        self._click_checkbox(performance_mode_field_element, self.config['performance_mode'])
        safe_button_element.click()

    def setup_expert_wlan(self):
        """
        Sets the given wlan configuration

        Info:
            client network: [checkbox]
            mesh network:   [checkbox]
            transmission p.:[selectbox]

            submit:         [Submit]
        """
        logging.debug("%sSetup 'WLAN' ...", LoggerSetup.get_log_deep(2))
        self.browser.get('http://' + self.router.ip + '/cgi-bin/luci/admin/wifi-config/')

        client_network_field_id = "cbid.wifi.1.radio0_client_enabled"
        mesh_network_field_id = "cbid.wifi.1.radio0_mesh_enabled"
        safe_button_xpath = "//*[@class='cbi-button cbi-button-save']"
        transmission_power_field_id = "cbi-wifi-1-radio0_txpower-"
        transmission_power_field_ids = list()
        for i in range(0, 19):
            if i == 1 or i == 2 or i == 3 or i == 6:
                continue
            transmission_power_field_ids.append(transmission_power_field_id + str(i))
        transmission_power_field_ids.append(transmission_power_field_id + "default")
        client_network_field_element = self._get_element_by_id(client_network_field_id)
        mesh_network_field_element = self._get_element_by_id(mesh_network_field_id)
        safe_button_element = self._get_element_by_xpath(safe_button_xpath)
        transmission_power_field_elements = []
        for field_id in transmission_power_field_ids:
            transmission_power_field_element = self._get_element_by_id(field_id)
            transmission_power_field_elements.append(transmission_power_field_element)

        # The checkboxes are set to 'display = none' via css.
        # Because selenium can't see them we have to set the checkboxes to 'display = inline'
        self.browser.execute_script("arguments[0].style.display = 'inline';", client_network_field_element)
        self.browser.execute_script("arguments[0].style.display = 'inline';", mesh_network_field_element)

        self._click_checkbox(client_network_field_element, self.config['client_network'])
        self._click_checkbox(mesh_network_field_element, self.config['mesh_network'])

        if self.config['transmission_power'] == "default":
            transmission_power_field_elements[-1].click()
        else:
            transmission_power_field_elements[int(self.config['transmission_power'])].click()
        safe_button_element.click()

    def setup_expert_autoupdate(self):
        """
        Does a automatic update by the given configuration

        Info:
            auto update:    [checkbox]
            branch:         [selectbox]
                stable:         [option]
                beta:           [option]
                expmental:      [option]

            submit:         [button]
        """
        logging.debug("%sSetup 'AutoUpdate' ...", LoggerSetup.get_log_deep(2))
        self.browser.get('http://' + self.router.ip + '/cgi-bin/luci/admin/autoupdater/')

        autoupdate_field_id = "cbid.autoupdater.settings.enabled"
        branch_stable_field_id = "cbi-autoupdater-settings-branch-stable"
        branch_beta_field_id = "cbi-autoupdater-settings-branch-beta"
        branch_experimental_field_id = "cbi-autoupdater-settings-branch-experimental"
        safe_button_xpath = "//*[@class='cbi-button cbi-button-save']"

        autoupdate_field_element = self._get_element_by_id(autoupdate_field_id)
        branch_stable_field_element = self._get_element_by_id(branch_stable_field_id)
        branch_beta_field_element = self._get_element_by_id(branch_beta_field_id)
        branch_experimental_field_element = self._get_element_by_id(branch_experimental_field_id)
        safe_button_element = self._get_element_by_xpath(safe_button_xpath)

        # The checkboxes are set to 'display = none' via css.
        # Because selenium can't see them we have to set the checkboxes to 'display = inline'
        self.browser.execute_script("arguments[0].style.display = 'inline';", autoupdate_field_element)
        self.browser.execute_script("arguments[0].style.display = 'inline';", branch_stable_field_element)
        self.browser.execute_script("arguments[0].style.display = 'inline';", branch_beta_field_element)
        self.browser.execute_script("arguments[0].style.display = 'inline';", branch_experimental_field_element)

        self._click_checkbox(autoupdate_field_element, self.config['auto_update'])

        if self.config['branch'] == "stable":
            branch_stable_field_element.click()
        elif self.config['branch'] == "beta":
            branch_beta_field_element.click()
        else:
            branch_experimental_field_element.click()
        safe_button_element.click()

    # def setup_expert_upgrade(self, config):
        # TODO

    def exit(self):
        """
        Close the browser
        """
        self.browser.close()
        logging.debug("Kill PhantomJS")
        # Otherwise the phantomjs-processes are still open
        Popen(["pkill", "phantomjs"])
        # self.display.stop()

    @staticmethod
    def _click_checkbox(field_element, condition):
        """
        Clicks on the given object if it isn't and it should or otherwise.

        :param field_element: checkbox-object
        :param condition: the value that the checkbox should have
        """
        if condition:
            if not field_element.is_selected():
                field_element.click()
        else:
            if field_element.is_selected():
                field_element.click()

    def _get_element_by_id(self, field_id: str):
        return WebDriverWait(self.browser, 10).until(lambda driver: driver.find_element_by_id(field_id))

    def _get_element_by_xpath(self, xpath: str):
        return WebDriverWait(self.browser, 10).until(lambda driver: driver.find_element_by_xpath(xpath))
