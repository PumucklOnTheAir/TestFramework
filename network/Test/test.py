import sys
import time
#sys.path.append('/root/TestFramework/network')
sys.path.append('/home/simon/TestFramework/network/')
#sys.path.append('/home/pi/TestFramework/network/')
from vlan_network.vlan_network import VLAN_Network
from Router.router import Router

routers = Router.get_configured_Routers()

vn = VLAN_Network()
vn.build_network()
for i in range(0,len(routers)):
    router = routers[i]
    #vn.execute_program(["ping","-c 1",router.get_ip()], router.get_vlan_interface_name())
    router.update_mac_default()
    time.sleep(2)
    router.print_infos()


vn.close_network()