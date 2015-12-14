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
        print("Connect with router ...")
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.router.ip, port=22, username=self.router.usr_name, password=self.router.usr_password)
            print("[+] Successfully connected with router(" + self.router.mac + ")")
        except Exception as e:
            print("[-] Couldn't connect to the router(" + self.router.mac + ")")
            print(str(e))

    def send_router_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            print("[+] Sent the command (" + command + ") to the router(" + self.router.ip + ")")
            output = stdout.readlines()
            return str(output)
        except Exception as e:
            print("[-] Couldn't send the command : " + command + ") to the router(" + self.router.ip + ")")
            print(str(e))

    def send_data(self, local_file: str, remote_file: str):
        try:
            sftp = self.ssh.open_sftp()
            sftp.put(local_file, remote_file)
            sftp.close()
            print("[+] Successfully send " + local_file + " to " + self.router.usr_name + "@" + self.router.ip + ":" + remote_file)
        except Exception as e:
            print("[-] Couldn't send " + local_file + " to " + self.router.usr_name + "@" + self.router.ip + ":" + remote_file)
            print(str(e))

    def exit(self):
        print("Disconnect ...")
        self.vlan.delete_interface()
        self.namespace.remove()
