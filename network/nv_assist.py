from network.vlan import Vlan
from network.namespace import Namespace


class NVAssistent:
    """
    1. Creats VLANs
    2. Creats Namespaces and encapsulte a given VLAN
    """

    def __init__(self):
        self._vlan = None
        self._namespace = None

    def create_vlan(self, link_iface_name: str, vlan_iface_name: str, vlan_iface_id: int,
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
        self.vlan = Vlan(link_iface_name, vlan_iface_name, vlan_iface_id, vlan_iface_ip, vlan_iface_ip_mask)
        self.vlan.create_interface()

    def create_namespace_vlan(self, namespace_name: str, link_iface_name: str, vlan_iface_name: str, vlan_iface_id: int,
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
        self.vlan = Vlan(link_iface_name, vlan_iface_name, vlan_iface_id, vlan_iface_ip, vlan_iface_ip_mask)
        self.vlan.create_interface()
        self.namespace = Namespace(namespace_name, self.vlan.ipdb)
        self.namespace.encapsulate_interface(self.vlan.vlan_iface_name)

    def delete_vlan(self):
        self.vlan.delete_interface()

    def delete_namespace(self):
        self.namespace.remove()

    @property
    def vlan(self) -> Vlan:
        """
        The VLAN of the RemoteSystem
        
        :return: Vlan
        """
        return self._vlan

    @vlan.setter
    def vlan(self, value: Vlan):
        """
        :type value: Vlan
        """
        assert isinstance(value, Vlan)
        self._vlan = value

    @property
    def namespace(self) -> Namespace:
        """
        The Namespace of the RemoteSystem
        
        :return: Vlan
        """
        return self._namespace

    @namespace.setter
    def namespace(self, value: Namespace):
        """
        :type value: Namespace
        """
        assert isinstance(value, Namespace)
        self._namespace = value
