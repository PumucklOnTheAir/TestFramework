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
        print("Configure Routers ...")
        num_routers = int(input("Number of connected routers: "))
        routers = []
        for i in range(1,num_routers+1):
            print("Router"+str(i)+"")
            print("----------------")
            vlan_interface_name = input("VLAN name: ")
            vlan_id = int(input("VLAN id: "))
            ip = input("IP: ")
            ip_mask = int(input("IP mask: "))
            router = Router(vlan_interface_name, vlan_id, ip, ip_mask)
            routers.append(router)
        return routers

    #TODO: Es muss noch überprüft werden ob die MAC auch tatsächlich zur IP des Routers gehört
    #Sendet einen Ping über das angegebene Interface
    #danach wird die MAC-Adresse aus der ARP-Tabelle extrahiert
    def update_mac(self, ip, vlan_interface_name, vlan_id):
        Popen(["ping", "-c", "1", "-I", vlan_interface_name, ip], stdout=PIPE)
        pid = Popen(["arp", "-n", ip], stdout=PIPE)
        s = pid.communicate()[0]
        self.mac = re.search(b"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]

    def update_mac_default(self):
        self.update_mac(self.ip, self.vlan_interface_name, self.vlan_id)

    def print_infos(self):
        print("############## Router - " + self.model + " ##############")
        print("Revision: " + self.revision)
        print("MAC: " + self.mac)
        print("VLAN name: " + self.vlan_interface_name)
        print("VLAN id: " + str(self.vlan_id))
        print("IP: " + self.ip)
        print("IP mask:" + str(self.ip_mask))

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