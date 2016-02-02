from pyroute2.ipdb import IPDB
import re
from log.logger import Logger
from network.remote_system import RemoteSystem
import os


class Vlan:
    """
    Represents a VLAN opbject.
    """""

    def __init__(self, ipdb: IPDB, remote_system: RemoteSystem, link_iface_name):
        """
        Creats a virtual interface on a existing interface (like eth0).

        :param ipdb: IPDB is a transactional database, containing records, representing network stack objects.
                    Any change in the database is not reflected immidiately in OS, but waits until commit() is called.
        :param link_iface_name: name of the existing interface (eth0, wlan0, ...)
        """
        self.ipdb = ipdb if ipdb else IPDB()
        self.remote_system = remote_system
        self.link_iface_name = link_iface_name
        self.vlan_iface_name = str(remote_system.vlan_iface_name)
        self.vlan_iface_id = int(remote_system.vlan_iface_id)

    def create_interface(self):
        """
         Creats a virtual interface on a existing interface (like eth0)
        """
        Logger().debug("Create VLAN Interface ...", 2)
        try:
            # Get the real link interface
            link_iface = self.ipdb.interfaces[self.link_iface_name]

            # Create a Vlan
            iface = self.ipdb.create(kind="vlan", ifname=self.vlan_iface_name, link=link_iface,
                                     vlan_id=self.vlan_iface_id).commit()
            # Try to assign an IP via dhclient
            if not self._wait_for_ip_assignment():
                # Otherwise add a static IP
                iface.add_ip(self._get_matching_ip(str(self.remote_system.ip)), self.remote_system.ip_mask).commit()
            iface.mtu = 1400

            Logger().debug("[+] " + self.vlan_iface_name + " created with: Link=" + self.link_iface_name +
                           ", VLAN_ID=" + str(self.vlan_iface_id) + ", IP=" + self.ipdb_get_ip(), 3)
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
        except KeyError:
            Logger().debug("[+] Interface(" + self.vlan_iface_name + ") is already deleted", 3)
            return
        except Exception as e:
            Logger().debug("[-] Interface(" + self.vlan_iface_name +
                           ") couldn't be deleted. Try 'ip link delete <vlan_name>'", 3)
            Logger().error(str(e), 3)

    def _wait_for_ip_assignment(self) -> bool:
        """
        Waits until the dhcp-client got an ip

        :return: True if we got a IP via dhclient
        """
        Logger().debug("Wait for IP assignment via dhcp for VLAN Interface(" + self.vlan_iface_name + ") ...", 3)
        try:
            stout = os.system('dhclient ' + self.vlan_iface_name)
            return stout == 0
        except KeyboardInterrupt:
            return False
        except Exception as e:
            Logger().debug("[-] Couldn't get an IP via dhclient")
            Logger().error(str(e), 3)
            return False

    def ipdb_get_ip(self, not_this_ip: str = None):
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

    def _get_matching_ip(self, ip: str) -> str:
        """
        Calculates the right IP for a given one.

        :param ip: IP address
        :return: New IP address
        """
        Logger().debug("")
        last_numer = int(ip.split(".")[-1])
        new_numer = last_numer
        if last_numer < 254:
            new_numer += 1
        else:
            new_numer -= 1

        return ip.replace(str(last_numer), str(new_numer))
