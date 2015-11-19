from vlan_network.vlan import VLAN
from subprocess import PIPE
from pyroute2 import NetNS, NSPopen, netns
import sys
import os

class VLAN_Network:
    def __init__(self):
        self.vlans = []
        self.num_vlans = 0
        self.vnsps = []

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
            #self.encapsulate_interface_in_namespace(self.vlans[-1].vlan_iface_name)

    def close_network(self):
        '''
        :Desc : Schließt alle virtuellen Interfaces
        '''
        print("\nClose VLAN Network ...")
        #self.close_vnsps()
        for i in range(0,self.num_vlans):
            vlan = self.vlans.pop()
            vlan.delete_interface()
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

        vlan = VLAN(vlan_iface_name)
        vlan.create_interface(link_iface_name, vlan_id, vlan_iface_ip, vlan_iface_mask)
        self.vlans.append(vlan)

    def delete_vlan(self, vlan_iface_name):
        vlan = self.vlans[vlan_iface_name]
        vlan.delete_interface()

    def get_vlans(self):
        return self.vlans

    def execute_program(self, program_command, vlan_iface_name):
        '''
        :Desc : Führt ein beliebiges Programm innerhalb eines Namespaces aus
        :param program_command: Programmausfruf mit Parametern
        :param vlan_iface_name: Welches virtuelle Interface soll verwendet werden
        '''
        print("Execute ...")
        vlan = self.vlans[-1]
        vnsp_name = vlan.ip.interfaces[vlan.vlan_iface_name].net_ns_fd
        print("args: " + str(program_command) + " :: " + str(vnsp_name))
        nsp = NSPopen(vnsp_name, program_command, stdout=PIPE)
        print("output: " + str(nsp.communicate()))
        nsp.wait()
        nsp.release()

    def encapsulate_interface_in_namespace(self, vlan_iface_name):
        '''
        :Desc : Das übergebene virtuelle Interface wird in einen Namespace gekapselt
        :param vlan_iface_name: Der Name des zu kapselnden Interfaces
        '''
        print("encapsulate ...")
        vnsp_name = self.add_vnsp()
        vlan = self.vlans[-1]
        #i = vlan.ip.link_look_up(vlan.vlan_iface_name)
        #vlan.ip.link("set",index=i,net_ns_fd=vnsp_name)
        #vlan.ip.net_ns_fd = vnsp_name
        vlan.ip.interfaces[vlan.vlan_iface_name].net_ns_fd = vnsp_name
        #vlan.ip.add_ip('192.168.1.11/24')
        #vlan.ip.up

    def add_vnsp(self):
        '''
        :Desc : Erstellt einen neuen Namespace und fügt diesen der Namespace-Liste hinzu
        '''
        print("add_vnsp ...")
        index = len(self.vnsps)
        vnsp_name = "vnsp"+str(index)
        #vnsp = NetNS(vnsp_name, flags=os.O_CREAT)
        netns.remove(vnsp_name)
        vnsp = netns.create(vnsp_name)
        self.vnsps.append(vnsp)
        return vnsp_name

    def close_vnsps(self):
        print("Close vnsps ...")
        for i in range(0,self.num_vlans):
            vnsp = self.vnsps.pop()
            self.delete_vnsp(vnsp)

    def delete_vnsp(self, vnsp):
        vnsp.close()
        vnsp.remove()

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


