from log.logger import Logger
from http.server import SimpleHTTPRequestHandler
import socketserver
from threading import Thread
import time, os


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
        Logger().info("Start WebServer on port " + str(WebServer.PORT_WEBSERVER) + " ...", 1)
        try:
            self.httpd.serve_forever()
        except Exception as e:
            Logger().debug("[-] WebServer couldn't get started", 2)
            raise e

    def join(self):
        Logger().info("Stop WebServer ...", 1)
        time.sleep(5)
        try:
            self.httpd.shutdown()
            Logger().debug("[+] WebServer successfully stoped", 2)
        except Exception as e:
            Logger().debug("[-] WebServer couldn't stoped", 2)
            Logger().error(str(e), 1)
