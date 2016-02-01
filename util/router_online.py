from threading import Thread
from router.router import Router, Mode
from log.logger import Logger
from subprocess import Popen, PIPE
import os


class RouterOnline(Thread):

    def __init__(self, router: Router):
        Thread.__init__(self)
        self.router = router
        self.daemon = True

    def run(self):
        Logger().debug("Check if Router is online ...", 2)
        self.router.mode = Mode.normal
        process = Popen(["ping", "-c", "1", self.router.ip], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        if sterr.decode('utf-8') == "":
            Logger().debug("[+] Router online with IP " + str(self.router.ip), 3)
            return

        self.router.mode = Mode.configuration
        process = Popen(["ping", "-c", "1", self.router.ip], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        if sterr.decode('utf-8') == "":
            Logger().debug("[+] Router online with IP " + str(self.router.ip), 3)
            return

        Logger().debug("[-] Router is not online", 3)
        self.router.mode = Mode.unknown
