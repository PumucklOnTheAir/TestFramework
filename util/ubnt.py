import paramiko
from util.power_strip import PowerStrip


class Ubnt(PowerStrip):
    """This class implements an API for the Ubiquiti mPower 6-Port mFi Power Strip
        running on Firmware version x.x.x
        Different ports can be turned on or off, each port corresponds to a router
    """

    def connect(self):
        ip = ""
        usr = "ubnt"
        pw = "ubnt"

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, usr, pw)

        return ssh

    def port_status(self, port_id):
        pass

    def up(self, port_id):
        command = ""
        ssh = self.connect()
        stdin, stdout, stderr = ssh.exec_command(command)
        pass

    def down(self, port_id):
        pass