import sys
import time
#sys.path.append('/root/TestFramework/network')
#sys.path.append('/home/simon/TestFramework/network/')
#sys.path.append('/home/pi/TestFramework/network/')
from vlan_network.vlan_network import VLAN_Network
from Router.router import Router

from subprocess import PIPE
from pyroute2 import netns
from pyroute2.netns.nslink import NetNS
from pyroute2.netns.process.proxy import NSPopen
from pyroute2.ipdb import IPDB
import subprocess

print("begin ...")
vlan_iface_name = 'Lan1'
vnsp_name = 'vnsp0'

ipdb = IPDB()
ipdb_netns = IPDB(nl=NetNS(vnsp_name))

program_command = ["ping","-c 1",'192.168.1.12']
link_iface = ipdb.interfaces['eth0']
print("create interface ...")
with ipdb.create(kind="vlan", ifname=vlan_iface_name, link=link_iface, vlan_id=10).commit() as i:
    i.add_ip('192.168.1.11', 24)
    i.mtu = 1400
    i.up()

print("add namespace ...")
with ipdb.interfaces.Lan1 as lan:
    lan.net_ns_fd = vnsp_name
with ipdb_netns.interfaces.Lan1 as lan:
    lan.add_ip('192.168.1.11/24')
    lan.up()

#ipdb.create(ifname='v0p0', kind='veth', peer='v0p1').commit()
#with ipdb.interfaces.v0p1 as veth:
#    veth.net_ns_fd = vnsp_name
#print("create namepsace ...")
#netns.create(vnsp_name)


'''
with ipdb.interfaces.v0p0 as veth:
    veth.add_ip('172.16.200.1/24')
    veth.up()
with ipdb_netns.interfaces.v0p1 as veth:
    veth.add_ip('172.16.200.2/24')
    veth.up()
'''

print("execute ...")
#with ipdb_netns.interfaces.Lan1 as lan:
#    vnsp_name = lan.net_ns_fd
print("args: " + str(program_command) + " :: " + str(vnsp_name) + " bzw. sollte eigl vnsp0")
try:
    nsp = NSPopen("vnsp0", program_command, stdout=PIPE)
    print("output: " + str(nsp.communicate()))
    nsp.wait()
    nsp.release()
except Exception as e:
    print("e: " + str(e))

print("close ...")
try:
    ipdb.interfaces[vlan_iface_name].remove().commit()
    print("[+] " + vlan_iface_name + " successfully deleted")
except Exception as e:
    print("[-] " + vlan_iface_name + " couldn't be deleted")
    print("  " + str(e))
ipdb.release()

print("end ...")


'''
routers = Router.get_configured_routers(manually=True)

vn = VLAN_Network()
vn.build_network()
for i in range(0,len(routers)):
    router = routers[i]
    #vn.execute_program(["ping","-c 1",router.get_ip()], router.get_vlan_interface_name())
    #router.update_mac_default()
    time.sleep(2)
    router.print_infos()


vn.close_network()
'''