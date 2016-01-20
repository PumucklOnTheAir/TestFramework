from pyroute2.ipdb import IPDB
from log.logger import Logger
import os
import time
import re


class Veth:
    """
    If we want to use a physical interface (like 'eth0') we have to create a bridge that connects the physical interface
    with Namespace by the 'veth'-interfaces.
    """""

    def __init__(self, ipdb: IPDB, veth_iface_name1: str, veth_iface_name2: str, veth_iface_ip1: str=None,
                 veth_iface_ip_mask1: int=None, veth_iface_ip2: str=None, veth_iface_ip_mask2: int=None):
        """
        Represents a 'veth'-interface.

        :param ipdb: IPDB is a transactional database, containing records, representing network stack objects.
                    Any change in the database is not reflected immidiately in OS, but waits until commit() is called.
        :param veth_iface_name1: like veth00
        :param veth_iface_name2: like veth0
        :param veth_iface_ip1:
        :param veth_iface_ip_mask1:
        :param veth_iface_ip2:
        :param veth_iface_ip_mask2:
        """
        self.ipdb = ipdb if ipdb else IPDB()
        self.veth_iface_name1 = veth_iface_name1
        self.veth_iface_name2 = veth_iface_name2
        self.veth_iface_ip1 = veth_iface_ip1
        self.veth_iface_ip_mask1 = veth_iface_ip_mask1
        self.veth_iface_ip2 = veth_iface_ip2
        self.veth_iface_ip_mask2 = veth_iface_ip_mask2

    def create_interface(self):
        """
        Creates a 'veth'-interface.
        """
        Logger().debug("Create Veth Interface ...", 2)
        try:
            self.ipdb.create(kind='veth', ifname=self.veth_iface_name1, peer=self.veth_iface_name2).commit()
            self.ipdb.interfaces[self.veth_iface_name1].up().commit()
            # veth0
            if self.veth_iface_ip1:
                iface = self.ipdb.interfaces[self.veth_iface_name1]
                iface.add_ip(self.veth_iface_ip1, self.veth_iface_ip_mask1).commit()
            # veth1
            if self.veth_iface_ip2:
                iface = self.ipdb.interfaces[self.veth_iface_name2]
                iface.add_ip(self.veth_iface_ip2, self.veth_iface_ip_mask2).commit()

            Logger().debug("[+] " + self.veth_iface_name1 + " <=> " + self.veth_iface_name2 + " created", 3)
        except Exception as e:
            Logger().debug("[-] " + self.veth_iface_name1 + self.veth_iface_name2 + " couldn't be created", 3)
            Logger().error(str(e), 3)

    def delete_interface(self, close_ipdb: bool=False):
        """
        Removes the 'veth'-interface.

        :param close_ipdb: If also the IPDB should be closed.
        """
        Logger().debug("Delete Veth Interface ...", 2)
        try:
            self.ipdb.interfaces[self.veth_iface_name1].remove().commit()
            if close_ipdb:
                self.ipdb.release()
            Logger().debug("[+] Interface(" + self.veth_iface_name1 + ") successfully deleted", 3)
        except KeyError as ke:
            Logger().debug("[+] Interface(" + self.veth_iface_name1 + ") is already deleted", 3)
            return
        except Exception as e:
            Logger().debug("[-] Interface(" + self.veth_iface_name1 +
                           ") couldn't be deleted. Try 'ip link delete <vlan_name>'", 3)
            Logger().error(str(e), 3)

    def set_new_ip(self, dhcp: bool, iface_name: str, new_ip: str=None, new_ip_mask: int=None):
        """
        Sets the IP either given by 'new_ip'-parameter or via dhclient.

        :param dhcp: should a dhclient be used?
        :param iface_name:
        :param new_ip:
        :param new_ip_mask:
        :return: the new IP with the format ip/mask
        """
        iface_ip = None
        if dhcp:
            try:
                self._wait_for_ip_assignment(iface_name)
                iface_ip = self._get_ip(iface_name)
                Logger().debug("[+] New IP " + iface_ip + " for " + iface_name + " by dhcp", 2)
            except TimeoutError as e:
                Logger().debug("[-] Couldn't get a new IP for " + iface_name + " by dhcp", 2)
        else:
            iface_ip = new_ip+"/"+str(new_ip_mask)
            Logger().debug("[+] New IP " + iface_ip + " for " + iface_name, 2)
        return iface_ip

    def _wait_for_ip_assignment(self, iface_name: str):
        """
        Waits until the dhcp-client got an ip.
        """
        Logger().debug("Wait for ip assignment via dhcp for Veth Interface(" + iface_name + ") ...", 3)
        current_ip = self._get_ip(iface_name).split('/')[0]
        if not self._get_ip(iface_name, not_this_ip=current_ip):
            os.system('dhclient ' + iface_name)
            i = 0
            while self._get_ip(iface_name, not_this_ip=current_ip) is None:
                time.sleep(0.5)
                i += 1
                if i == 20:
                    raise TimeoutError

    def _get_ip(self, iface_name: str, not_this_ip: str = None):
        """
        Reads the first IP from IPDB.

        :param iface_name:
        :param not_this_ip: If we know the first IP and are searching for another
        :return: the IP with the format ip/mask
        """
        iface = self.ipdb.interfaces[iface_name]
        ipaddr_dictionary = iface.ipaddr
        for i in range(len(ipaddr_dictionary)):
            ip = ipaddr_dictionary[i]['address']
            mask = ipaddr_dictionary[i]['prefixlen']
            if re.match("((((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3})(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))", ip):
                if ip != not_this_ip:
                    return ip + "/" + str(mask)
        return ""
