from subprocess import Popen, PIPE
import re
from Router.wlan_mode import Mode

class Router:
    def __init__(self, vlan_interface_name, vlan_id, ip, ip_mask):
        self.model = "TP-LINK-DEFAULT"
        self.revision = "0.0"
        self.vlan_id = vlan_id
        self.vlan_interface_name = vlan_interface_name
        self.ip = ip
        self.ip_mask = ip_mask
        self.mac = "ff:ff:ff:ff:ff:ff"
        self.wlan_mode = Mode.managed

    @staticmethod
    def get_configured_Routers():
        '''
        :Desc : Der Nutzer kann beliebig viele Router konfigurieren
        :return: Eine List konfigurierter Router
        '''
        print("Configure Routers ...")
        num_routers = int(input("Number of connected routers: "))
        routers = []
        for i in range(1,num_routers+1):
            print("\nRouter"+str(i)+"")
            print("------------------------")
            vlan_interface_name = input("VLAN name: ")
            vlan_id = int(input("VLAN id: "))
            ip = input("IP: ")
            ip_mask = int(input("IP mask: "))
            print("------------------------")
            router = Router(vlan_interface_name, vlan_id, ip, ip_mask)
            routers.append(router)
        return routers

    #TODO: Es muss noch überprüft werden ob die MAC auch tatsächlich zur IP des Routers gehört
    def update_mac(self, ip, vlan_interface_name, vlan_id):
        '''
        :Desc : Sendet einen Ping über das angegebene Interface. Danach wird die MAC-Adresse aus der ARP-Tabelle extrahiert
        :param ip: IP des Router
        :param vlan_interface_name: Name des virtuellen Interfaces
        :param vlan_id: ID des VLANs indem sich der Router befindet
        '''
        print("\nUpdate MAC for " + vlan_interface_name + " ...")
        try:
            Popen(["ping", "-c", "1", "-I", vlan_interface_name, ip], stdout=PIPE)
            pid = Popen(["arp", "-n", ip], stdout=PIPE, stderr=None)
            s = pid.communicate()[0]
            self.mac = re.search(b"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]
        except Exception as e:
            print("[-] " + str(e))
            pass


    def update_mac_default(self):
        '''
        :Desc : Sendet einen Ping über das angegebene Interface. Danach wird die MAC-Adresse aus der ARP-Tabelle extrahier
        '''
        self.update_mac(self.ip, self.vlan_interface_name, self.vlan_id)

    def print_infos(self):
        print("\n############## Router - " + self.model + " ##############")
        print("Revision : " + self.revision)
        print("MAC      : " + str(self.mac))
        print("VLAN name: " + self.vlan_interface_name)
        print("VLAN id  : " + str(self.vlan_id))
        print("IP       : " + self.ip)
        print("IP mask  : " + str(self.ip_mask))
        print("######################################################")

    def set_ip(self, ip):
        self.ip = ip

    def set_vlanIP(self, vlan_id):
        self.vlan_id = vlan_id

    def set_mac(self, mac):
        self.mac = mac

    def set_mode(self, mode):
        self.wlan_mode = mode

    def set_vlan_interface_name(self, vlan_interface_name):
        self.vlan_interface_name = vlan_interface_name

    def get_ip(self):
        return self.ip

    def get_vlanID(self):
        return self.vlan_id

    def get_mac(self):
        return self.mac

    def get_mode(self):
        return self.wlan_mode

    def get_vlan_interface_name(self):
        return self.vlan_interface_name