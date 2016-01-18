from abc import abstractmethod
from network.remote_system import RemoteSystem


class PowerStrip(metaclass=RemoteSystem):
    """
    This class provides the Interface for the basic functions to manage the power strip.
    """

    @abstractmethod
    def connect(self):
        """
        connect to the power strip
        """
        pass

    @abstractmethod
    def port_status(self, port_id) -> int:
        """
        returns the status of the requested port

        :param port_id: port to be checked
        :return: 0 or 1 for off or on
        """
        pass

    @abstractmethod
    def up(self, port_id) -> bool:
        """
        sets the selected port to up, aka turn on the power

        :param port_id: port to be set
        :return: bool for failure or success
        """
        pass

    @abstractmethod
    def down(self, port_id) -> bool:
        """
        sets the selected port to down, aka turn off power

        :param port_id: port to be set
        :return: bool for failure or success
        """
        pass
