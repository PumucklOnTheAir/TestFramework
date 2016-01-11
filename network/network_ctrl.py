import os

import paramiko

from log.logger import Logger
from network.namespace import Namespace
from network.vlan import Vlan
from network.web_config_assist import WebConfigurationAssist
from network.webserver import WebServer
from server.server import Router


class NetworkCtrl:
    """
    The NetworkCtrl manages:
        1. Creates a Vlan and a Namespace
        2. Encapsulates the Vlan inside the Namespace
        3. Provides a SSH-Connection via paramiko
        4. Provides a WebServer
        5. Provides a Web_configuration_Assistent
    """

    def __init__(self, router: Router, link_iface_name='eth0'):
        """
        Creats a VLAN and a Namespace for the specific Router and 'eth0' as the link-interface.
        The VLAN will be encapsulate in the Namespace.
        Also the a SSHClient will be created.
        :param router:
        """
        Logger().info("Create Network Controller for Router(" + str(router.id) + ") ...", 1)
        self.router = router

        self.vlan = Vlan(link_iface_name, router.vlan_iface_name, router.vlan_iface_id,
                         vlan_iface_ip=None, vlan_iface_ip_mask=None)
        self.vlan.create_interface()

        self.namespace = Namespace("nsp"+str(router.vlan_iface_id), self.vlan.ipdb)
        self.namespace.encapsulate_interface(self.vlan.vlan_iface_name)

        self.ssh = paramiko.SSHClient()

    def connect_with_router(self):
        """
        Connects to the Router via SSH(Paramiko).
        Ignores a missing signatur.
        """
        Logger().info("Connect with Router(" + str(self.router.id) + ") ...", 1)
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.router.ip, port=22, username=self.router.usr_name, password=self.router.usr_password)
            Logger().debug("[+] Successfully connected with Router(" + str(self.router.id) + ")", 2)
        except Exception as e:
            Logger().error("[-] Couldn't connect to the Router(" + str(self.router.id) + ")", 2)
            Logger().error(""+str(e), 1)

    def send_router_command(self, command) -> str:
        """
        Sends the given command via SSH to the Router.
        :param command: like "ping 8.8.8.8"
        :return: The output of the command given by the Router
        """
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            output = stdout.readlines()
            Logger().debug("[+] Sent the command (" + command + ") to the Router(" + str(self.router.id) + ")", 2)
            return str(output)
        except Exception as e:
            Logger().error("[-] Couldn't send the command (" + command +
                           ") to the Router(" + str(self.router.id) + ")", 2)
            Logger().error(str(e), 2)

    def send_data(self, local_file: str, remote_file: str):
        """
        Sends Data via sftp to the Router
        :param local_file: Path to the local file
        :param remote_file: Path on the Router, where the file should be saved
        """
        try:
            # TODO: If sftp is installed on the Router
            '''
            sftp = self.ssh.open_sftp()
            sftp.put(local_file, remote_file)
            sftp.close()
            '''
            command = 'sshpass  -p' + self.router.usr_password + ' scp ' + local_file + ' ' + \
                      self.router.usr_name + '@' + self.router.ip + ':' + remote_file
            os.system(command)

            # TODO: Paramiko_scp have to installed
            '''
            scp = SCPClient(self.ssh.get_transport())
            scp.put(local_file, remote_file)
            '''
            Logger().debug("[+] Sent data '" + local_file + "' to Router(" + str(self.router.id) + ") '" +
                           self.router.usr_name + "@" + self.router.ip + ":" + remote_file + "'", 2)
        except Exception as e:
            Logger().error("[-] Couldn't send '" + local_file + "' to Router(" + str(self.router.id) + ") '" +
                           self.router.usr_name + "@" + self.router.ip + ":" + remote_file + "'", 2)
            Logger().error(str(e), 2)

    def router_wget(self, file: str, remote_path: str):
        """
        The Router downloads the file from the PI and stores it at remote_file
        :param file: like /root/TestFramework/firmware/.../<firmware>.bin
        :param remote_path: like /tmp/
        """
        try:
            webserver = WebServer()
            webserver.start()
            self.send_router_command('wget -N http://' +
                                     self.namespace.get_ip_of_encapsulate_interface() + ':' +
                                     str(WebServer.PORT_WEBSERVER) +
                                     file.replace(WebServer.BASE_DIR, '') +
                                     ' -P ' + remote_path)
            webserver.join()
        except Exception as e:
            Logger().error(str(e), 2)

    def wca_setup_wizard(self, config):
        """
        Starts the WebConfigurationAssist and
        sets the values provided by the wizard-mode (in the WebConfiguration)
        :param config: {node_name, mesh_vpn, limit_bandwidth, show_location, latitude, longitude, altitude, contact,...}
        """
        try:
            wca = WebConfigurationAssist(config, self.router)
            wca.setup_wizard()
            wca.exit()
        except Exception as e:
            Logger().error(str(e), 2)
            self.exit()
            raise e

    def wca_setup_expert(self, config):
        """
        Starts the WebConfigurationAssist and
        sets the values provided by the expert-mode(in the WebConfiguration)
        :param config: {node_name, mesh_vpn, limit_bandwidth, show_location, latitude, longitude, altitude, contact,...}
        """
        try:
            wca = WebConfigurationAssist(config, self.router)
            wca.setup_expert_private_wlan()
            wca.setup_expert_remote_access()
            wca.setup_expert_network()
            wca.setup_expert_mesh_vpn()
            wca.setup_expert_wlan()
            wca.setup_expert_autoupdate()
            wca.exit()
        except Exception as e:
            Logger().error(str(e), 2)
            self.exit()
            raise e

    def exit(self):
        """
        Delete the VLAN resp. the Namespace with the VLAN
        """
        Logger().info("Close Network Controller for Router(" + str(self.router.id) + ") ...", 1)
        self.vlan.delete_interface()
        self.namespace.remove()