from network.vlan import Vlan
from network.namespace import Namespace
from pyroute2.ipdb import IPDB
from network.remote_system import RemoteSystem
from log.logger import Logger
import os


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
        self.ipdb = IPDB()
        self.link_iface_name = link_iface_name
        self.vlan_dict = dict()
        self.veth_dict = dict()
        self.nsp_dict = dict()

    def create_namespace_vlan(self, remote_system: RemoteSystem):
        """
        Creats a Namespace and a VLAN. Encapsulate the VLAN inside the Namespace.

        :param remote_system: Router or powerstrip
        """
        if remote_system.namespace_name in self.nsp_dict.keys():
            Logger().debug("[-] Namespace already exists", 2)
            return

        vlan = Vlan(self.ipdb, remote_system, self.link_iface_name)
        vlan.create_interface()
        self.vlan_dict[vlan.vlan_iface_name] = vlan

        namespace = Namespace(self.ipdb, str(remote_system.namespace_name))
        namespace.encapsulate_interface(vlan.vlan_iface_name)
        self.nsp_dict[namespace.nsp_name] = namespace

    def get_ip_address(self, namespace_name: str, vlan_iface_name: str) -> (str, int):
        """
        Returns the the first IP of the VLAN in the IPDB of the Namespace

        :param namespace_name: Namespace name
        :param vlan_iface_name: VLAN name
        :return: IP address (ip, mask)
        """
        ip_address = self.nsp_dict[namespace_name].ipdb_get_ip(ipdb=False, iface_name=vlan_iface_name).split("/")
        ip = ip_address[0]
        mask = int(ip_address[1])
        return ip, mask

    def delete_vlan(self, vlan_iface_name: str):
        self.vlan_dict[vlan_iface_name].delete_interface()

    def delete_veth(self, veth_iface_name: str):
        self.veth_dict[veth_iface_name].delete_interface()

    def delete_namespace(self, nsp_name: str):
        self.nsp_dict[nsp_name].remove()

    def close(self):
        """
        Deletes all VLANs, 'veth'-interfaces and Namespaces
        """
        for vlan in self.vlan_dict:
            self.delete_vlan(vlan)
        for veth in self.veth_dict:
            self.delete_veth(veth)
        for nsp in self.nsp_dict:
            self.delete_namespace(nsp)
        self.ipdb.release()
        Logger().debug("Kill dhclient ...", 2)
        os.system('pkill dhclient')
