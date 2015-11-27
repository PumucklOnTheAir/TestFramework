import paramiko
from vlan_network import VLAN_Network
from Router.router import Router
from vlan import Vlan
from namespace import Namespace
import time, re

class Network_Ctrl:
    def __init__(self, router, id):
        print("Create Network Controller ...")
        #self.vn = VLAN_Network()
        #self.vn.build_network(namespaces=True)
        self.id = id
        self.vlan = Vlan()
        self.namespace = Namespace("nsp"+str(id), self.vlan.vlan_iface_name, self.vlan.ipdb)
        self.ssh = paramiko.SSHClient()
        self.router = router

    def connect_with_router(self):
        print("Connect with router - " +self.router.model + " ...")
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("ip of router: " + str(self.router.ip))
        self.ssh.connect(self.router.ip, port=22, username=self.router.usr_name, password=self.router.usr_password)

    def send_router_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            print("[+] Sent the command (" + command + ") to the router(" + self.router.ip + ")")
            output = stdout.readlines()
            return str(output)
        except Exception as e:
            print("[-] Couldn't send the command : " + command + ") to the router(" + self.router.ip + ")");
            print(str(e))

    def configure_router(self):
        #Model
        self.router.model = self.send_router_command('cat /proc/cpuinfo | grep machine').split(":")[1][:-4]
        #MAC
        self.router.mac = self.send_router_command('uci show network.client.macaddr').split('=')[1][:-4]
        #SSID
        self.router.ssid = self.send_router_command('uci show wireless.client_radio0.ssid').split('=')[1][:-4]

    def exit(self):
        print("Exit ...")
        self.namespace.delete_interface()
        #self.vn.close_network(namespaces=True)


