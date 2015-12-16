from subprocess import Popen, PIPE
from pyroute2.ipdb import IPDB
import time
import re
import socket, struct, fcntl
from log.logger import Logger


class Vlan:

    def __init__(self, link_iface_name: str, vlan_iface_name: str, vlan_iface_id: int, vlan_iface_ip: str=None, vlan_iface_ip_mask: int=None):
        """
        Creats a virtual interface on a existing interface (like eth0).
        It uses IPDB: IPDB is a transactional database, containing records, representing network stack objects.
                    Any change in the database is not reflected immidiately in OS, but waits until commit() is called.
        :param link_iface_name: name of the existing interface (eth0, wlan0, ...)
        :param vlan_iface_id: the id of the vlan
        :param vlan_iface_ip: ip of the virtual interface
        :param vlan_iface_ip_mask: network-mask of the virtual interface
        """
        self.vlan_iface_name = vlan_iface_name
        self.vlan_iface_id = vlan_iface_id
        self.ipdb = IPDB()
        self.create_interface(link_iface_name, vlan_iface_name, vlan_iface_id, vlan_iface_ip, vlan_iface_ip_mask)

    def create_interface(self, link_iface_name: str='eth0', vlan_iface_name: str='Lan1', vlan_iface_id: int=10, vlan_iface_ip: str=None,
                         vlan_iface_ip_mask: int=None):
        """
         Creats a virtual interface on a existing interface (like eth0)
        :param link_iface_name: name of the existing interface (eth0, wlan0, ...)
        :param vlan_iface_id: the id of the vlan
        :param vlan_iface_ip: ip of the virtual interface
        :param vlan_iface_ip_mask: network-mask of the virtual interface
        """
        Logger().debug("Create VLAN Interface ...", 2)
        try:
            link_iface = self.ipdb.interfaces[link_iface_name]
            with self.ipdb.create(kind="vlan", ifname=vlan_iface_name, link=link_iface, vlan_id=vlan_iface_id).commit()\
                    as i:
                if vlan_iface_ip:
                    i.add_ip(vlan_iface_ip, vlan_iface_ip_mask)
                i.mtu = 1400
            if not vlan_iface_ip:
                self._wait_for_ip_assignment(vlan_iface_name)
                vlan_iface_ip = self._get_ipv4_from_dictionary(self.ipdb.interfaces[vlan_iface_name])
            Logger().debug("[+] " + vlan_iface_name + " created with: Link=" + link_iface_name + ", VLAN_ID=" + str(vlan_iface_id)+ ", IP=" + vlan_iface_ip, 3)
        except Exception as e:
            Logger().debug("[-] " + vlan_iface_name + " couldn't be created", 3)
            Logger().error(str(e), 3)

    def delete_interface(self):
        """
        Removes the virtual interface
        """
        Logger().debug("Delete VLAN Interface ...", 2)
        try:
            self.ipdb.interfaces[self.vlan_iface_name].remove().commit()
            self.ipdb.release()
            Logger().debug("[+] Interface(" + self.vlan_iface_name + ") successfully deleted", 3)
        except KeyError as ke:
            Logger().debug("[+] Interface(" + self.vlan_iface_name + ") is already deleted", 3)
            return
        except Exception as e:
            Logger().debug("[-] Interface(" + self.vlan_iface_name + ") couldn't be deleted. Try 'ip link delete <vlan_name>'", 3)
            Logger().error(str(e), 3)

    def _wait_for_ip_assignment(self, vlan_iface_name: str):
        """
        Waits until the dhcp-client got an ip
        :param vlan_iface_name:
        """
        Logger().debug("Wait for ip assignment via dhcp for VLAN Interface(" + vlan_iface_name + ") ...", 3)
        time.sleep(2)
        if not self._get_ip(vlan_iface_name):
            Popen(["dhclient", vlan_iface_name], stdout=PIPE)
            while self._get_ip(vlan_iface_name) is None:
                time.sleep(0.5)

    def _get_ip(self, vlan_iface_name: str) -> str:
        """
        Gets the ip of a specific interface
        :param vlan_iface_name:
        :return: the ip of an interface without network-mask
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockfd = sock.fileno()
        ifreq = struct.pack('16sH14s', vlan_iface_name.encode('utf-8'), socket.AF_INET, b'\x00' * 14)
        try:
            res = fcntl.ioctl(sockfd, 0x8915, ifreq)
        except:
            return None
        ip = struct.unpack('16sH2x4s8x', res)[2]
        return socket.inet_ntoa(ip)

    def _get_ipv4_from_dictionary(self, iface) -> str:
        """
        Gets the ip and network-mask from the ipdb
        :param iface: the interface from ipdb
        :return: ip with network-mask
        """
        ipaddr_dictionary = iface.ipaddr
        for i in range(len(ipaddr_dictionary)):
            ip = ipaddr_dictionary[i]['address']
            mask = ipaddr_dictionary[i]['prefixlen']
            if re.match("((((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3})(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))", ip):
                return ip + "/" + str(mask)
        return None
