from pyroute2.netns.nslink import NetNS
from pyroute2.ipdb import IPDB
from pyroute2 import netns
import re
import sys
import traceback
from log.logger import Logger


class Namespace:

    def __init__(self, nsp_name: str, ipdb: IPDB):
        """
        Creats a namespace for a specific vlan_iface

        :param nsp_name:
        :param ipdb: IPDB is a transactional database, containing records, representing network stack objects.
                    Any change in the database is not reflected immidiately in OS, but waits until commit() is called.
        """
        Logger().debug("Create Namespace ...", 2)
        self.nsp_name = nsp_name
        self.id = id
        self.vlan_iface_name = ""
        self.vlan_iface_ip = "0.0.0.0"
        self.ipdb = ipdb
        self.ipdb_netns = None
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
            netns.remove(self.nsp_name)
            if self.ipdb_netns is not None:
                self.ipdb_netns.interfaces[self.vlan_iface_name].nl.remove()
                self.ipdb_netns.release()
            Logger().debug("[+] Namespace(" + self.nsp_name + ") successfully deleted", 3)
        except Exception as e:
            if re.match("\[Errno 2\]*", str(e)):
                Logger().debug("[+] Namespace(" + self.nsp_name + ") is already deleted", 3)
                return
            Logger().debug("[-] Namespace(" + self.nsp_name +
                           ") couldn't be deleted. Try 'ip netns delete <namespace_name>'", 3)
            Logger().error(str(e), 3)

    def encapsulate_interface(self, vlan_iface_name: str):
        """
        Capture the assigned interface in a namespace.

        :param vlan_iface_name: name of the vlan interface
        """
        self.vlan_iface_name = vlan_iface_name
        self.vlan_iface_ip = self._get_ipv4_from_dictionary(self.ipdb.interfaces[self.vlan_iface_name])
        try:
            with self.ipdb.interfaces[self.vlan_iface_name] as vlan:
                vlan.net_ns_fd = self.nsp_name
            # the interface automatically switched the database and is now inside ipdb_netns_dictionary[vlan_iface_name]
            with self.ipdb_netns.interfaces[self.vlan_iface_name] as vlan:
                vlan.add_ip(self.vlan_iface_ip)  # '192.168.1.11/24'
                vlan.up()
            Logger().debug("[+] Encapsulate Interface(" + self.vlan_iface_name + ")", 3)
        except Exception as e:
            Logger().debug("[-] Couldn't encapsulate the Interface(" + self.vlan_iface_name + ")", 3)
            Logger().error(str(e), 3)

    def get_ip_of_encapsulate_interface(self) -> str:
        """
        :return: The IP(without ip_mask) of the interface encapsulated in this namespace
        """
        return self.vlan_iface_ip.split('/')[0]

    def _get_ipv4_from_dictionary(self, iface) -> str:
        """
        Gets the ip and network-mask from the ipdb

        :param iface: the interface from ipdb
        :return: ip with network-mask
        """
        ipaddr_dictionary = iface.ipaddr
        for i in range(len(ipaddr_dictionary)):
            ip = ipaddr_dictionary[i]['address']
            mask = ipaddr_dictionary[i]['prefixlen']
            if re.match('((((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3})(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))', ip):
                return ip + "/" + str(mask)
