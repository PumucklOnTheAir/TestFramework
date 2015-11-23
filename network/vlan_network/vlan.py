from pyroute2 import IPDB
class VLAN:
    def __init__(self, ipdb, vlan_iface_name):
        #self.ip = IPDB()
        self.ipdb = ipdb
        self.vlan_iface_name = vlan_iface_name

    def create_interface(self, link_iface_name, vlan_id, vlan_iface_ip, vlan_iface_mask):
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
            with self.ipdb.create(kind="vlan", ifname=self.vlan_iface_name, link=link_iface, vlan_id=vlan_id).commit() as i:
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

    def delete_interface(self):
        '''
        : Desc : Löscht das virtuelle Interface
        '''
        try:
            self.ipdb.interfaces[self.vlan_iface_name].remove().commit()
            print("[+] " + self.vlan_iface_name + " successfully deleted")
        except Exception as e:
            print("[-] " + self.vlan_iface_name + " couldn't be deleted")
            print("  " + str(e))
        self.ipdb.release()
