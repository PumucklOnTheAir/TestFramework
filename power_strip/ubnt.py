from power_strip.power_strip import PowerStrip
import logging


class Ubnt(PowerStrip):
    """
    This class implements an API for the Ubiquiti mPower 6-Port mFi Power Strip
    running on Firmware version 2.1.11.
    Different ports can be turned on or off, each port corresponds to a Router.
    """""

    def __init__(self, sid: int, vlan_iface_name: str, vlan_iface_id: int, ip: str, ip_mask: int,
                 usr_name: str, usr_password: str, n_ports: int):
        """
        :param sid: ID of the object
        :param vlan_iface_name: Name of the VLAN Interface
        :param vlan_iface_id: ID of the VLAN Interface
        :param ip: IP of the power strip
        :param ip_mask: IP Mask of the power strip
        :param usr_name: Username to login via SSH
        :param usr_password: Password to login via SSH
        :param n_ports: Number of ports on the power strip
        """

        # Static IP of Ubiquiti mPower Pro (EU)
        self._ip = "192.168.1.20"
        self._ip = ip

        self._id = 1
        self._id = sid

        self._vlan_iface_id = 20
        self._vlan_iface_id = vlan_iface_id

        self._vlan_iface_name = "vlan20"
        self._vlan_iface_name = vlan_iface_name

        self._namespace_name = None
        self._namespace_name = "nsp" + str(self._vlan_iface_id)

        self._ip_mask = None
        self._ip_mask = ip_mask

        # Default Ubiquiti username
        self._usr_name = "ubnt"
        self._usr_name = usr_name

        # Default Ubiquiti password
        self._usr_password = "ubnt"
        self._usr_password = usr_password

        # Number of ports on power strip
        self._n_ports = 6
        self._n_ports = n_ports

    @property
    def ip(self) -> str:
        """
        IP of power strip.

        :return: IP number as string
        """
        return self._ip

    @property
    def id(self) -> int:
        """
        ID of power strip.

        :return: ID as int
        """
        return self._id

    @property
    def vlan_iface_id(self) -> int:
        """
        VLAN ID of power strip.

        :return:
        """
        return self._vlan_iface_id

    @property
    def vlan_iface_name(self) -> str:
        """
        Used VLAN name from server for this power strip.

        :return:
        """
        return self._vlan_iface_name

    @property
    def namespace_name(self) -> str:
        """
        Name of namespace.

        :return: namespace name
        """
        return self._namespace_name

    @property
    def ip_mask(self) -> int:
        """
        IP mask.

        :return: ip mask
        """
        return self._ip_mask

    @property
    def usr_name(self) -> str:
        """
        Username.

        :return: user name
        """
        return self._usr_name

    @property
    def usr_password(self) -> str:
        """
        User password.

        :return: user password
        """
        return self._usr_password

    @property
    def n_ports(self) -> int:
        """
        Number of Ports.

        :return: number of ports
        """
        return self._n_ports

    def __port_exists(self, port_id):
        if port_id == 0 or port_id > self.n_ports:
            logging.info("No such port")
            return False
        else:
            return True

    def port_status(self, port_id):
        """
        Checks if power on port is on or off.

        :param port_id: ID of power strip port
        :return: '1' for on or '0' for off, '2' for error
        """
        if self.__port_exists(port_id):
            cmd = "cat /dev/output" + str(port_id)
            return cmd

    def create_command(self, port_id: int, on_or_off: bool):
        """
        Switches the power on the given port.

        :param port_id: ID of port to be switched
        :param on_or_off: Switch power to: 'True' for on, 'False' for off
        """
        if self.__port_exists(port_id):
            on = 1 if on_or_off else 0
            cmd = "echo " + str(on) + " > /dev/output" + str(port_id)
            return cmd
