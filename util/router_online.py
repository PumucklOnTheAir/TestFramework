from threading import Thread
from router.router import Router, Mode
from log.loggersetup import LoggerSetup
import logging
from subprocess import Popen, PIPE
from network.remote_system import RemoteSystemJob
from util.dhclient import Dhclient


class RouterOnline(Thread):
    """
    Checks if the given Router is online and sets the Mode (normal, configuration)
    """""

    def __init__(self, router: Router):
        Thread.__init__(self)
        self.router = router
        self.daemon = True

    def run(self):
        logging.debug("%sCheck if Router is online ...", LoggerSetup.get_log_deep(1))
        try:
            Dhclient.update_ip(self.router.vlan_iface_name)
            self._test_connection()
        except FileExistsError:
            self._test_connection()
        except Exception:
            logging.debug("%s[*] Try again in a minute", LoggerSetup.get_log_deep(2))
        return

    def _test_connection(self):
        self.router.mode = Mode.normal
        process = Popen(["ping", "-c", "1", self.router.ip], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        if not(sterr.decode('utf-8') == "" and "Unreachable" not in stdout.decode('utf-8')):
            self.router.mode = Mode.configuration
            process = Popen(["ping", "-c", "1", self.router.ip], stdout=PIPE, stderr=PIPE)
            stdout, sterr = process.communicate()
            if not(sterr.decode('utf-8') == "" and "Unreachable" not in stdout.decode('utf-8')):
                logging.warning("%s[!] Router is not online", LoggerSetup.get_log_deep(2))
                self.router.mode = Mode.unknown
                return
        logging.debug("%s[+] Router online with IP " + str(self.router.ip), LoggerSetup.get_log_deep(2))


class RouterOnlineJob(RemoteSystemJob):
    """
    Encapsulate  RouterOnline as a job for the Server
    """""
    def run(self):
        router = self.remote_system
        router_info = RouterOnline(router)
        router_info.start()
        router_info.join()
        return {'router': router}

    def pre_process(self, server) -> {}:
        return None

    def post_process(self, data: {}, server) -> None:
        """
        Updates the router in the Server with the new information

        :param data: result from run()
        :param server: the Server
        :return:
        """
        ref_router = server.get_router_by_id(data['router'].id)
        ref_router.update(data['router'])  # Don't forget to update this method
