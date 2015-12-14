import paramiko
from network.vlan import Vlan
from network.namespace import Namespace
from server.server import Router
from log.logger import Logger


class NetworkCtrl:

    def __init__(self, router: Router):
        Logger().info("Create Network Controller for Router(" + router.mac + ") ...")
        self.vlan = Vlan('eth0', router.vlan_iface_name, router.vlan_iface_id, vlan_iface_ip=None, vlan_iface_ip_mask=None)
        self.namespace = Namespace("nsp"+str(router.vlan_iface_id), self.vlan.vlan_iface_name, self.vlan.ipdb)
        self.ssh = paramiko.SSHClient()
        self.router = router

    def connect_with_router(self):
        Logger().info("Connect with Router(" + self.router.mac + ") ...")
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.router.ip, port=22, username=self.router.usr_name, password=self.router.usr_password)
            Logger().debug("[+] Successfully connected with router(" + self.router.mac + ")", 1)
        except Exception as e:
            Logger().error("[-] Couldn't connect to the router(" + self.router.mac + ")", 1)
            Logger().error(""+str(e), 1)

    def send_router_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            Logger().debug("[+] Sent the command (" + command + ") to the router(" + self.router.ip + ")", 1)
            output = stdout.readlines()
            return str(output)
        except Exception as e:
            Logger().error("[-] Couldn't send the command : " + command + ") to the router(" + self.router.ip + ")", 1)
            Logger().error(str(e), 1)

    def send_data(self, local_file: str, remote_file: str):
        try:
            sftp = self.ssh.open_sftp()
            sftp.put(local_file, remote_file)
            sftp.close()
            Logger().debug("[+] Sent data " + local_file + " to Router(" + self.router.mac + ") " + self.router.usr_name + "@" + self.router.ip + ":" + remote_file, 1)
        except Exception as e:
            Logger().error("[-] Couldn't send " + local_file + " to Router(" + self.router.mac + ") " + self.router.usr_name + "@" + self.router.ip + ":" + remote_file, 1)
            Logger().error(str(e), 1)

    def exit(self):
        Logger().info("Disconnect with Router(" + self.router.mac + ") ...")
        self.vlan.delete_interface()
        self.namespace.remove()
