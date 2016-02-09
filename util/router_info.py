from threading import Thread
from network.network_ctrl import NetworkCtrl
from network.remote_system import RemoteSystemJob
from router.router import Router
from log.logger import Logger
from router.network_interface import NetworkInterface, Status
from router.cpu_process import CPUProcess
from router.memory import RAM
from typing import Dict, List
import traceback, sys


class RouterInfo(Thread):
    """
    This class gets the following information via SSH:
        1. RouterModel
        2. MAC-Address
        3. SSID
        4. NetworkInterfaces
        5. CPU-Processes-Information
        6. Memory-Information
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
            #TODO self.router.model = self._get_router_model()
            # MAC
            #self.router.mac = self._get_router_mac()
            # SSID
            #self.router.ssid = self._get_router_ssid()
            # NetworkInterfaces
            self.router.interfaces = self._get_router_network_interfaces()
            # CPUProcesses
            #self.router.cpu_processes = self._get_router_cpu_process()
            # RAM
            #self.router.ram = self._get_router_mem_ram()
            Logger().debug("[+] Infos updated", 2)
        except Exception as e:
            Logger().warning("[-] Couldn't update all Infos", 2)
            Logger().error(str(e))
            for tb in traceback.format_tb(sys.exc_info()[2]):
                Logger().error(tb, 3)

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
        raw_iface_lst = self.network_ctrl.send_command("ip a | grep '^[0-9]*:*:'")
        raw_iface_lst = raw_iface_lst.replace("[", "").replace("]", "").split("\\n'")[0:-1]
        iface_names = list()
        iface_id_lst = list()

        # transform a line tmp:
        # '2: enp0s25: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000'
        # into '2'; 'enp0s25' and lists it.
        for raw_iface in raw_iface_lst:
            # Iface Id
            iface_id = int(raw_iface.split(":")[0].split("'")[1])
            if iface_names.count(iface_id) == 0:
                iface_id_lst.append(iface_id)

            # Iface Name
            iface_name = raw_iface.split(":")[1].replace(" ", "")
            if "@" in iface_name:
                iface_name = iface_name.split("@")[0]
            if iface_names.count(iface_name) == 0:
                iface_names.append(iface_name)

        # Take the information of the interfaces separately
        for i, iface_id in enumerate(iface_id_lst):
            iface_name = iface_names[i]
            interface = NetworkInterface(iface_id, iface_name)

            # MAC
            raw_iface_infos = self.network_ctrl.send_command("ip addr show " + iface_name + " | grep 'link/ether'")
            raw_iface_infos = raw_iface_infos.replace("[", "").replace("]", "").replace("'", "")
            if len(raw_iface_infos) > 0:
                raw_mac = raw_iface_infos.split(" ")
                i = raw_mac.count("")
                for i in range(0, i):
                    raw_mac.remove("")
                interface.mac = raw_mac[1]

            # Status
            raw_iface_infos = self.network_ctrl.send_command("ip addr show " + iface_name + " | grep " + iface_name)
            raw_iface_infos = raw_iface_infos.replace("[", "").replace("]", "").replace("'", "")
            raw_status = raw_iface_infos.split("state")
            if len(raw_status) > 1:
                status = raw_status[1].split(" ")[1]
                # Status: UP | DOWN | UNKNOWN
                if status == "UP":
                    interface.status = Status.up
                elif status == "DOWN":
                    interface.status = Status.down
                else:
                    interface.status = Status.unknown

            # IPv4 addresses
            raw_iface_infos = self.network_ctrl.send_command("ip addr show " + iface_name + " | grep 'inet '")
            raw_iface_infos = raw_iface_infos.replace("[", "").replace("]", "").replace("'", "")
            if len(raw_iface_infos) > 0:
                inet_lst = raw_iface_infos.split("\\n")
                for inet in inet_lst:
                    if not ("inet" in inet):
                        continue
                    ip = inet.split("/")[0].split("inet ")[1]
                    ip_mask = int(inet.split("/")[1].split(" ")[0])
                    interface.add_ip_address(ip, ip_mask)

            # IPv6 addresses
            raw_iface_infos = self.network_ctrl.send_command("ip addr show " + iface_name + " | grep 'inet6 '")
            raw_iface_infos = raw_iface_infos.replace("[", "").replace("]", "").replace("'", "")
            if len(raw_iface_infos) > 0:
                inet_lst = raw_iface_infos.split("\\n")
                for inet in inet_lst:
                    if not ("inet6" in inet):
                        continue
                    ip = inet.split("/")[0].split("inet6 ")[1]
                    ip_prefix_len = int(inet.split("/")[1].split(" ")[0])
                    interface.add_ip_address(ip, ip_prefix_len)
            interfaces[iface_name] = interface
        return interfaces

    def _get_router_cpu_process(self) -> List:
        """
        :return: the cpu processes of the given Router object
        """
        cpu_processes = list()
        raw_cpu_process_info = self.network_ctrl.send_command("top -n 1")
        raw_cpu_process_info = raw_cpu_process_info.replace("[", "").replace("]", "").replace("'", "")
        raw_cpu_process_info = raw_cpu_process_info.replace(",", "").replace("%", "")
        raw_cpu_process_info = raw_cpu_process_info.split("\\n")
        # A line looks like:
        # 1051  1020 root     R     1388   5%   9% firefox
        for cpu_process_info_line in raw_cpu_process_info[4:]:

            # Split and remove the spaces
            cpu_process_info_lst = cpu_process_info_line.split(" ")
            i = cpu_process_info_lst.count("")
            for i in range(0, i):
                cpu_process_info_lst.remove("")

            if len(cpu_process_info_lst) > 7:
                # Get the infos
                pid = int(cpu_process_info_lst[0])
                user = cpu_process_info_lst[2]
                mem = float(cpu_process_info_lst[5])
                cpu = float(cpu_process_info_lst[6])
                command = ""
                for i in range(7, len(cpu_process_info_lst)):
                    command += cpu_process_info_lst[i]
                cpu_process = CPUProcess(pid, user, mem, cpu, command)
                cpu_processes.append(cpu_process)
        return cpu_processes

    def _get_router_mem_ram(self) -> RAM:
        """
        :return: the RAM of the given Router.
        """
        ram = None
        raw_mem_infos = self.network_ctrl.send_command("free -m")
        raw_mem_infos = raw_mem_infos.replace("[", "").replace("]", "").replace("'", "").replace(",", "")
        raw_mem_infos = raw_mem_infos.split("\\n")
        for ram_info_line in raw_mem_infos:
            if "Mem" in ram_info_line:
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
                ram = RAM(total, used, free, shared, buffers)
        return ram


class RouterInfoJob(RemoteSystemJob):
    """
    Encapsulate RouterInfo as a job for the Server
    """""
    def run(self):
        router = self.remote_system
        router_info = RouterInfo(router)
        router_info.start()
        router_info.join()
        self.return_data({'router': router})

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
