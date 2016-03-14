from power_strip.power_strip import PowerStrip
import logging


class Ubnt(PowerStrip):
    """This class implements an API for the Ubiquiti mPower 6-Port mFi Power Strip
        running on Firmware version 2.1.11
        Different ports can be turned on or off, each port corresponds to a router
    """

    def __init__(self, sid: int, vlan_iface_name: str, vlan_iface_id: int, ip: str, ip_mask: int,
                 usr_name: str, usr_password: str, n_ports: int):

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
        IP of power strip

        :return: IP number as string
        """
        return self._ip

    @property
    def id(self) -> int:
        """
        ID of power strip
        :return: ID as int
        """
        return self._id

    @property
    def vlan_iface_id(self) -> int:
        """
        VLAN ID of power strip

        :return:
        """
        return self._vlan_iface_id

    @property
    def vlan_iface_name(self) -> str:
        """
        Used VLAN name from server for this power strip

        :return:
        """
        return self._vlan_iface_name

    @property
    def namespace_name(self) -> str:
        """
        Name of namespace

        :return:
        """
        return self._namespace_name

    @property
    def ip_mask(self) -> int:
        """
        IP mask

        :return:
        """
        return self._ip_mask

    @property
    def usr_name(self) -> str:
        """
        Username

        :return:
        """
        return self._usr_name

    @property
    def usr_password(self) -> str:
        """
        User password

        :return:
        """
        return self._usr_password

    @property
    def n_ports(self) -> int:
        """
        Number of Ports

        :return:
        """
        return self._n_ports

    def __port_exists(self, port_id):
        if port_id == 0 or port_id > self.n_ports:
            Logger().info("No such port")
            return False
        else:
            return True

    def port_status(self, port_id):
        """
        Checks if power on port is on or off

        :param port_id: ID of power strip port
        :return: 1 for on or 0 for off, 2 for error
        """
        if self.__port_exists(port_id):
            cmd = "cat /dev/output" + str(port_id)
            return cmd

    def up(self, port_id):
        """
        Turns on power on port

        :param port_id: ID of power strip port
        :param switch_all: flag to turn on all ports
        :return: bool for failure or success
        """
        if self.__port_exists(port_id):
            self.switch(port_id,  1)
            return True
        else:
            return False

    def down(self, port_id):
        """
        Turns off power on port

        :param port_id: ID of power strip port
        :param switch_all: flag to turn off all ports
        :return: bool for failure or success
        """

        if self.__port_exists(port_id):
            self.switch(port_id, 0)
            return True
        else:
            return False

    def switch(self, port_id, on_or_off):
        """
        Switches the power on the given port

        :param port_id: ID of port to be switched
        :param switch_all: flag to switch the whole strip
        :param on_or_off: switch power to: 1 for on, 0 for off
        """
        assert on_or_off == 0 or on_or_off == 1
        cmd = "echo " + str(on_or_off) + " > /dev/output" + str(port_id)

        return cmd
