from abc import abstractmethod
from network.remote_system import RemoteSystem


class PowerStrip(RemoteSystem):
    """
    This class provides the Interface for the basic functions to manage the power strip.
    """""

    @abstractmethod
    def port_status(self, port_id) -> str:
        """
        Returns the status of the requested port.

        :param port_id: port to be checked
        :return: Command to query port status
        """
        pass

    @abstractmethod
    def create_command(self, port_id: int, on_or_off: bool) -> str:
        """
        Generates the command to set the selected port to up or down.

        :param port_id: Port to be set
        :param on_or_off: Turn on or off
        :return: Command as string to set power on port
        """
        pass
