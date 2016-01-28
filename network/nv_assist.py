from network.vlan import Vlan
from network.veth import Veth
from network.namespace import Namespace
from network.bridge import Bridge
from pyroute2.ipdb import IPDB
from server.router import Router
from log.logger import Logger
import os
from os import getpid


class NVAssistent:
    """
    1. Creates a IPDB: stores interfaces
    2. Creates a Bridge: connects multiple interfaces via a virtual switch
    3. Creates VLANs
    4. Creates Veths: connects a Namespace with the Bridge
    5. Creates Namespaces: encapsulte a given Interface

    If we want to use VLANs for Systems (with identical IPs) on the network, we need Namespaces. Each Namespace
    encapsulate one VLAN for the current process. The Namespace only contains the given VLAN and the 'lo'-interface.
    If we want to use a physical interface (like 'eth0') we have to create a bridge that connects the physical interface
    with Namespace by the 'veth'-interfaces.
    """""

    def __init__(self, link_iface_name: str):
        """
        Initialize the IPDB for the interfaces and creates a Bridge (virtual switch).

        :param link_iface_name: 'physical'-interface like 'eth0'
        """
        print("nvassi: " + str(getpid()))
        self.ipdb = IPDB()
        self.link_iface_name = link_iface_name
        #self.bridge = Bridge(self.ipdb, 'br0', self.link_iface_name)
        self.vlan_dict = dict()
        self.veth_dict = dict()
        self.namespace = None

    def create_namespace_vlan(self, namespace_name: str, link_iface_name: str, vlan_iface_name: str, vlan_iface_id: int):
        """
        Creats a Namespace and a VLAN. Encapsulate the VLAN inside the Namespace.
        
        :param namespace_name: Namespace name
        :param link_iface_name: name of the existing interface (eth0, wlan0, ...)
        :param vlan_iface_name: name of the vlan
        :param vlan_iface_id: the id of the vlan
        """
        vlan = Vlan(self.ipdb, link_iface_name, vlan_iface_name, vlan_iface_id)
        vlan.create_interface()
        self.vlan_dict[vlan.vlan_iface_name] = vlan

        namespace = Namespace(self.ipdb, namespace_name)
        namespace.encapsulate_interface(vlan.vlan_iface_name)
        self.namespace = namespace

    def create_namespace_vlan_veth(self, router: Router):
        """
        Creates a Namespace and a VLAN with the id given by the Router. Also creates a 'veth'-interface to connect
        the 'physical'-interface with the Namespace.

        :param router: Router object
        """
        vlan = Vlan(self.ipdb, self.link_iface_name, router.vlan_iface_name, router.vlan_iface_id)
        vlan.create_interface()
        self.vlan_dict[vlan.vlan_iface_name] = vlan

        veth = Veth(self.ipdb, 'veth'+str(router.id)+str(router.id), 'veth'+str(router.id),
                    '192.168.3.'+str(10+router.id), 24, '192.168.3.'+str(110+router.id), 24)
        veth.create_interface()
        self.veth_dict[veth.veth_iface_name1] = veth

        self.bridge = Bridge(self.ipdb, 'br'+str(router.id), self.link_iface_name)
        self.bridge.add_iface(veth.veth_iface_name1)

        namespace = Namespace(self.ipdb, router.namespace_name)
        namespace.encapsulate_interface(vlan.vlan_iface_name)
        namespace.encapsulate_interface(veth.veth_iface_name2)
        namespace.set_new_ip(dhcp=True, iface_name=veth.veth_iface_name2)
        self.namespace = namespace

    def delete_vlan(self, vlan_iface_name: str):
        self.vlan_dict[vlan_iface_name].delete_interface()

    def delete_veth(self, veth_iface_name: str):
        self.veth_dict[veth_iface_name].delete_interface()

    def delete_namespace(self, nsp_name: str):
        self.namespace.remove()

    def close(self):
        """
        Deletes all VLANs, 'veth'-interfaces and Namespaces
        """
        for vlan in self.vlan_dict:
            self.delete_vlan(vlan)
        for veth in self.veth_dict:
            self.delete_veth(veth)
        self.namespace.remove()
        #self.bridge.close()
        self.ipdb.release()
        Logger().debug("Kill dhclient ...")
        os.system('pkill dhclient')
