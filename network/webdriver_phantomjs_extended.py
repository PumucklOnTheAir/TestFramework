from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from .service_phantomjs_extended import ServicePhantomjsExtended


class WebdriverPhantomjsExtended(WebDriver):
    """
    Extend the WebDriver class with a option to call PhantomJS inside a network namespace.
    """

    def __init__(self, executable_path="phantomjs",
                 port=0, desired_capabilities=DesiredCapabilities.PHANTOMJS, pre_command=None,
                 service_args=None, service_log_path=None):
        """
        Creates a new instance of the PhantomJS / Ghostdriver.

        Starts the service and then creates new instance of the driver.

        :Args:
         - executable_path - path to the executable. If the default is used it assumes the executable is in the $PATH
         - port - port you would like the service to run, if left as 0, a free port will be found.
         - desired_capabilities: Dictionary object with non-browser specific
           capabilities only, such as "proxy" or "loggingPref".
         - pre_command : Is in case the 'executable_path' has to bee called in another command.
                         e.g.: if network namespaces are used,
                         we need to execute phantom after 'ip netns exec <namespace_name>'
         - service_args : A List of command line arguments to pass to PhantomJS
         - service_log_path: Path for phantomjs service to log to.
        """

        self.service = ServicePhantomjsExtended(executable_path, port=port, pre_command=pre_command, service_args=service_args, log_path=service_log_path)
        self.service.start()

        try:
            RemoteWebDriver.__init__(self, command_executor=self.service.service_url, desired_capabilities=desired_capabilities)
        except:
            self.quit()
            raise

        self._is_remote = False
