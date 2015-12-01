import paramiko
from network.vlan import Vlan
from network.namespace import Namespace
from server.server import Router


class NetworkCtrl:

    def __init__(self, router: Router):
        print("Create Network Controller ...")
        self.vlan = Vlan('eth0', router.vlan_iface_name, router.vlan_iface_id, vlan_iface_ip=None,
                         vlan_iface_ip_mask=None)
        self.namespace = Namespace("nsp"+str(router.vlan_iface_id), self.vlan.vlan_iface_name, self.vlan.ipdb)
        self.ssh = paramiko.SSHClient()
        self.router = router

    def connect_with_router(self):
        print("Connect with router - " + self.router.model + " ...")
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
            print("[-] Couldn't send the command : " + command + ") to the router(" + self.router.ip + ")")
            print(str(e))

    def exit(self):
        print("Exit ...")
        self.namespace.delete_interface()
