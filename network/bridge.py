from pyroute2.ipdb import IPDB
from log.loggersetup import LoggerSetup
import logging
import os
import time
import re


class Bridge:
    """
    If we want to use a physical interface (like 'eth0') we have to create a Bridge that connects the physical interface
    with Namespace by the 'veth'-interfaces.
    """""

    def __init__(self, ipdb: IPDB, bridge_name: str = 'br0', link_iface_name: str='eth0'):
        """
        Creates a 'bridge'-interface.

        :param ipdb: IPDB is a transactional database, containing records, representing network stack objects.
                    Any change in the database is not reflected immidiately in OS, but waits until commit() is called.
        :param bridge_name: like 'br0'
        :param link_iface_name: like 'eth0'
        """
        self.ipdb = ipdb if ipdb else IPDB()
        self.bridge_name = bridge_name
        self.ipdb.create(kind='bridge', ifname=self.bridge_name).commit()
        # self.ipdb.interfaces[self.bridge_name].up()
        self.add_iface(link_iface_name)
        self.set_new_ip(dhcp=True)

    def add_iface(self, iface_name):
        """
        Adds the given interface to the Bridge.

        :param iface_name:
        """
        self.ipdb.interfaces[self.bridge_name].add_port(self.ipdb.interfaces[iface_name]).commit()
        # self.ipdb.interfaces[iface_name].up()

    def del_iface(self, iface_name):
        """
        Deletes the given interface from the Bridge.

        :param iface_name:
        :return:
        """
        self.ipdb.interfaces[self.bridge_name].del_port(self.ipdb.interfaces[iface_name]).commit()

    def set_new_ip(self, dhcp: bool, new_ip: str=None, new_ip_mask: int=None):
        """
        Sets the IP either given by 'new_ip'-parameter or via dhclient.

        :param dhcp: should a dhclient be used?
        :param new_ip:
        :param new_ip_mask:
        :return: the new IP with the format ip/mask
        """
        iface_ip = None
        if dhcp:
            try:
                self._wait_for_ip_assignment()
                iface_ip = self._get_ip()
                logging.debug("%s[+] New IP " + iface_ip + " for " + self.bridge_name + " by dhcp",
                              LoggerSetup.get_log_deep(2))
            except TimeoutError:
                logging.debug("%s[-] Couldn't get a new IP for " + self.bridge_name + " by dhcp",
                              LoggerSetup.get_log_deep(2))
        else:
            iface_ip = new_ip + "/" + str(new_ip_mask)
            logging.debug("%s[+] New IP " + iface_ip + " for " + self.bridge_name, LoggerSetup.get_log_deep(2))
        return iface_ip

    def _wait_for_ip_assignment(self):
        """
        Waits until the dhcp-client got an ip
        """
        logging.debug("%sWait for ip assignment via dhcp for Bridge Interface(" + self.bridge_name + ") ...",
                      LoggerSetup.get_log_deep(3))
        current_ip = self._get_ip().split('/')[0]
        if not self._get_ip(not_this_ip=current_ip):
            os.system('dhclient ' + self.bridge_name)
            i = 0
            while self._get_ip(not_this_ip=current_ip) is None:
                time.sleep(0.5)
                i += 1
                if i == 20:
                    raise TimeoutError

    def _get_ip(self, not_this_ip: str = None):
        """
        Reads the first IP from IPDB.

        :param not_this_ip: If we know the first IP and are searching for another
        :return: the IP with the format ip/mask
        """
        iface = self.ipdb.interfaces[self.bridge_name]
        ipaddr_dictionary = iface.ipaddr
        for i in range(len(ipaddr_dictionary)):
            ip = ipaddr_dictionary[i]['address']
            mask = ipaddr_dictionary[i]['prefixlen']
            if re.match("((((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3})(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))", ip):
                if ip != not_this_ip:
                    return ip + "/" + str(mask)
        return ""

    def close(self, close_ipdb: bool=False):
        """
        Removes the 'bridge'-interface.

        :param close_ipdb: If also the IPDB should be closed.
        """
        logging.debug("%sClose Bridge Interface ...", LoggerSetup.get_log_deep(2))
        try:
            self.ipdb.interfaces[self.bridge_name].remove().commit()
            if close_ipdb:
                self.ipdb.release()
            logging.debug("%s[+] Interface(" + self.bridge_name + ") successfully deleted", LoggerSetup.get_log_deep(3))
        except KeyError:
            logging.debug("%s[+] Interface(" + self.bridge_name + ") is already deleted", LoggerSetup.get_log_deep(3))
            return
        except Exception as e:
            logging.debug("%s[-] Interface(" + self.bridge_name +
                          ") couldn't be deleted. Try 'ip link delete <bridge_name>'", LoggerSetup.get_log_deep(3))
            logging.error("%s" + str(e), LoggerSetup.get_log_deep(3))
