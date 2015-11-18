from vlan_network.vlan import VLAN
from subprocess import PIPE
from pyroute2 import NetNS, NSPopen, netns
import os

class VLAN_Network:
    def __init__(self):
        self.vlans = []
        self.num_vlans = 0
        self.vnsps = []

    #Baut beliebig viele virtuelle Interfaces auf
    def build_network(self):
        print("Build VLAN Network ...")
        self.num_vlans = int(input("Number of desired VLANs: "))
        for i in range(0,self.num_vlans):
            self.add_vlan()
            self.encapsulate_interface_in_namespace(self.vlans[-1].vlan_iface_name)

    #Schließt alle virtuellen Interfaces
    def close_network(self):
        print("Close VLAN Network ...")
        #self.close_vnsps()
        for i in range(0,self.num_vlans):
            vlan = self.vlans.pop()
            vlan.delete_interface()
        print("\n")

    def add_vlan(self):
        link_iface_name = input("Link interface: ")
        vlan_iface_name = input("VLAN name: ")
        vlan_id = int(input("VLAN id: "))
        vlan_iface_ip = input("VLAN ip: ")
        vlan_iface_mask = int(input("VLAN ip mask: "))

        vlan = VLAN(vlan_iface_name)
        vlan.create_interface(link_iface_name, vlan_id, vlan_iface_ip, vlan_iface_mask)
        self.vlans.append(vlan)

    def delete_vlan(self, vlan_iface_name):
        vlan = self.vlans[vlan_iface_name]
        vlan.delete_interface()

    def get_vlans(self):
        return self.vlans

    def execute_program(self, program_command, vlan_iface_name):
        print("Execute ...")
        vlan = self.vlans[-1]
        vnsp_name = vlan.ip.interfaces[vlan.vlan_iface_name].net_ns_fd
        print("args: " + str(program_command) + " :: " + str(vnsp_name))
        nsp = NSPopen(vnsp_name, program_command, stdout=PIPE)
        print("output: " + str(nsp.communicate()))
        nsp.wait()
        nsp.release()

    def encapsulate_interface_in_namespace(self, vlan_iface_name):
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


