from subprocess import Popen, PIPE, TimeoutExpired
from log.loggersetup import LoggerSetup
import socket
import struct
import fcntl
import time
import logging


class Dhclient:
    """
    This class represents a dhcp-client.
    """""

    @staticmethod
    def update_ip(interface: str, timeout: int = 20):
        """
        Uses 'Popen' to start a dhclient in new process, for a given interface.

        :param interface: Network-Interface_name
        :param timeout: Time until break
        :exception KeyboardInterrupt: If the dhclient-processs is interrupted by the user.
        :exception TimeoutError: If the dhclient-process needs more time than given.
        :exception FileExistsError: If a Dhclient already exists for this Network-Interfaces
        :exception Exception: If something else go wrong
        """
        try:
            logging.debug("%sUpdate IP via dhclient (Timeout=" + str(timeout) + ") ...", LoggerSetup.get_log_deep(2))
            process = Popen(['dhclient', interface], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate(timeout=timeout)
            while Dhclient.get_ip(interface) is None:
                time.sleep(1)
                if timeout <= 0:
                    raise TimeoutError
                timeout -= 1
            if "File exists" in str(stderr):
                raise FileExistsError
            elif stderr.decode('utf-8') != "":
                raise Exception(stderr.decode('utf-8'))
            else:
                Dhclient.kill()
        except KeyboardInterrupt as ki:
            logging.warning("%s[!] KeyboardInterrupt", LoggerSetup.get_log_deep(3))
            Dhclient.kill()
            raise ki
        except TimeoutError and TimeoutExpired:
            logging.warning("%s[!] Timeout: Couldn't get any IP", LoggerSetup.get_log_deep(3))
            Dhclient.kill()
            raise TimeoutError
        except FileExistsError as fee:
            logging.warning("%s[!] A Dhclient already exist", LoggerSetup.get_log_deep(3))
            Dhclient.kill()
            raise fee
        except Exception as e:
            logging.warning("%s[!] Couldn't get a new IP", LoggerSetup.get_log_deep(3))
            logging.error("%s" + str(e), LoggerSetup.get_log_deep(3))
            Dhclient.kill()
            raise e

    @staticmethod
    def get_ip(interface: str) -> str:
        """
        Gets the ip of a specific interface

        :param interface: Interface_name
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

    @staticmethod
    def kill():
        """
        Starts a new subprocess and kills all dhclients.
        """
        logging.debug("%sKill dhclients", LoggerSetup.get_log_deep(3))
        Popen(['pkill', 'dhclient'])
