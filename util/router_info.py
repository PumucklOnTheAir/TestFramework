from threading import Thread
from network.network_ctrl import NetworkCtrl
from router.router import Router
from log.logger import Logger
from router.network_interface import NetworkInterface, Status
from router.ip_address import IPv4, IPv6
from router.cpu_process import CPUProcess
from router.memory import RAM, Flashdriver
from typing import Dict, List


class RouterInfo(Thread):
    """
    The RouterInfo collects in a new Thread informations about the Routers
    """""

    def __init__(self, router: Router):
        Thread.__init__(self)
        self.router = router
        self.network_ctrl = NetworkCtrl(self.router, 'eth0')
        self.daemon = True

    def run(self):
        """
        Runs new thread and gets the information from the router via ssh

        :return:
        """
        Logger().info("Update the Infos of the Router(" + str(self.router.id) + ") ...", 1)
        self.network_ctrl.connect_with_remote_system()

        # Model
        self.router.model = self._get_router_model()
        # MAC
        self.router.mac = self._get_router_mac()
        # SSID
        self.router.ssid = self._get_router_ssid()
        # NetworkInterfaces
        self.router.interfaces = self._get_router_network_interfaces()
        # CPUProcesses
        self.router.cpu_processes = self._get_router_cpu_process()
        # RAM
        self.router.ram = self._get_router_mem_ram()
        # Flashdriver
        # TODO: self.router.flashdriver = self._get_router_mem_flashdriver()

    def join(self):
        self.network_ctrl.exit()
        Thread.join(self)

    def _get_router_model(self) -> str:
        """
        :return: the Model of the given Router object
        """
        return self.network_ctrl.send_command('cat /proc/cpuinfo | grep machine').split(":")[1][:-4]

    def _get_router_mac(self) -> str:
        """
        :return: the MAC of the given Router object
        """
        return self.network_ctrl.send_command('uci show network.client.macaddr').split('=')[1][:-4]

    def _get_router_ssid(self):
        """
        :return: the SSID of the given Router object
        """
        return self.network_ctrl.send_command('uci show wireless.client_radio0.ssid').split('=')[1][:-4]

    def _get_router_network_interfaces(self) -> Dict:
        """
        :return: the network interfaces of the given Router object
        """
        interfaces = dict()
        tmp_interfaces_names = self.network_ctrl.send_command("ip a | grep '^[0-9]*:*:'").split("\n")
        interface_names = list()

        # transform a line tmp:
        # '2: enp0s25: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000'
        # into 'enp0s25' and lists it.
        for tmp in tmp_interfaces_names:
            interface_names.append(tmp.split(":")[1].replace(" ", ""))

        for iface_name in interface_names:
            mac = self.network_ctrl.send_command("ip addr show enp0s25 | grep 'link/ether'").split(" ")[1]

            interface = NetworkInterface(iface_name, mac)

            # Status: UP | DOWN | UNKNOWN
            cmd = "ip addr show " + iface_name
            interface.status = self.network_ctrl.send_command(cmd).split("state")[1].split("group")[0].replace(" ", "")

            # IPv4 addresses
            inet_lst = self.network_ctrl.send_command("ip addr show " + iface_name + " | grep 'inet '")
            for inet in inet_lst:
                ip = inet.split("/")[0].split(" ")[1]
                ip_mask = int(inet.split("/")[1].split(" ")[0])
                interface.ipv4_lst.append(IPv4(ip, ip_mask))

            # IPv6 addresses
            inet_lst = self.network_ctrl.send_command("ip addr show " + iface_name + " | grep 'inet6 '")
            for inet in inet_lst:
                ip = inet.split("/")[0].split(" ")[1]
                ip_prefix_len = int(inet.split("/")[1].split(" ")[0])
                interface.ipv6_lst.append(IPv6(ip, ip_prefix_len))

            interfaces[iface_name] = interface
        return interfaces

    def _get_router_cpu_process(self) -> List:
        """
        :return: the cpu processes of the given Router object
        """
        cpu_processes = list()
        cpu_process_info = self.network_ctrl.send_command("ps aux")

        # A line looks like:
        # 'root     1731  7.0  8.2 1824844 661228 tty2   Sl+  09:50  18:01 firefox'
        for cpu_process_info_line in cpu_process_info[1:]:
            # Split and remove the spaces
            cpu_process_info_lst = cpu_process_info_line.split(" ")
            i = cpu_process_info_lst.count("")
            for i in range(0, i):
                cpu_process_info_lst.remove("")
            # Get the infos
            user = cpu_process_info_lst[0]
            pid = int(cpu_process_info_lst[1])
            cpu = float(cpu_process_info_lst[2])
            mem = float(cpu_process_info_lst[3])
            start = cpu_process_info_lst[8]
            command = ""
            for i in range(10, len(cpu_process_info_lst)):
                command += cpu_process_info_lst[i]
            cpu_process = CPUProcess(pid, user, cpu, mem, start, command)
            cpu_processes.append(cpu_process)
        return cpu_processes

    def _get_router_mem_ram(self) -> RAM:
        """
        :return: the RAM of the given Router.
        """
        ram = None
        ram_info = self.network_ctrl.send_command("free -m")
        for ram_info_line in ram_info[1:]:
            if "Mem" in ram_info:
                # Split and remove the spaces
                ram_info_lst = ram_info_line.split(" ")
                i = ram_info_lst.count("")
                for i in range(0, i):
                    ram_info_lst.remove("")
                # Get the infos
                total = int(ram_info_lst[1])
                used = int(ram_info_lst[2])
                free = int(ram_info_lst[3])
                shared = int(ram_info_lst[4])
                buffers = int(ram_info_lst[5])
                cached = int(ram_info_lst[6])
                ram = RAM(total, used, free, shared, buffers, cached)
        return ram

    def _get_router_mem_flashdriver(self) -> Flashdriver:
        """
        :return: the memory of an external Flashdriver(like usb SDcard) of the given Router.
        """
        falshdriver = None
        # TODO: '_get_router_mem_flashdriver' muss noch implementiert werden
