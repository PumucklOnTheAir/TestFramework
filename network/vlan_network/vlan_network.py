from subprocess import PIPE
from pyroute2.netns.nslink import NetNS
from pyroute2.netns.process.proxy import NSPopen
from pyroute2.ipdb import IPDB
import sys
import re

class VLAN_Network:
    def __init__(self):
        self.num_vlans = 0
        self.vlan_names = []
        self.ipdb = IPDB()
        self.ipdb_netns_dictionary = {}

    def build_network(self):
        '''
        :Desc : Baut beliebig viele virtuelle Interfaces auf
        '''
        print("\nBuild VLAN Network ...")
        self.num_vlans = int(input("Number of desired VLANs: "))
        for i in range(0,self.num_vlans):
            print("\nVirtual Interface"+str(i))
            print("------------------------")
            self.add_vlan()
            print("------------------------")
            self.encapsulate_interface_in_namespace(self.vlan_names[-1])

    def close_network(self):
        '''
        :Desc : Schließt alle virtuellen Interfaces bzw deren Namespaces
        '''
        print("\nClose VLAN Network ...")
        for i in range(0,self.num_vlans):
            vlan_iface_name = self.vlan_names.pop()
            ipdb_netns = self.ipdb_netns_dictionary[vlan_iface_name]
            self.delete_interface(ipdb_netns,vlan_iface_name,namespace=True)


    def add_vlan(self):
        input_accepted = False
        while (not input_accepted):
            try:
                link_iface_name = input("Link interface: ")
                vlan_iface_name = input("VLAN name: ")
                vlan_id = int(input("VLAN id: "))
                vlan_iface_ip = input("VLAN ip: ")
                vlan_iface_mask = int(input("VLAN ip mask: "))
                input_accepted = self.query_yes_no("Input valid?")
            except Exception as e:
                print("[-] " + str(e))
        self.create_interface(link_iface_name,vlan_iface_name,vlan_id, vlan_iface_ip, vlan_iface_mask)
        self.vlan_names.append(vlan_iface_name)

    def execute_program(self, program_command, vlan_iface_name):
        '''
        :Desc : Führt ein beliebiges Programm innerhalb eines Namespaces aus
        :param program_command: Programmausfruf mit Parametern
        :param vlan_iface_name: Welches virtuelle Interface soll verwendet werden
        '''
        print("Execute ...")
        try:
            vnsp_name = self.ipdb_netns_dictionary[vlan_iface_name].nl.netns
            nsp = NSPopen(vnsp_name, program_command, stdout=PIPE)
            print("output: " + str(nsp.communicate()))
            nsp.wait()
            nsp.release()
            print("[+] " + str(program_command) + " successfully executed")
        except Exception as e:
            print("[-] " + str(program_command) + "couldn't be executed")
            print("e: " + str(e))

    def encapsulate_interface_in_namespace(self, vlan_iface_name):
        '''
        :Desc : Das übergebene virtuelle Interface wird in einen Namespace gekapselt
        :param vlan_iface_name: Der Name des zu kapselnden Interfaces
        '''
        print("encapsulate ...")
        vnsp_name = self.add_vnsp(vlan_iface_name)
        vlan_ip = self.get_ipv4_from_dictionary(self.ipdb.interfaces[vlan_iface_name].ipaddr)
        print("vlan_name: " + vlan_iface_name + " vlan_ip: " + str(vlan_ip))
        with self.ipdb.interfaces[vlan_iface_name] as vlan:
            vlan.net_ns_fd = vnsp_name
        #Das Interface hat automatisch die Datenbank gewechselt und befindet sich jetzt in ipdb_netns_dictionary[vlan_iface_name]
        with self.ipdb_netns_dictionary[vlan_iface_name].interfaces[vlan_iface_name] as vlan:
            vlan.add_ip(vlan_ip) #'192.168.1.11/24'
            vlan.up()

    def add_vnsp(self, vlan_iface_name):
        '''
        :Desc : Erstellt einen neuen Namespace und fügt diesen dem Namespace-Dictionary hinzu
        :return Gibt den Namen des namespaces zurück
        '''
        print("add_vnsp ...")
        index = len(self.ipdb_netns_dictionary)
        vnsp_name = "vnsp"+str(index)
        ipdb_netns = IPDB(nl = NetNS(vnsp_name))
        self.ipdb_netns_dictionary[vlan_iface_name] = ipdb_netns
        return vnsp_name


    def create_interface(self, link_iface_name='eth0', vlan_iface_name='Lan1', vlan_id=10, vlan_iface_ip='127.0.0.1', vlan_iface_mask=24):
        '''
        :Desc : Erstellt ein neues virtuelles Interface auf einem bestehenden
        :param link_iface_name: Das eigentliche Interface (eth0, wlan0, ...)
        :param vlan_id: ID des VLANs
        :param vlan_iface_ip: IP des neuen Interfaces
        :param vlan_iface_mask: Netzmaske des neuen Interfaces
        '''
        print("Create VLAN Interface ...")
        try:
            link_iface = self.ipdb.interfaces[link_iface_name]
            with self.ipdb.create(kind="vlan", ifname=vlan_iface_name, link=link_iface, vlan_id=vlan_id).commit() as i:
                i.add_ip(vlan_iface_ip, vlan_iface_mask)
                #Müsste die Größe der zu übertragenden Pake sein
                i.mtu = 1400
                print("[+] " + vlan_iface_name + " created with:")
                print("  Link: " + link_iface_name)
                print("  VLAN_ID: " + str(vlan_id))
                print("  IP: " + vlan_iface_ip + "/" + str(vlan_iface_mask))
        except Exception as e:
            print("[-] " + vlan_iface_name + " couldn't be created")
            print("  " + str(e))

    def delete_interface(self, ipdb, vlan_iface_name, namespace=True):
        '''
        : Desc : Löscht das virtuelle Interface
        '''
        try:
            if namespace:
                ipdb.interfaces[vlan_iface_name].nl.remove()
            else:
                ipdb.interfaces[vlan_iface_name].remove().commit()
            print("[+] " + vlan_iface_name + " successfully deleted")
        except Exception as e:
            print("[-] " + vlan_iface_name + " couldn't be deleted")
            print("  " + str(e))
        ipdb.release()

    def get_ipv4_from_dictionary(self, ipaddr_dictionary):
        for i in range(len(ipaddr_dictionary)):
            ip = ipaddr_dictionary[i]['address']
            mask = ipaddr_dictionary[i]['prefixlen']
            if re.match("((((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3})(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))", ip):
                return (ip+"/"+str(mask))
        return None

#TODO: Diese Funktion muss ausgelagert werden
    def query_yes_no(self, question, default=None):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            choice = input(question + prompt).lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")


