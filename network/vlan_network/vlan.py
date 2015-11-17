from pyroute2 import IPDB

class VLAN:
    def __init__(self, vlan_iface_name):
        self.ip = IPDB()
        self.vlan_iface_name = vlan_iface_name

    #Erstellt ein neues virtuelles Interface auf einem bestehenden.
    #link_iface_name:   das eigentliche Interface (eth0, wlan0, ...)
    #vlan_id:           ID des VLANs
    #vlan_iface_ip:     IP des neuen Interfaces
    #vlan_iface_mask:   Netzmaske des neuen Interfaces
    def create_interface(self, link_iface_name, vlan_id, vlan_iface_ip, vlan_iface_mask):
        print("Create VLAN Interface ...")
        try:
            link_iface = self.ip.interfaces[link_iface_name]
            with self.ip.create(kind="vlan", ifname=self.vlan_iface_name, link=link_iface, vlan_id=vlan_id) as i:
                i.add_ip(vlan_iface_ip, vlan_iface_mask)
                #Müsste die Größe der zu übertragenden Pake sein
                i.mtu = 1400
                print("[+] " + self.vlan_iface_name + " created with:")
                print("  Link: " + link_iface_name)
                print("  VLAN_ID: " + str(vlan_id))
                print("  IP: " + vlan_iface_ip + "/" + str(vlan_iface_mask))
        except Exception as e:
            print("[-] " + self.vlan_iface_name + " couldn't be created")
            print("  " + str(e))
            pass
        print("\n")

    #Löscht das virtuelle Interface
    def delete_interface(self):
        try:
            self.ip.interfaces[self.vlan_iface_name].remove().commit()
            print("[+] " + self.vlan_iface_name + " successfully deleted")
        except Exception as e:
            print("[-] " + self.vlan_iface_name + " couldn't be deleted")
            print("  " + str(e))
            pass
        self.ip.release()