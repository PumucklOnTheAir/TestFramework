from http.server import SimpleHTTPRequestHandler
from log.loggersetup import LoggerSetup
from threading import Thread
import logging
import socketserver
import time
import os


class WebServer(Thread):
    """
    This class make it possible to start and stop a WebServer in a new thread.
    """""

    # This is your Project Root
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    PORT_WEBSERVER = 8000

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        os.chdir(WebServer.BASE_DIR)
        self.Handler = SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", WebServer.PORT_WEBSERVER), self.Handler)

    def run(self):
        """
        Starts the WebServer.

        :exception Exception: If the WebServer couldn't get started
        """
        logging.info("%sStart WebServer on port " + str(WebServer.PORT_WEBSERVER) + " ...", LoggerSetup.get_log_deep(1))
        try:
            self.httpd.serve_forever()
        except Exception as e:
            logging.debug("%s[-] WebServer couldn't get started", LoggerSetup.get_log_deep(2))
            raise e

    def join(self):
        """
        Stops the WebServer.
        """
        logging.info("%sStop WebServer ...", LoggerSetup.get_log_deep(1))
        time.sleep(2)
        try:
            self.httpd.shutdown()
            logging.debug("%s[+] WebServer successfully stoped", LoggerSetup.get_log_deep(2))
        except Exception as e:
            logging.debug("%s[-] WebServer couldn't stoped", LoggerSetup.get_log_deep(2))
            logging.error("%s" + str(e), LoggerSetup.get_log_deep(1))
