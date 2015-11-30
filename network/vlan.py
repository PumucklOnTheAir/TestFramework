from subprocess import Popen, PIPE
from pyroute2.ipdb import IPDB
import sys, time
import re
import socket, struct, fcntl

class Vlan:
    def __init__(self, link_iface_name, vlan_iface_name, vlan_iface_id, vlan_iface_ip, vlan_iface_ip_mask):
        self.vlan_iface_name = vlan_iface_name
        self.vlan_iface_id = vlan_iface_id
        self.ipdb = IPDB()
        self.create_interface(link_iface_name, vlan_iface_name, vlan_iface_id, vlan_iface_ip, vlan_iface_ip_mask)

    def create_interface(self, link_iface_name='eth0', vlan_iface_name='Lan1', vlan_iface_id=10, vlan_iface_ip=None, vlan_iface_ip_mask=24):
        '''
        :Desc : Creats a virtual interface on a existing interface (like eth0)
        :param link_iface_name: name of the existing interface (eth0, wlan0, ...)
        :param vlan_iface_id: the id of the vlan
        :param vlan_iface_ip: ip of the virtual interface
        :param vlan_iface_ip_mask: network-mask of the virtual interface
        '''
        print("Create VLAN Interface ...")
        try:
            link_iface = self.ipdb.interfaces[link_iface_name]
            with self.ipdb.create(kind="vlan", ifname=vlan_iface_name, link=link_iface, vlan_id=vlan_iface_id).commit() as i:
                if vlan_iface_ip:
                    i.add_ip(vlan_iface_ip, vlan_iface_ip_mask)
                i.mtu = 1400
            if not vlan_iface_ip:
                self.wait_for_ip_assignment(vlan_iface_name)
                vlan_iface_ip = self.get_ipv4_from_dictionary(self.ipdb.interfaces[vlan_iface_name])
            print("[+] " + vlan_iface_name + " created with:")
            print("  Link: " + link_iface_name)
            print("  VLAN_ID: " + str(vlan_iface_id))
            print("  IP: " + vlan_iface_ip)
        except Exception as e:
            print("[-] " + vlan_iface_name + " couldn't be created")
            print("  " + str(e))

    def delete_interface(self):
        '''
        : Desc : removes the virtual interface
        '''
        try:
            self.ipdb.interfaces[self.vlan_iface_name].remove().commit()
            print("[+] " + self.vlan_iface_name + " successfully deleted")
        except Exception as e:
            print("[-] " + self.vlan_iface_name + " couldn't be deleted")
            print("  " + str(e))
        self.ipdb.release()

    def wait_for_ip_assignment(self, vlan_iface_name):
        '''
        :Desc : Waits until the dhcp-client got an ip
        :param vlan_iface_name:
        '''
        print("Wait for ip assignment via dhcp...")
        while self.get_ip(vlan_iface_name) is None:
            Popen(["dhclient", vlan_iface_name], stdout=PIPE)
            time.sleep(0.5)

    def get_ip(self, vlan_iface_name ='eth0'):
        '''
        :Desc : gets the ip of a specific interface
        :param vlan_iface_name:
        :return: the ip of an interface without network-mask
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockfd = sock.fileno()
        ifreq = struct.pack('16sH14s', vlan_iface_name.encode('utf-8'), socket.AF_INET, b'\x00' * 14)
        try:
            res = fcntl.ioctl(sockfd, 0x8915, ifreq)
        except:
            return None
        ip = struct.unpack('16sH2x4s8x', res)[2]
        print("assigned ip: " + str(socket.inet_ntoa(ip)))
        return socket.inet_ntoa(ip)

    def get_ipv4_from_dictionary(self, iface):
        '''
        : Desc : gets the ip and network-mask from the ipdb
        :param iface: the interface from ipdb
        :return: ip with network-mask
        '''
        ipaddr_dictionary = iface.ipaddr
        for i in range(len(ipaddr_dictionary)):
            ip = ipaddr_dictionary[i]['address']
            mask = ipaddr_dictionary[i]['prefixlen']
            if re.match("((((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3})(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))", ip):
                return (ip + "/" + str(mask))
        return None

    #TODO: Diese Funktion muss ausgelagert werden
    def query_yes_no(self, question, default=None):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            choice = input(question + prompt).lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")