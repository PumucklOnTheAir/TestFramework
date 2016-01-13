from util.power_strip import PowerStrip
from log.logger import Logger
from network.network_ctrl import NetworkCtrl


class Ubnt(PowerStrip):
    """This class implements an API for the Ubiquiti mPower 6-Port mFi Power Strip
        running on Firmware version 2.1.11
        Different ports can be turned on or off, each port corresponds to a router
    """

    def __init__(self, vlan_iface_name: str, vlan_iface_id: int, ip: str, ip_mask: int,
                 usr_name: str, usr_password: str):

        # Static IP of Ubiquiti mPower 6
        self._ip = "192.168.1.20"
        self._ip = ip

        self._vlan_iface_id = None
        self._vlan_iface_id = vlan_iface_id

        self._vlan_iface_name = None
        self._vlan_iface_name = vlan_iface_name

        self._ip_mask = None
        self._ip_mask = ip_mask

        # Default Ubiquiti username
        self._usr_name = "ubnt"
        self._usr_name = usr_name

        # Default Ubiquiti password
        self._usr_password = "ubnt"
        self._usr_password = usr_password

    @property
    def ip(self) -> str:
        """
        IP number of the Router
        :return: IP number as string
        """
        return self._ip

    @property
    def vlan_iface_id(self) -> int:
        """
        The VLAN ID from router
        :return:
        """
        return self._vlan_iface_id

    @property
    def vlan_iface_name(self) -> str:
        """
        Used VLAN name from server for this router
        :return:
        """
        return self._vlan_iface_name

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
        Username
        :return:
        """
        return self._usr_password

    def connect(self):
        """
        Connects with the power strip via network controller
        """
        global network_ctrl
        network_ctrl = NetworkCtrl(self)
        network_ctrl.connect_with_remote_system()

    def __command(self, cmd):
        self.connect()
        output = network_ctrl.send_command(cmd)
        Logger().info("Command \'" + str(cmd) + "\' sent to power strip")
        network_ctrl.exit()
        return output

    def port_status(self, port_id):
        """
        Checks if power on port is on or off
        :param port_id: ID of power strip port
        :return: 1 for on or 0 for off
        """
        cmd = "cat /dev/output" + str(port_id)
        output = self.__command(cmd)
        return int(output)

    def up(self, port_id):
        """
        Turns on power on port
        :param port_id: ID of power strip port
        :return: bool for failure or success
        """
        cmd = "echo 1 > /dev/output" + str(port_id)
        self.__command(cmd)
        if self.port_status(port_id) == 1:
            Logger().info("Power turned on: port " + str(port_id))
            return True
        else:
            Logger().error("Could not turn on power on port " + str(port_id))
            return False

    def down(self, port_id):
        """
        Turns off power on port
        :param port_id: ID of power strip port
        :return: bool for failure or success
        """
        cmd = "echo 0 > /dev/output" + str(port_id)
        self.__command(cmd)
        if self.port_status(port_id) == 0:
            Logger().info("Power turned off: port " + str(port_id))
            return True
        else:
            Logger().error("Could not turn off power on port " + str(port_id))
            return False
