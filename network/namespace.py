from pyroute2.netns.nslink import NetNS
from pyroute2.ipdb import IPDB
from pyroute2 import netns
import re, sys
import traceback
from log.logger import Logger

class Namespace:
    def __init__(self, nsp_name: str, vlan_iface_name: str, ipdb: IPDB):
        """
        Creats a namespace for a specific vlan_iface
        :param nsp_name:
        :param vlan_iface_name:
        :param ipdb:
        :return:
        """
        Logger().debug("Create Namespace ...", 1)
        self.nsp_name = nsp_name
        self.id = id
        self.vlan_iface_name = vlan_iface_name
        self.ipdb = ipdb
        self.ipdb_netns = None
        try:
            self.ipdb_netns = IPDB(nl=NetNS(nsp_name))
            netns.setns(nsp_name)
            Logger().debug("[+] Namespace(" + nsp_name + ") successfully created", 2)
            self.encapsulate_interface()
        except Exception as e:
            Logger().debug("[-] Couldn't create Namespace(" + nsp_name + ") or encapsulate interface", 2)
            for tb in traceback.format_tb(sys.exc_info()[2]):
                Logger().error(tb, 2)
            Logger().error(str(e), 2)
            self.remove()

    def remove(self):
        """
        : Desc : removes the virtual namespace and interface
        :return:
        """
        Logger().debug("Delete Namespace ...", 1)
        try:
            if self.ipdb_netns is None:
                netns.remove(self.nsp_name)
            else:
                self.ipdb_netns.interfaces[self.vlan_iface_name].nl.remove()
                self.ipdb_netns.release()
            Logger().debug("[+] namespace(" + self.nsp_name + ") successfully deleted", 2)
        except Exception as e:
            if re.match("\[Errno 2\]*",str(e)):
                Logger().debug("[+] namespace(" + self.nsp_name + ") is already deleted", 2)
                return
            Logger().debug("[-] namespace(" + self.nsp_name + ") couldn't be deleted. Try 'ip netns delete <namespace_name>'", 2)
            Logger().error("        "+str(e))

    def encapsulate_interface(self):
        """
        :Desc : capture the assigned interface in a namespace
        """
        vlan_ip = self.get_ipv4_from_dictionary(self.ipdb.interfaces[self.vlan_iface_name])
        with self.ipdb.interfaces[self.vlan_iface_name] as vlan:
            vlan.net_ns_fd = self.nsp_name
        # the interface automatically switched the database and is now inside ipdb_netns_dictionary[vlan_iface_name]
        with self.ipdb_netns.interfaces[self.vlan_iface_name] as vlan:
            vlan.add_ip(vlan_ip)  # '192.168.1.11/24'
            vlan.up()
        Logger().debug("[+] Encapsulate Interface(" + self.vlan_iface_name + ")", 2)

    def get_ipv4_from_dictionary(self, iface):
        """
        : Desc : gets the ip and network-mask from the ipdb
        :param iface: the interface from ipdb
        :return: ip with network-mask
        """
        ipaddr_dictionary = iface.ipaddr
        for i in range(len(ipaddr_dictionary)):
            ip = ipaddr_dictionary[i]['address']
            mask = ipaddr_dictionary[i]['prefixlen']
            if re.match("((((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3})(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))", ip):
                return ip+"/"+str(mask)
