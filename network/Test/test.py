import sys
sys.path.append('/root/TestFramework/network')
from vlan_network.vlan_network import VLAN_Network
from Router.router import Router

router = Router("192.168.1.10", "Lan1", 10)

vn = VLAN_Network()
vn.build_network()

#router.update_mac_default()
print("MAC from Router: " + str(router.get_mac()))


vn.close_network()