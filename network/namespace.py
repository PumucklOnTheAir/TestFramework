from pyroute2.netns.nslink import NetNS
from pyroute2.ipdb import IPDB
from pyroute2 import netns
import re
import sys
import traceback
from log.logger import Logger
import os
import time


class Namespace:
    """
    A network namespace is logically another copy of the network stack,
    with its own routes, firewall rules, and network devices.

    By default a process inherits its network namespace from its parent.
    Initially all the processes share the same default network namespace
    from the init process.
    """""

    def __init__(self, ipdb: IPDB, nsp_name: str):
        """
        Creats a namespace for a specific vlan_iface

        :param nsp_name:
        :param ipdb: IPDB is a transactional database, containing records, representing network stack objects.
                    Any change in the database is not reflected immidiately in OS, but waits until commit() is called.
        """
        Logger().debug("Create Namespace ...", 2)
        self.ipdb = ipdb if ipdb else IPDB()
        self.ipdb_netns = None
        self.nsp_name = nsp_name
        try:
            self.ipdb_netns = IPDB(nl=NetNS(nsp_name))
            netns.setns(nsp_name)
            self.ipdb_netns.interfaces['lo'].up().commit()
            Logger().debug("[+] Namespace(" + nsp_name + ") successfully created", 3)
            # self.encapsulate_interface()
        except Exception as e:
            Logger().debug("[-] Couldn't create Namespace(" + nsp_name + ")", 3)
            for tb in traceback.format_tb(sys.exc_info()[2]):
                Logger().error(tb, 3)
            Logger().error(str(e), 3)
            self.remove()

    def remove(self):
        """
        Removes the virtual namespace and interface.
        """
        Logger().debug("Delete Namespace ...", 2)
        try:
            if not (self.ipdb_netns is None):
                for iface_name in self.ipdb_netns.interfaces:
                    if "vlan" in str(iface_name) or "veth" in str(iface_name):
                        self.ipdb_netns.interfaces[iface_name].remove().commit()
            netns.remove(self.nsp_name)
            self.ipdb_netns.release()
            Logger().debug("[+] Namespace(" + self.nsp_name + ") successfully deleted", 3)
        except Exception as e:
            if re.match("\[Errno 2\]*", str(e)):
                Logger().debug("[+] Namespace(" + self.nsp_name + ") is already deleted", 3)
                return
            Logger().debug("[-] Namespace(" + self.nsp_name +
                           ") couldn't be deleted. Try 'ip netns delete <namespace_name>'", 3)
            Logger().error(str(e), 3)

    def encapsulate_interface(self, iface_name: str):
        """
        Encapsulate the the given interface inside the Namespace.

        :param iface_name:
        """
        iface_ip = self._get_ip(True, iface_name)
        try:
            with self.ipdb.interfaces[iface_name] as iface:
                iface.net_ns_fd = self.nsp_name
            # the interface automatically switched the database and is now inside ipdb_netns_dictionary[vlan_iface_name]
            with self.ipdb_netns.interfaces[iface_name] as iface:
                iface.add_ip(iface_ip)  # '192.168.1.11/24'
                iface.up()
            Logger().debug("[+] Encapsulate Interface(" + iface_name + ")", 3)
        except Exception as e:
            Logger().debug("[-] Couldn't encapsulate the Interface(" + iface_name + ")", 3)
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
                iface_ip = self._get_ip(False, iface_name)
                Logger().debug("[+] New IP " + iface_ip + " for " + iface_name + " by dhcp", 2)
            except TimeoutError as e:
                Logger().debug("[-] Couldn't get a new IP for " + iface_name + " by dhcp", 2)
        else:
            iface_ip = new_ip+"/"+str(new_ip_mask)
            Logger().debug("[+] New IP " + iface_ip + " for " + iface_name, 2)
        return iface_ip

    def _wait_for_ip_assignment(self, iface_name: str):
        """
        Waits until the dhcp-client got an ip

        :param iface_name:
        """
        Logger().debug("Wait for ip assignment via dhcp for Interface(" + iface_name +
                       ") in Namespace(" + self.nsp_name + ")...", 3)
        current_ip = self._get_ip(False, iface_name).split('/')[0]
        if not self._get_ip(False, iface_name, not_this_ip=current_ip):
            os.system("ip netns exec " + self.nsp_name + " dhclient " + iface_name)
            i = 0
            while self._get_ip(False, iface_name, not_this_ip=current_ip) is None:
                time.sleep(0.5)
                i += 1
                if i == 20:
                    raise TimeoutError

    def _get_ip(self, ipdb: bool, iface_name: str, not_this_ip: str = None):
        """
        Reads the 'first' IP from the IPDB or if intended from IPDN_NETNS.

        :param ipdb: If True IPDB is used, else IPDB_NETNS is used
        :param iface_name:
        :param not_this_ip: If we know the first IP and are searching for another
        :return: the IP with the format ip/mask
        """
        if ipdb:
            iface = self.ipdb.interfaces[iface_name]
        else:
            iface = self.ipdb_netns.interfaces[iface_name]
        ipaddr_dictionary = iface.ipaddr
        for i in range(len(ipaddr_dictionary)):
            ip = ipaddr_dictionary[i]['address']
            mask = ipaddr_dictionary[i]['prefixlen']
            if re.match("((((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3})(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))", ip):
                if ip != not_this_ip:
                    return ip + "/" + str(mask)
        return ""
