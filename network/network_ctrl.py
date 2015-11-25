import paramiko
from vlan_network import VLAN_Network
from Router.router import Router
import time

class Network_Ctrl:
    def __init__(self, router):
        self.vn = VLAN_Network()
        self.vn.build_network(namespaces=True)
        self.ssh = paramiko.SSHClient()
        self.router = router

    def connect_with_router(self):
        print("Connect with router - " +self.router.model + " ...")
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("ip of router: " + str(self.router.ip))
        self.ssh.connect(self.router.ip, port=22, username=self.router.usr_name, password=self.router.usr_password)

    def send_router_command(self, command):
        print("send command " + command + " ...")
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.readlines()
        print("stdout: " + str(output))

    def exit(self):
        self.vn.close_network(namespaces=True)


