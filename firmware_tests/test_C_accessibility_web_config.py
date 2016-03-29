from server.test import FirmwareTest
from router.router import Mode
from network.webdriver_phantomjs_extended import WebdriverPhantomjsExtended
from log.loggersetup import LoggerSetup
import logging


class TestAccessibilityWebConfig(FirmwareTest):
    """
    Tests if WebInterface (wizard and expert) of the Router is accessible.
    The Router has to be in configuration-mode therefore
    """""

    def test_accessibility_of_wizard(self):
        """
        Test:
            1. Router is in configuration-mode
            2. The page-source of the wizard-page doesn't contain "Not Found" => wizard-page exist
        """
        logging.debug("%sTest: Accessibility of the WebInterface: Wizard-Page", LoggerSetup.get_log_deep(1))
        assert self.remote_system.mode == Mode.configuration
        logging.debug("%s[" + u"\u2714" + "] Correct Mode", LoggerSetup.get_log_deep(2))
        pre_command = ['ip', 'netns', 'exec', self.remote_system.namespace_name]
        browser = WebdriverPhantomjsExtended(pre_command=pre_command)
        browser.get(self.remote_system.ip)
        browser.get('http://' + self.remote_system.ip)
        self.assertTrue("Not Found" not in browser.page_source, "The Wizard-Page isn't accessible")
        logging.debug("%s[" + u"\u2714" + "] The Wizard-Page is accessible", LoggerSetup.get_log_deep(2))
        browser.close()

    def test_accessibility_of_expert(self):
        """
        Test:
            1. Router is in configuration-mode
            2. The page-source of the expert-page doesn't contain "Not Found" => expert-page exist
        """
        logging.debug("%sTest: Accessibility of the WebInterface: Expert-Page", LoggerSetup.get_log_deep(1))
        assert self.remote_system.mode == Mode.configuration
        logging.debug("%s[" + u"\u2714" + "] Correct Mode", LoggerSetup.get_log_deep(2))
        pre_command = ['ip', 'netns', 'exec', self.remote_system.namespace_name]
        browser = WebdriverPhantomjsExtended(pre_command=pre_command)
        browser.get(self.remote_system.ip)
        browser.get('http://' + self.remote_system.ip + '/cgi-bin/luci/admin/')
        self.assertTrue("Not Found" not in browser.page_source, "The Expert-Page isn't accessible")
        logging.debug("%s[" + u"\u2714" + "] The Expert-Page is accessible", LoggerSetup.get_log_deep(2))
        browser.close()
