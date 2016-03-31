from selenium.common.exceptions import WebDriverException
from selenium.webdriver.phantomjs.service import Service
from selenium.webdriver.common import utils
import platform
import subprocess
import time


class ServicePhantomjsExtended(Service):
    """
    Extend the Service class with a option to call PhantomJS inside a network namespace.
    """""

    def __init__(self, executable_path, port=0, pre_command=None, service_args=None, log_path=None):
        """
        :param executable_path: Path to PhantomJS binary
        :param port: Port the service is running on
        :param pre_command: Is in case the 'executable_path' has to bee called in another command.
                            e.g.: if network namespaces are used,
                            we need to execute phantom after 'ip netns exec <namespace_name>'
        :param service_args: A List of other command line options to pass to PhantomJS
        :param log_path: Path for PhantomJS service to log to
        """
        super().__init__(executable_path, port, service_args, log_path)
        self.pre_command = pre_command

    def start(self):
        """
        Starts PhantomJS with GhostDriver.

        :exception WebDriverException: Raised either when it can't start the service
                                        or when it can't connect to the service.
        """
        try:
            self.process = subprocess.Popen(self.pre_command + self.service_args, stdin=subprocess.PIPE,
                                            close_fds=platform.system() != 'Windows',
                                            stdout=self._log, stderr=self._log)
        except Exception as e:
            raise WebDriverException("Unable to start phantomjs with ghostdriver: %s" % e)
        count = 0
        while not utils.is_connectable(self.port):
            count += 1
            time.sleep(1)
            if count == 30:
                raise WebDriverException("Can not connect to GhostDriver on port {}".format(self.port))
