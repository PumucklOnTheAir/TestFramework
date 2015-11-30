from server.proxyobject import ProxyObject


class Router(ProxyObject):

    def __init__(self, vlan_name, vlan_id, ip, ip_mask):
        ProxyObject.__init__(self)

        self._ip = None
        self._ip = ip

        self._vlan_id = None
        self._vlan_id = vlan_id

        self._vlan_name = None
        self._vlan_name = vlan_name

        self._ip_mask = None
        self._ip_mask = ip_mask


    @property
    def ip(self) -> str:
        """
        IP number of the Router
        :return: IP number as string
        """
        return self._ip

    @property
    def vlan_id(self) -> int:
        """
        The VLAN ID from router
        :return:
        """
        return self._vlan_id

    @property
    def vlan_name(self) -> str:
        """
        Wozu ist ein VLAN Name gut?
        :return:
        """
        return self._vlan_id

    @property
    def ip_mask(self) -> int:
        """
        IP mask
        :return:
        """
        return self._ip_mask

    ## Optional information

