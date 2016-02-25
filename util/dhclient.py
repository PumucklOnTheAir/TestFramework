from subprocess import Popen, PIPE
import socket
import struct
import fcntl
import time
from log.logger import Logger

class Dhclient:
    """
    This class represents a dhcp-client.
    """""

    @staticmethod
    def update_ip(interface: str) -> int:
        """
        Uses 'Popen' to start a dhclient in new process, for a given interface.

        :param interface: interface name
        :return: 0 = no error; 1 = error; 2 = a dhclient is already running
        """
        try:
            Logger().debug("Update IP via dhclient ...", 2)
            process = Popen(['dhclient', interface], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            while Dhclient.get_ip(interface) is None:
                time.sleep(0.5)
            if "File exists" in str(stderr):
                return 2
            elif stderr.decode('utf-8') != "":
                return 1
            return 0
        except KeyboardInterrupt:
            return 3
        except Exception as e:
            raise e

    @staticmethod
    def get_ip(interface) -> str:
        """
        Gets the ip of a specific interface
        :return: the ip of an interface without network-mask
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockfd = sock.fileno()
        ifreq = struct.pack('16sH14s', interface.encode('utf-8'), socket.AF_INET, b'\x00' * 14)
        try:
            res = fcntl.ioctl(sockfd, 0x8915, ifreq)
        except:
            return None
        ip = struct.unpack('16sH2x4s8x', res)[2]
        return socket.inet_ntoa(ip)
