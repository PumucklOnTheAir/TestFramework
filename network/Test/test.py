import sys
import time
#sys.path.append('/root/TestFramework/network')
sys.path.append('/home/simon/TestFramework/network/')
#sys.path.append('/home/pi/TestFramework/network/')
from vlan_network.vlan_network import VLAN_Network
from Router.router import Router

router1 = Router("192.168.1.13", "Lan1", 10)
router2 = Router("192.168.1.13", "Lan2", 20)

vn = VLAN_Network()
vn.build_network()

vn.execute_program(["ping","-c 1",router1.get_ip()], router1.get_vlan_interface_name())

#router1.update_mac_default()
#time.sleep(5)
#router2.update_mac_default()
#print("MAC from Router: " + str(router1.get_mac()))
#print("MAC from Router: " + str(router2.get_mac()) + "\n")


vn.close_network()