from network.vlan import Vlan
from network.namespace import Namespace
from pyroute2.ipdb import IPDB
from network.remote_system import RemoteSystem
from log.loggersetup import LoggerSetup
import logging


class NVAssistent:
    """
    The NVAssistent (NamespaceVlanAssistent) provides the following Features:
        1. Creates a IPDB: stores the Network-Interfaces
        2. Creates VLANs and Namespaces
        3. Encapsulates the VLANs inside the Namespaces
        4. Delete VLANs and Namespaces

    IPDB:   Is a transactional database, containing records, representing network stack objects.
            Any change in the database is not reflected immidiately in OS, but waits until commit() is called.

    If we want to use VLANs for Systems (with identical IPs) on the network, we need Namespaces. Each Namespace
    encapsulate one VLAN for the current process. The Namespace only contains the given VLAN and the 'lo'-interface.
    If we want to use a physical interface (like 'eth0') we have to create a bridge that connects the physical interface
    with Namespace by the 'veth'-interfaces.
    """""

    def __init__(self, link_iface_name: str):
        """
        :param link_iface_name: 'physical'-interface like 'eth0' to which the VLAN is connected to
        """
        self.ipdb = IPDB()
        self.link_iface_name = link_iface_name
        self.vlan_dict = dict()
        self.nsp_dict = dict()

    def create_namespace_vlan(self, remote_system: RemoteSystem):
        """
        Creats a Namespace and a VLAN. Encapsulate the VLAN inside the Namespace.

        :param remote_system: Router-Obj or Powerstrip-Obj with which we want to connect to.
        """
        if remote_system.namespace_name in self.nsp_dict.keys():
            logging.debug("%s[-] Namespace already exists", LoggerSetup.get_log_deep(2))
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

        :param namespace_name: Namespace_name
        :param vlan_iface_name: VLAN_name
        :return: IP address (ip/mask)
        """
        ip_address = self.nsp_dict[namespace_name].ipdb_get_ip(ipdb=False, iface_name=vlan_iface_name).split("/")
        ip = ip_address[0]
        mask = int(ip_address[1])
        return ip, mask

    def delete_vlan(self, vlan_iface_name: str):
        """
        Removes the given VLAN.

        :param vlan_iface_name: VLAN_name
        """
        self.vlan_dict[vlan_iface_name].delete_interface()

    def delete_namespace(self, namespace_name: str):
        """
        Removes the given Namespace.

        :param namespace_name: Namespace_name
        """
        self.nsp_dict[namespace_name].remove()

    def close(self):
        """
        Deletes all VLANs and Namespaces and releases the IPDB.
        """
        for vlan in self.vlan_dict:
            self.delete_vlan(vlan)
        for nsp in self.nsp_dict:
            self.delete_namespace(nsp)
        self.ipdb.release()
