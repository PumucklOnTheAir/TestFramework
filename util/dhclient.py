from subprocess import Popen, PIPE


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
            process = Popen(['dhclient', interface], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if "File exists" in str(stderr):
                return 2
            elif stderr.decode('utf-8') != "":
                return 1
            return 0
        except KeyboardInterrupt:
            return 0
        except Exception as e:
            raise e
