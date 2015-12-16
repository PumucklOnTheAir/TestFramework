import paramiko
from network.vlan import Vlan
from network.namespace import Namespace
from server.server import Router
from log.logger import Logger
import os

class NetworkCtrl:

    def __init__(self, router: Router):
        """
        Creats a VLAN and a Namespace for the specific Router and 'eth0' as the link-interface.
        The VLAN will be encapsulate in the Namespace.
        Also the a SSHClient will be created.
        :param router:
        """
        Logger().info("Create Network Controller for Router(" + str(router.vlan_iface_id) + ") ...", 1)
        self.vlan = Vlan('eth0', router.vlan_iface_name, router.vlan_iface_id, vlan_iface_ip=None, vlan_iface_ip_mask=None)
        self.namespace = Namespace("nsp"+str(router.vlan_iface_id), self.vlan.vlan_iface_name, self.vlan.ipdb)
        self.ssh = paramiko.SSHClient()
        self.router = router

    def connect_with_router(self):
        """
        Connects to the Router via SSH(Paramiko).
        Ignores a missing signatur.
        """
        Logger().info("Connect with Router(" + str(self.router.vlan_iface_id) + ") ...", 1)
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.router.ip, port=22, username=self.router.usr_name, password=self.router.usr_password)
            Logger().debug("[+] Successfully connected with Router(" + str(self.router.vlan_iface_id) + ")", 2)
        except Exception as e:
            Logger().error("[-] Couldn't connect to the Router(" + str(self.router.vlan_iface_id) + ")", 2)
            Logger().error(""+str(e), 1)

    def send_router_command(self, command) -> str:
        """
        Sends the given command via SSH to the Router.
        :param command: like "ping 8.8.8.8"
        :return: The output of the command given by the Router
        """
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            Logger().debug("[+] Sent the command (" + command + ") to the Router(" + str(self.router.vlan_iface_id) + ")", 2)
            output = stdout.readlines()
            return str(output)
        except Exception as e:
            Logger().error("[-] Couldn't send the command (" + command + ") to the Router(" + str(self.router.vlan_iface_id) + ")", 2)
            Logger().error(str(e), 2)

    def send_data(self, local_file: str, remote_file: str):
        """
        Sends Data via sftp to the Router
        :param local_file: Path to the local file
        :param remote_file: Path on the Router, where the file should be saved
        """
        try:
            '''
            sftp = self.ssh.open_sftp()
            sftp.put(local_file, remote_file)
            sftp.close()
            '''
            command = 'sshpass  -p' + self.router.usr_password + ' scp ' + local_file + ' ' + self.router.usr_name +'@' + self.router.ip + ':' + remote_file
            os.system(command)
            Logger().debug("[+] Sent data '" + local_file + "' to Router(" + str(self.router.vlan_iface_id) + ") '" + self.router.usr_name + "@" + self.router.ip + ":" + remote_file + "'", 2)
        except Exception as e:
            Logger().error("[-] Couldn't send '" + local_file + "' to Router(" + str(self.router.vlan_iface_id) + ") '" + self.router.usr_name + "@" + self.router.ip + ":" + remote_file + "'", 2)
            Logger().error(str(e), 2)

    def exit(self):
        """
        Delete the VLAN resp. the Namespace with the VLAN
        """
        Logger().info("Disconnect with Router(" + str(self.router.vlan_iface_id) + ") ...", 1)
        self.vlan.delete_interface()
        self.namespace.remove()
