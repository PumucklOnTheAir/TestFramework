from abc import abstractmethod
from network.remote_system import RemoteSystem


class PowerStrip(RemoteSystem):
    """
    This class provides the Interface for the basic functions to manage the power strip.
    """

    @abstractmethod
    def port_status(self, port_id) -> str:
        """
        returns the status of the requested port

        :param port_id: port to be checked
        :return: command to query port status
        """
        pass

    @abstractmethod
    def up(self, port_id: int) -> str:
        """
        generates the command to set the selected port to up, aka turn on the power

        :param port_id: port to be set
        :return: command as string
        """
        pass

    @abstractmethod
    def down(self, port_id: int) -> str:
        """
        generates the command to set the selected port to down, aka turn off power

        :param port_id: port to be set
        :return: command as string
        """
        pass
