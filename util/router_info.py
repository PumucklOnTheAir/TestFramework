from threading import Thread
from network.network_ctrl import NetworkCtrl
from network.remote_system import RemoteSystemJob
from router.router import Router
from log.logger import Logger
from router.network_interface import NetworkInterface, Status, WifiInformation
from router.cpu_process import CPUProcess
from router.memory import RAM
from router.socket import InternetSocket
from typing import Dict, List
import traceback
import sys


class RouterInfo(Thread):
    """
    This class gets the following information via SSH:
        1. RouterModel
        2. MAC-Address
        3. SSID
        4. NetworkInterfaces
        5. CPU-Processes-Information
        6. Memory-Information
        7. Sockets
    """""

    def __init__(self, router: Router):
        Thread.__init__(self)
        self.router = router
        self.network_ctrl = NetworkCtrl(self.router)
        self.daemon = True

    def run(self):
        """
        Runs new thread and gets the information from the Router via ssh
        """
        Logger().info("Update the Infos of the Router(" + str(self.router.id) + ") ...", 1)
        try:
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
            # Sockets
            self.router.sockets = self._get_router_sockets()
            Logger().debug("[+] Infos updated", 2)
        except Exception as e:
            Logger().warning("[-] Couldn't update all Infos", 2)
            Logger().error(str(e))
            for tb in traceback.format_tb(sys.exc_info()[2]):
                Logger().error(tb, 3)
        finally:
            self.network_ctrl.exit()

    def _get_router_model(self) -> str:
        """
        :return: the Model of the given Router object
        """
        return self.network_ctrl.send_command('cat /proc/cpuinfo | grep machine')[0].split(":")[1][1:-1]

    def _get_router_mac(self) -> str:
        """
        :return: the MAC of the given Router object
        """
        return self.network_ctrl.send_command('uci show network.client.macaddr')[0].split('=')[1][:-1]

    def _get_router_ssid(self):
        """
        :return: the SSID of the given Router object
        """
        return self.network_ctrl.send_command('uci show wireless.client_radio0.ssid')[0].split('=')[1][:-1]

    def _get_router_network_interfaces(self) -> Dict:
        """
        :return: the network interfaces of the given Router object
        """
        interfaces = dict()
        # Get all network interfaces
        raw_iface_lst = self.network_ctrl.send_command("ip a | grep '^[0-9]*:*:'")
        iface_names_lst = list()
        iface_id_lst = list()

        # Get only the wifi interfaces
        raw_wifi_inface_name_lst = self.network_ctrl.send_command("iw dev | grep Interface")
        wifi_iface_name_lst = list()
        for raw_wifi_iface_name in raw_wifi_inface_name_lst:
            wifi_iface_name_lst.append(raw_wifi_iface_name.split("Interface ")[1].replace("\n", ""))

        # transform a line tmp:
        # '2: enp0s25: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000'
        # into '2'; 'enp0s25' and lists it.
        for raw_iface in raw_iface_lst:
            # Iface Id
            iface_id = int(raw_iface.split(":")[0])
            if iface_id_lst.count(iface_id) == 0:
                iface_id_lst.append(iface_id)

            # Iface Name
            iface_name = raw_iface.split(":")[1].replace(" ", "")
            if "@" in iface_name:
                iface_name = iface_name.split("@")[0]
            if iface_names_lst.count(iface_name) == 0:
                iface_names_lst.append(iface_name)

        # Take the information of the interfaces separately
        for i, iface_id in enumerate(iface_id_lst):
            iface_name = iface_names_lst[i]
            interface = NetworkInterface(iface_id, iface_name)
            raw_iface_info_lst = self.network_ctrl.send_command("ip addr show " + iface_name)
            for raw_iface_info in raw_iface_info_lst:
                # Status
                raw_status = raw_iface_info.split("state")
                if len(raw_status) > 1:
                    status = raw_status[1].split(" ")[1]
                    # Status: UP | DOWN | UNKNOWN
                    if status == "UP":
                        interface.status = Status.up
                    elif status == "DOWN":
                        interface.status = Status.down
                    else:
                        interface.status = Status.unknown

                # MAC
                raw_mac = raw_iface_info.split("link/ether")
                if len(raw_mac) > 1:
                    raw_mac = raw_mac[1].split()
                    interface.mac = raw_mac[0]

                # IP Address
                raw_ip = raw_iface_info.split("inet")
                if len(raw_ip) > 1:
                    raw_ip = raw_ip[1].split(" ")[1].split("/")
                    interface.add_ip_address(raw_ip[0], int(raw_ip[1]))

                # Wifi information
                if wifi_iface_name_lst.count(iface_name) != 0:
                    interface.wifi_information = self.__get_wifi_information(iface_name)
            interfaces[iface_name] = interface
        return interfaces

    def __get_wifi_information(self, iface_name: str) -> WifiInformation:
        """
        If the given interface name belongs to an wifi interface, there are some more infomations.

        :param iface_name: Name of the network interface
        :return: WifiInformation
        """
        wifi_information = WifiInformation()
        raw_wifi_info_lst = self.network_ctrl.send_command("iw dev")
        right_iface = False

        for raw_wifi_info in raw_wifi_info_lst:
            raw_wifi_info = raw_wifi_info.replace("\n", "")
            if "Interface" in raw_wifi_info:
                right_iface = True if iface_name in raw_wifi_info else False
            elif right_iface:
                if "wdev" in raw_wifi_info:
                    wifi_information.wdev = raw_wifi_info.split(" ")[1]
                elif "ssid" in raw_wifi_info:
                    wifi_information.ssid = raw_wifi_info.split(" ")[1]
                elif "type" in raw_wifi_info:
                    wifi_information.type = raw_wifi_info.split(" ")[1]
                elif "channel" in raw_wifi_info:
                    wifi_information.channel = int(raw_wifi_info.split(" ")[1])
                    wifi_information.channel_width = int(raw_wifi_info.split(" ")[5])
                    wifi_information.channel_center1 = int(raw_wifi_info.split(" ")[8])
        return wifi_information

    def _get_router_cpu_process(self) -> List:
        """
        :return: The cpu processes of the given Router object
        """
        cpu_processes = list()
        raw_cpu_process_lst = self.network_ctrl.send_command("top -n 1")
        # A line looks like:
        # 1051  1020 root     R     1388   5%   9% firefox
        for cpu_process_info_line in raw_cpu_process_lst[4:]:
            cpu_process_info_lst = cpu_process_info_line.split()

            if len(cpu_process_info_lst) > 7:
                # Get the infos
                pid = int(cpu_process_info_lst[0])
                user = cpu_process_info_lst[2]
                mem = float(cpu_process_info_lst[5].replace("%", ""))
                cpu = float(cpu_process_info_lst[6].replace("%", ""))
                command = ""
                for i in range(7, len(cpu_process_info_lst)):
                    command += cpu_process_info_lst[i]
                cpu_process = CPUProcess(pid, user, mem, cpu, command)
                cpu_processes.append(cpu_process)
        return cpu_processes

    def _get_router_mem_ram(self) -> RAM:
        """
        :return: The RAM of the given Router.
        """
        ram = None
        raw_mem_lst = self.network_ctrl.send_command("free -m")[1:]
        for ram_info_line in raw_mem_lst:
            if "Mem" in ram_info_line:
                # Split and remove the spaces
                ram_info_lst = ram_info_line.split()
                # Get the infos
                total = int(ram_info_lst[1])
                used = int(ram_info_lst[2])
                free = int(ram_info_lst[3])
                shared = int(ram_info_lst[4])
                buffers = int(ram_info_lst[5])
                ram = RAM(total, used, free, shared, buffers)
        return ram

    def _get_router_sockets(self) -> List:
        """
        :return: The Sockets of the Router.
        """
        socket_lst = list()
        raw_socket_lst = self.network_ctrl.send_command("netstat -taupn")[2:]
        for raw_socket in raw_socket_lst:
            # raw_socket looks like:
            # tcp        0     32 192.168.1.1:22          192.168.1.239:51891     ESTABLISHED 1067/dropbear
            raw_socket = raw_socket.split()
            socket = InternetSocket()
            socket.protocol = raw_socket[0]
            raw_local_address = raw_socket[3].split(":")
            socket.local_address = raw_local_address[0] if len(raw_local_address) == 2 else "::"
            socket.local_port = raw_local_address[-1]
            raw_foreign_address = raw_socket[4].split(":")
            socket.foreign_address = raw_foreign_address[0] if len(raw_foreign_address) == 2 else "::"
            socket.foreign_port = raw_foreign_address[-1]
            raw_process = "-1/error"
            if raw_socket[0] == "tcp":
                socket.state = raw_socket[5]
                raw_process = raw_socket[6].split("/")
            elif raw_socket[0] == "udp":
                raw_process = raw_socket[5].split("/")
            socket.pid = int(raw_process[0])
            socket.program_name = raw_process[1]
            socket_lst.append(socket)
        return socket_lst


class RouterInfoJob(RemoteSystemJob):
    """
    Encapsulate RouterInfo as a job for the Server
    """""
    def run(self):
        router = self.remote_system
        router_info = RouterInfo(router)
        router_info.start()
        router_info.join()
        return {'router': router}

    def pre_process(self, server) -> {}:
        return None

    def post_process(self, data: {}, server) -> None:
        """
        Updates the router in the Server with the new information

        :param data: result from run()
        :param server: the Server
        :return:
        """
        ref_router = server.get_router_by_id(data['router'].id)
        ref_router.update(data['router'])  # Don't forget to update this method
