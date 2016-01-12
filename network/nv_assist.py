from network.vlan import Vlan
from network.namespace import Namespace


class NVAssistent:
    """
    1. Creats VLANs
    2. Creats Namespaces and encapsulte a given VLAN
    """

    @staticmethod
    def create_vlan(link_iface_name: str, vlan_iface_name: str, vlan_iface_id: int,
                    vlan_iface_ip=None, vlan_iface_ip_mask=None):
        """
        Creats a VLAN.
        :param link_iface_name: name of the existing interface (eth0, wlan0, ...)
        :param vlan_iface_name: name of the vlan
        :param vlan_iface_id: the id of the vlan
        :param vlan_iface_ip: ip of the virtual interface
        :param vlan_iface_ip_mask: network-mask of the virtual interface
        :return: VLAN object
        """
        vlan = Vlan(link_iface_name, vlan_iface_name, vlan_iface_id, vlan_iface_ip, vlan_iface_ip_mask)
        vlan.create_interface()
        return vlan

    @staticmethod
    def create_namespace_vlan(namespace_name: str, vlan: Vlan):
        """
        Creats a Namespace and encapsulate the given VLAN inside.
        :param namespace_name: Namespace name
        :param vlan: vlan object
        :return: Namespace object
        """
        namespace = Namespace(namespace_name, vlan.ipdb)
        namespace.encapsulate_interface(vlan.vlan_iface_name)
        return namespace

    @staticmethod
    def create_namespace_vlan(namespace_name: str, link_iface_name: str, vlan_iface_name: str, vlan_iface_id: int,
                              vlan_iface_ip=None, vlan_iface_ip_mask=None):
        """
        Creats a Namespace and a VLAN. Encapsulate the VLAN inside the Namespace.
        :param namespace_name: Namespace name
        :param link_iface_name: name of the existing interface (eth0, wlan0, ...)
        :param vlan_iface_name: name of the vlan
        :param vlan_iface_id: the id of the vlan
        :param vlan_iface_ip: ip of the virtual interface
        :param vlan_iface_ip_mask: network-mask of the virtual interface
        :return: Namespace object
        """
        vlan = Vlan(link_iface_name, vlan_iface_name, vlan_iface_id, vlan_iface_ip, vlan_iface_ip_mask)
        vlan.create_interface()
        namespace = Namespace(namespace_name, vlan.ipdb)
        namespace.encapsulate_interface(vlan.vlan_iface_name)
        return namespace
