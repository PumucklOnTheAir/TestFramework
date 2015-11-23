from vlan_network.vlan import VLAN
from subprocess import PIPE
from pyroute2 import netns
from pyroute2.netns.nslink import NetNS
from pyroute2.netns.process.proxy import NSPopen
from pyroute2.ipdb import IPDB
import sys
import os

class VLAN_Network:
    def __init__(self):
        self.num_vlans = 0
        self.vlan_names = []
        self.vnsps = []
        self.ipdb = IPDB()
        #self.ipdb_netns = IPDB(nl = NetNS("vnsp0"))

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
        :Desc : Schließt alle virtuellen Interfaces
        '''
        print("\nClose VLAN Network ...")
        #self.close_vnsps()
        for i in range(0,self.num_vlans):
            vlan_name = self.vlan_names.pop()
            self.delete_interface(vlan_name)
        self.close_vnsps()
        print("\n")

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
        self.vlan_names.append(vlan_iface_name)
        self.create_interface(link_iface_name,vlan_iface_name,vlan_id, vlan_iface_ip, vlan_iface_mask)

    def execute_program(self, program_command, vlan_iface_name):
        '''
        :Desc : Führt ein beliebiges Programm innerhalb eines Namespaces aus
        :param program_command: Programmausfruf mit Parametern
        :param vlan_iface_name: Welches virtuelle Interface soll verwendet werden
        '''
        print("Execute ...")
        try:
            vnsp_name = self.ipdb.interfaces[vlan_iface_name].net_ns_fd
            print("args: " + str(program_command) + " :: " + str(vnsp_name) + " bzw. sollte eigl vnsp0")
            nsp = NSPopen("vnsp0", program_command, stdout=PIPE)
            print("output: " + str(nsp.communicate()))
            nsp.wait()
            nsp.release()
        except Exception as e:
            print("[-] " + str(e))

    def encapsulate_interface_in_namespace(self, vlan_iface_name):
        '''
        :Desc : Das übergebene virtuelle Interface wird in einen Namespace gekapselt
        :param vlan_iface_name: Der Name des zu kapselnden Interfaces
        '''
        print("encapsulate ...")
        #vnsp_name = self.add_vnsp()
        vnsp_name="vnsp0"
        vlan_name = self.vlan_names[-1]
        #vlan.ip.link("set",index=i,net_ns_fd=vnsp_name)
        #vlan.ip.net_ns_fd = vnsp_name
        self.ipdb.interfaces[vlan_iface_name].net_ns_fd = vnsp_name
        print("netns: " + str(self.ipdb.interfaces[vlan_iface_name]))
        #vlan.ip.add_ip('192.168.1.11/24')
        #vlan.ip.up

    def add_vnsp(self):
        '''
        :Desc : Erstellt einen neuen Namespace und fügt diesen der Namespace-Liste hinzu
        '''
        print("add_vnsp ...")
        index = len(self.vnsps)
        vnsp_name = "vnsp"+str(index)
        #self.ip_netns = IPDB(nl = NetNS(vnsp_name))
        #vnsp = NetNS(vnsp_name, flags=os.O_CREAT)
        #netns.remove(vnsp_name)
        vnsp = netns.create(vnsp_name)
        print("netns.listnetns() : " + str(netns.listnetns()))
        self.vnsps.append(vnsp)
        return vnsp_name

    def close_vnsps(self):
        print("Close vnsps ...")
        for i in range(0,len(self.vnsps)):
            vnsp = self.vnsps[i]
            vnsp.close()
            vnsp.remove()


    def create_interface(self, link_iface_name, vlan_iface_name, vlan_id, vlan_iface_ip, vlan_iface_mask):
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

    def delete_interface(self, vlan_iface_name):
        '''
        : Desc : Löscht das virtuelle Interface
        '''
        try:
            self.ipdb.interfaces[vlan_iface_name].remove().commit()
            print("[+] " + vlan_iface_name + " successfully deleted")
        except Exception as e:
            print("[-] " + vlan_iface_name + " couldn't be deleted")
            print("  " + str(e))
        self.ipdb.release()

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


