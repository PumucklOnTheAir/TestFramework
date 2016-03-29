from unittest import TestCase
from router.router import Router, Mode
from router.network_interface import NetworkInterface
from router.cpu_process import CPUProcess
from router.socket import InternetSocket
from router.memory import RAM, Flashdriver
from router.bat_originator import BatOriginator


class TestRouter(TestCase):
    def test_create_Router(self):
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)

        assert isinstance(router, Router)

        self.assertEqual(0, router.id)
        self.assertEqual("vlan21", router.vlan_iface_name)
        self.assertEqual(21, router.vlan_iface_id)
        self.assertEqual("nsp21", router.namespace_name)
        self.assertEqual("10.223.254.254", router._ip)
        self.assertEqual(16, router._ip_mask)
        self.assertEqual("192.168.1.1", router._config_ip)
        self.assertEqual(24, router._config_ip_mask)
        self.assertEqual("root", router.usr_name)
        self.assertEqual("root", router.usr_password)
        self.assertEqual(1, router.power_socket)

    def test_optional_getter_setter(self):
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)

        assert isinstance(router, Router)

        router.mode = Mode.configuration
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        router.node_name = "64293-testframework1"
        router.public_key = "1234567890abcdef16171819"

        network_interface = NetworkInterface(0, "eth0")
        assert isinstance(network_interface, NetworkInterface)
        router.network_interfaces[network_interface.name] = network_interface

        cpu_process = CPUProcess(11, "root", 1.1, 11.2, "echo")
        assert isinstance(cpu_process, CPUProcess)
        router.cpu_processes.append(cpu_process)

        socket = InternetSocket()
        assert isinstance(socket, InternetSocket)
        router.sockets.append(socket)

        ram = RAM(8000, 4000, 4000, 0, 0)
        assert isinstance(ram, RAM)
        router.ram = ram

        flash_driver = Flashdriver(8000, 2000, 6000)
        assert isinstance(flash_driver, Flashdriver)
        router.flashdriver = flash_driver

        router.uci["autoupdater.settings.enabled"] = "1"

        bat_originator = BatOriginator("00:00:00:00:00:00", 12.2, "01:00:01:00:01:00", "mesh0",
                                       ["01:00:01:00:01:00", "21:00:21:00:21:00", "03:00:03:00:03:00"])
        assert isinstance(bat_originator, BatOriginator)
        router.bat_originators.append(bat_originator)

        self.assertEqual(Mode.configuration, router.mode)
        self.assertEqual("TP-LINK TL-WR841N/ND v9", router.model)
        self.assertEqual("e8:de:27:b7:7c:e2", router.mac)
        self.assertEqual("64293-testframework1", router.node_name)
        self.assertEqual("1234567890abcdef16171819", router.public_key)
        self.assertEqual(network_interface, router.network_interfaces[network_interface.name])
        self.assertEqual(cpu_process, router.cpu_processes.pop())
        self.assertEqual(socket, router.sockets.pop())
        self.assertEqual(ram, router.ram)
        self.assertEqual(flash_driver, router.flashdriver)
        self.assertEqual('Firmware not known', router.firmware.name)
        self.assertEqual("1", router.uci["autoupdater.settings.enabled"])
        self.assertEqual(bat_originator, router.bat_originators.pop())
