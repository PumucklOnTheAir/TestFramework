from pyroute2.ipdb import IPDB
import re
from log.loggersetup import LoggerSetup
import logging
from network.remote_system import RemoteSystem
from util.dhclient import Dhclient


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
         Creates a virtual interface on a existing interface (like eth0)
        """
        logging.debug("%sCreate VLAN Interface ...", LoggerSetup.get_log_deep(2))
        try:
            # Get the real link interface
            link_iface = self.ipdb.interfaces[self.link_iface_name]

            # Create a Vlan
            iface = self.ipdb.create(kind="vlan", ifname=self.vlan_iface_name, link=link_iface,
                                     vlan_id=self.vlan_iface_id).commit()
            # Try to assign an IP via dhclient
            # IP 169.254.235.157/16 is returned when static is expected
            if (not self._wait_for_ip_assignment()) or (self.ipdb_get_ip("169.254.235.157") == ""):
                # Otherwise add a static IP
                iface.add_ip(self._get_matching_ip(str(self.remote_system.ip)), self.remote_system.ip_mask).commit()
            iface.mtu = 1400

            logging.debug("%s[+] " + self.vlan_iface_name + " created with: Link=" + self.link_iface_name +
                          ", VLAN_ID=" + str(self.vlan_iface_id) + ", IP=" + self.ipdb_get_ip(),
                          LoggerSetup.get_log_deep(3))
        except Exception as e:
            logging.debug("%s[-] " + self.vlan_iface_name + " couldn't be created", LoggerSetup.get_log_deep(3))
            logging.error("%s" + str(e), LoggerSetup.get_log_deep(3))

    def delete_interface(self, close_ipdb: bool=False):
        """
        Removes the virtual interface

        :param close_ipdb: If also the IPDB should be closed.
        """
        logging.debug("%sDelete VLAN Interface ...", LoggerSetup.get_log_deep(2))
        try:
            self.ipdb.interfaces[self.vlan_iface_name].remove().commit()
            if close_ipdb:
                self.ipdb.release()
            logging.debug("%s[+] Interface(" + self.vlan_iface_name + ") successfully deleted",
                          LoggerSetup.get_log_deep(3))
        except KeyError:
            logging.debug("%s[+] Interface(" + self.vlan_iface_name + ") is already deleted",
                          LoggerSetup.get_log_deep(3))
            return
        except Exception as e:
            logging.debug("%s[-] Interface(" + self.vlan_iface_name +
                          ") couldn't be deleted. Try 'ip link delete <vlan_name>'", LoggerSetup.get_log_deep(3))
            logging.error("%s" + str(e), LoggerSetup.get_log_deep(3))

    def _wait_for_ip_assignment(self) -> bool:
        """
        Waits until the dhcp-client got an ip

        :return: True if we got a IP via dhclient
        """
        logging.debug("%sWait for IP assignment via dhcp for VLAN Interface(" + self.vlan_iface_name + ") ...",
                      LoggerSetup.get_log_deep(3))
        try:
            ret = Dhclient.update_ip(self.vlan_iface_name)
            if ret == 2:
                logging.warning("[!] dhclient already exists")
            elif ret == 1:
                logging.debug("[-] Couldn't get an IP via dhclient")
            else:
                return True
            return False
        except Exception as e:
            logging.debug("[-] Couldn't get an IP via dhclient")
            logging.error("%s" + str(e), LoggerSetup.get_log_deep(3))
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
        logging.debug("Set static IP for VLAN(" + str(self.vlan_iface_id) + ")")
        last_numer = int(ip.split(".")[-1])
        new_numer = last_numer
        if last_numer < 254:
            new_numer += 1
        else:
            new_numer -= 1

        return ip.replace(str(last_numer), str(new_numer))
