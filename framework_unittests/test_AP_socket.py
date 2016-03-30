from unittest import TestCase
from router.socket import InternetSocket, Protocol, State
import ipaddress


class TestSocket(TestCase):

    def test_create_InternetSocket(self):
        socket = InternetSocket()
        socket.protocol = Protocol.tcp
        socket.local_address = "192.168.2.11"
        socket.local_port = "22"
        socket.foreign_address = "0.0.0.0"
        socket.foreign_port = "*"
        socket.state = State.listen
        socket.pid = 11
        socket.program_name = "/path/programm"

        assert isinstance(socket, InternetSocket)

        self.assertEqual(Protocol.tcp, socket.protocol)
        self.assertEqual(ipaddress.ip_address("192.168.2.11"), socket.local_address)
        self.assertEqual("22", socket.local_port)
        self.assertEqual(ipaddress.ip_address("0.0.0.0"), socket.foreign_address)
        self.assertEqual("*", socket.foreign_port)
        self.assertEqual(State.listen, socket.state)
        self.assertEqual(11, socket.pid)
        self.assertEqual("/path/programm", socket.program_name)
