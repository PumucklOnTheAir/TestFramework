from server.test import FirmwareTest
from router.router import Mode
from network.webdriver_phantomjs_extended import WebdriverPhantomjsExtended


class AccessibilityWebConfig(FirmwareTest):
    """
    Test if WebInterface (wizard and expert) of the Router is accessible.
    The Router has to be in configuration-mode therefore
    """""

    def test_accessibility_of_wizard(self):
        assert self.remote_system.mode == Mode.configuration
        pre_command = ['ip', 'netns', 'exec', self.remote_system.namespace_name]
        browser = WebdriverPhantomjsExtended(pre_command=pre_command)
        browser.get(self.remote_system.ip)
        browser.get('http://' + self.remote_system.ip + '/cgi-bin/luci/gluon-config-mode/')
        assert browser.title != ""
        browser.close()

    def test_accessibility_of_expert(self):
        assert self.remote_system.mode == Mode.configuration
        pre_command = ['ip', 'netns', 'exec', self.remote_system.namespace_name]
        browser = WebdriverPhantomjsExtended(pre_command=pre_command)
        browser.get(self.remote_system.ip)
        browser.get('http://' + self.remote_system.ip + '/cgi-bin/luci/admin/')
        assert browser.title != ""
        browser.close()
