from vlan_network.vlan import VLAN

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

    #Schließt alle virtuellen Interfaces
    def close_network(self):
        print("Close VLAN Network ...")
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

