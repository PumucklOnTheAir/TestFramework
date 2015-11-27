from subprocess import Popen, PIPE, STDOUT
from pyroute2.netns.nslink import NetNS
from pyroute2.netns.process.proxy import NSPopen
from pyroute2.ipdb import IPDB
from pyroute2 import netns
import sys, time
import re
import socket, struct, fcntl

class Namespace:
    def __init__(self, nsp_name, vlan_iface_name, ipdb):
        self.nsp_name = nsp_name
        self.id = id
        self.vlan_iface_name = vlan_iface_name
        self.ipdb = ipdb
        self.ipdb_netns = IPDB(nl=NetNS(nsp_name))
        netns.setns(nsp_name)
        self.encapsulate_interface()

    def delete_interface(self):
        '''
        : Desc : removes the virtual interface
        '''
        try:
            self.ipdb_netns.interfaces[self.vlan_iface_name].nl.remove()
            print("[+] " + self.vlan_iface_name + " successfully deleted")
        except Exception as e:
            print("[-] " + self.vlan_iface_name + " couldn't be deleted")
            print("  " + str(e))
        self.ipdb_netns.release()

    def encapsulate_interface(self):
        '''
        :Desc : capture the assigned interface in a namespace
        :param vlan_iface_name: name of the interface
        '''
        print("encapsulate interface " + self.vlan_iface_name + " in namespace ...")
        vlan_ip = self.get_ipv4_from_dictionary(self.ipdb.interfaces[self.vlan_iface_name])
        with self.ipdb.interfaces[self.vlan_iface_name] as vlan:
            vlan.net_ns_fd = self.nsp_name
        #the interface automatically switched the database and is now inside ipdb_netns_dictionary[vlan_iface_name]
        with self.ipdb_netns.interfaces[self.vlan_iface_name] as vlan:
            vlan.add_ip(vlan_ip) #'192.168.1.11/24'
            vlan.up()
        print("netns: " + str(netns.listnetns()))

    def get_ipv4_from_dictionary(self, iface):
        '''
        : Desc : gets the ip and network-mask from the ipdb
        :param iface: the interface from ipdb
        :return: ip with network-mask
        '''
        ipaddr_dictionary = iface.ipaddr
        for i in range(len(ipaddr_dictionary)):
            ip = ipaddr_dictionary[i]['address']
            mask = ipaddr_dictionary[i]['prefixlen']
            if re.match("((((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3})(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))", ip):
                return (ip+"/"+str(mask))
        return None