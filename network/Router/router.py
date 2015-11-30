from subprocess import Popen, PIPE
import re
from Router.wlan_mode import Mode

class Router:
    def __init__(self, usr_name, usr_password, vlan_iface_name, vlan_iface_id, ip, ip_mask):
        self.model = "TP-LINK-DEFAULT"
        self.usr_name = usr_name
        self.usr_password = usr_password
        self.vlan_iface_id = vlan_iface_id
        self.vlan_iface_name = vlan_iface_name
        self.ip = ip
        self.ip_mask = ip_mask
        self.mac = "ff:ff:ff:ff:ff:ff"
        self.ssid = "SSID-Default"
        self.wlan_mode = Mode.managed

    @staticmethod
    def get_manual_configured_routers():
        '''
        :Desc : Der Nutzer kann beliebig viele Router konfigurieren
        :return: Eine List konfigurierter Router
        '''
        print("Configure Routers manually...")
        num_routers = int(input("Number of connected routers: "))
        routers = []
        for i in range(1,num_routers+1):
            print("\nRouter"+str(i)+"")
            print("------------------------")
            usr_name = input("Usr name: ")
            usr_password = input("Usr password: ")
            vlan_interface_name = input("VLAN name: ")
            vlan_id = int(input("VLAN id: "))
            ip = input("IP: ")
            ip_mask = int(input("IP mask: "))
            print("------------------------")
            router = Router(usr_name, usr_password, vlan_interface_name, vlan_id, ip, ip_mask)
            routers.append(router)
        return routers

    #TODO: Es muss noch überprüft werden ob der INput gültig ist
    @staticmethod
    def get_auto_configured_routers():
        print("Configure Routers automatically...")
        num_routers = int(input("Number of connected routers: "))
        first_vlan_id = int(input("First VLAN id: "))
        routers = []
        for i in range(1,num_routers+1):
            usr_name = "root"
            usr_password = "admin"
            vlan_interface_name = "VLan"+str(i)
            vlan_id = first_vlan_id+(i-1)
            ip, ip_mask = Router.get_gateway_ip()
            print("\nRouter"+str(i)+"")
            print("------------------------")
            print("Usr name: " + usr_name)
            print("Usr password: " + usr_password)
            print("VLAN name: " + vlan_interface_name)
            print("VLAN id: " + str(vlan_id))
            print("IP: " + ip)
            print("IP mask: " + ip_mask)
            print("------------------------")
            #if not(query_yes_no("Input valid?")):
            #    get_manual_configured_routers()
            #else:
            router = Router(usr_name, usr_password, vlan_interface_name, vlan_id, ip, ip_mask)
            routers.append(router)
        return routers

    @staticmethod
    def get_conf_configured_routers(args=[]):
        if not args:
            return None

    @staticmethod
    def get_configured_routers(manually=False, args=[]):
        print("Configure Routers ...")
        if manually:
            return Router.get_manual_configured_routers()
        else:
            #Es wurden keine Argumente übergeben
            if args:
                return Router.get_conf_configured_routers(args)
            else:
                return Router.get_auto_configured_routers()

    @staticmethod
    def get_gateway_ip():
        try:
            ip_route = Popen(["ip", "route"], stdout=PIPE)
            s = ip_route.communicate()[0]
            gateway_ip = re.search(b"((((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3})(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))", s).groups()[0].decode("utf-8")
            gateway_mask = re.search(b"(\/([1-2]\d|3[0-2]))", s).groups()[0].decode("utf-8")[1:]
            return [gateway_ip, gateway_mask]
        except Exception as e:
            print("[-] " + str(e))
            pass


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
            self.mac = re.search(b"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0].decode("utf-8")
        except Exception as e:
            print("[-] " + str(e))
            pass


    def update_mac_default(self):
        '''
        :Desc : Sendet einen Ping über das angegebene Interface. Danach wird die MAC-Adresse aus der ARP-Tabelle extrahier
        '''
        self.update_mac(self.ip, self.vlan_iface_name, self.vlan_iface_id)

    def print_infos(self):
        print("\n############## Router - " + self.model + " ##############")
        print("MAC      : " + str(self.mac))
        print("Usr name : " + self.usr_name)
        print("VLAN name: " + self.vlan_iface_name)
        print("VLAN id  : " + str(self.vlan_iface_id))
        print("IP       : " + self.ip)
        print("IP mask  : " + str(self.ip_mask))
        print("SSID     : " + self.ssid)
        print("######################################################")
