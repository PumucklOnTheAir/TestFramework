from pyroute2.ipdb import IPDB
import time
import re
from log.logger import Logger
import os


class Vlan:
    """
    Represents a VLAN opbject.
    """""

    def __init__(self, ipdb: IPDB, link_iface_name: str, vlan_iface_name: str, vlan_iface_id: int):
        """
        Creats a virtual interface on a existing interface (like eth0).

        :param ipdb: IPDB is a transactional database, containing records, representing network stack objects.
                    Any change in the database is not reflected immidiately in OS, but waits until commit() is called.
        :param link_iface_name: name of the existing interface (eth0, wlan0, ...)
        :param vlan_iface_name: name of the vlan
        :param vlan_iface_id: the id of the vlan
        """
        self.ipdb = ipdb if ipdb else IPDB()
        self.link_iface_name = link_iface_name
        self.vlan_iface_name = vlan_iface_name
        self.vlan_iface_id = vlan_iface_id

    def create_interface(self, vlan_iface_ip: str=None, vlan_iface_ip_mask: int=None):
        """
         Creats a virtual interface on a existing interface (like eth0)

        :param vlan_iface_ip: ip of the virtual interface
        :param vlan_iface_ip_mask: network-mask of the virtual interface
        """
        Logger().debug("Create VLAN Interface ...", 2)
        try:
            link_iface = self.ipdb.interfaces[self.link_iface_name]
            with self.ipdb.create(kind="vlan", ifname=self.vlan_iface_name, link=link_iface,
                                  vlan_id=self.vlan_iface_id).commit() as i:
                if vlan_iface_ip:
                    i.add_ip(vlan_iface_ip, vlan_iface_ip_mask)
                i.mtu = 1400
            if not vlan_iface_ip:
                vlan_iface_ip = self.set_new_ip(dhcp=True)
            Logger().debug("[+] " + self.vlan_iface_name + " created with: Link=" + self.link_iface_name +
                           ", VLAN_ID=" + str(self.vlan_iface_id) + ", IP=" + vlan_iface_ip, 3)
        except Exception as e:
            Logger().debug("[-] " + self.vlan_iface_name + " couldn't be created", 3)
            Logger().error(str(e), 3)

    def delete_interface(self, close_ipdb: bool=False):
        """
        Removes the virtual interface

        :param close_ipdb: If also the IPDB should be closed.
        """
        Logger().debug("Delete VLAN Interface ...", 2)
        try:
            self.ipdb.interfaces[self.vlan_iface_name].remove().commit()
            if close_ipdb:
                self.ipdb.release()
            Logger().debug("[+] Interface(" + self.vlan_iface_name + ") successfully deleted", 3)
        except KeyError as ke:
            Logger().debug("[+] Interface(" + self.vlan_iface_name + ") is already deleted", 3)
            return
        except Exception as e:
            Logger().debug("[-] Interface(" + self.vlan_iface_name +
                           ") couldn't be deleted. Try 'ip link delete <vlan_name>'", 3)
            Logger().error(str(e), 3)

    def set_new_ip(self, dhcp: bool, new_ip: str=None, new_ip_mask: int=None):
        """
        Sets the IP either given by 'new_ip'-parameter or via dhclient.

        :param dhcp: should a dhclient be used?
        :param new_ip:
        :param new_ip_mask:
        :return: the new IP with the format ip/mask
        """
        iface_ip = None
        if dhcp:
            try:
                self._wait_for_ip_assignment()
                iface_ip = self._get_ip()
                Logger().debug("[+] New IP " + iface_ip + " for " + self.vlan_iface_name +
                               str(self.vlan_iface_id) + " by dhcp", 2)
            except TimeoutError as e:
                Logger().debug("[-] Couldn't get a new IP for " + self.vlan_iface_name +
                               str(self.vlan_iface_id) + " by dhcp", 2)
        else:
            iface_ip = new_ip+"/"+str(new_ip_mask)
            Logger().debug("[+] New IP " + iface_ip + " for " + self.vlan_iface_name + str(self.vlan_iface_id), 2)
        return iface_ip

    def _wait_for_ip_assignment(self):
        """
        Waits until the dhcp-client got an ip
        """
        Logger().debug("Wait for ip assignment via dhcp for VLAN Interface(" + self.vlan_iface_name + ") ...", 3)
        current_ip = self._get_ip().split('/')[0]
        if not self._get_ip(not_this_ip=current_ip):
            os.system('dhclient ' + self.vlan_iface_name)
            i = 0
            while self._get_ip(not_this_ip=current_ip) is None:
                time.sleep(0.5)
                i += 1
                if i == 20:
                    raise TimeoutError

    def _get_ip(self, not_this_ip: str = None):
        """
        Reads the first IP from IPDB.

        :param not_this_ip: If we know the first IP and are searching for another
        :return: the IP with the format ip/mask
        """
        iface = self.ipdb.interfaces[self.vlan_iface_name]
        ipaddr_dictionary = iface.ipaddr
        for i in range(len(ipaddr_dictionary)):
            ip = ipaddr_dictionary[i]['address']
            mask = ipaddr_dictionary[i]['prefixlen']
            if re.match("((((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3})(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))", ip):
                if ip != not_this_ip:
                    return ip + "/" + str(mask)
        return ""
