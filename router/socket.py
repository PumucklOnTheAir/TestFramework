from enum import Enum
import ipaddress


class Protocol(Enum):
    """
    Represent the protocol which is used by the Socket.
    """""
    tcp = 1
    udp = 2
    unix = 3


class State(Enum):
    """
    Represent the status of a Socket.
    """""
    listen = 1
    established = 2


class Socket:
    """
    This class represents a Socket of the Router, with the protocol, state, pid and
    the name of the program using the Socket.
    """""

    def __init__(self):
        """
        protocol can be tcp, udp or unix
        state can be listen or established
        pid is the process id of the program using the Socket
        program_name is the name of the program using the Socket
        """
        self._protocol = None
        self._state = None
        self._pid = None
        self._program_name = None

    @property
    def protocol(self) -> Protocol:
        """
        The Protocol of the socket. (like tcp, upd, unix)

        :rtype: Protocol
        :return:
        """
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        """
        :type value: Protocol or str
        """
        if isinstance(value, Protocol):
            self._protocol = value
        else:
            if value == "tcp":
                self._protocol = Protocol.tcp
            elif value == "udp":
                self._protocol = Protocol.udp
            elif value == "unix":
                self._protocol = Protocol.unix

    @property
    def state(self) -> State:
        """
        The State of the socket. (like listen, established)

        :rtype: State
        :return:
        """
        return self._state

    @state.setter
    def state(self, value):
        """
        :type value: State or str
        """
        if isinstance(value, State):
            self._state = value
        else:
            if value.lower() == "listen":
                self._state = State.listen
            elif value.lower() == "established":
                self._state = State.established

    @property
    def pid(self) -> int:
        """
        The process id of the program using the socket.

        :rtype: int
        :return:
        """
        return self._pid

    @pid.setter
    def pid(self, value: int):
        """
        :type value: int
        """
        assert isinstance(value, int)
        self._pid = value

    @property
    def program_name(self) -> str:
        """
        The name of the program that use the socket.

        :rtype: str
        :return:
        """
        return self._program_name

    @program_name.setter
    def program_name(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._program_name = value


class InternetSocket(Socket):

    def __init__(self):
        super().__init__()
        self._local_address = None
        self._local_port = None
        self._foreign_address = None
        self._foreign_port = None

    @property
    def local_address(self) -> ipaddress:
        """
        The local ip address.

        :rtype: ipaddress
        :return:
        """
        return self._local_address

    @local_address.setter
    def local_address(self, value):
        """
        :type value: ipaddress or str
        """
        self._local_address = ipaddress.ip_address(value)

    @property
    def local_port(self) -> str:
        """
        The local port of the socket.

        :rtype: str
        :return:
        """
        return self._local_port

    @local_port.setter
    def local_port(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._local_port = value

    @property
    def foreign_address(self) -> ipaddress:
        """
        The foreign ip address.

        :rtype: ipaddress
        :return:
        """
        return self._foreign_address

    @foreign_address.setter
    def foreign_address(self, value):
        """
        :type value: ipaddress or str
        """
        self._foreign_address = ipaddress.ip_address(value)

    @property
    def foreign_port(self) -> str:
        """
        The foreign port of the socket.

        :rtype: str
        :return:
        """
        return self._local_port

    @foreign_port.setter
    def foreign_port(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._foreign_port = value

    def __str__(self):
        return str(self.protocol) + " " + str(self.local_address) + ":" + self.local_port + " " + \
               str(self.foreign_address) + ":" + self.foreign_port + " " + str(self.state) + " " + \
               str(self.pid) + " " + \
               self.program_name
