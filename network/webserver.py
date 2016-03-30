from log.loggersetup import LoggerSetup
import logging
from http.server import SimpleHTTPRequestHandler
import socketserver
from threading import Thread
import time
import os


class WebServer(Thread):

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
    PORT_WEBSERVER = 8000

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        os.chdir(WebServer.BASE_DIR)
        self.Handler = SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", WebServer.PORT_WEBSERVER), self.Handler)

    def run(self):
        logging.info("%sStart WebServer on port " + str(WebServer.PORT_WEBSERVER) + " ...", LoggerSetup.get_log_deep(1))
        try:
            self.httpd.serve_forever()
        except Exception as e:
            logging.debug("%s[-] WebServer couldn't get started", LoggerSetup.get_log_deep(2))
            raise e

    def join(self):
        logging.info("%sStop WebServer ...", LoggerSetup.get_log_deep(1))
        time.sleep(2)
        try:
            self.httpd.shutdown()
            logging.debug("%s[+] WebServer successfully stoped", LoggerSetup.get_log_deep(2))
        except Exception as e:
            logging.debug("%s[-] WebServer couldn't stoped", LoggerSetup.get_log_deep(2))
            logging.error("%s" + str(e), LoggerSetup.get_log_deep(1))
