from unittest import TestCase
from network.vlan import Vlan
from network.namespace import Namespace
from subprocess import Popen, PIPE
from log.logger import Logger
import time
from pyroute2.ipdb import IPDB
from pyroute2.netns.nslink import NetNS
from pyroute2.ipdb import IPDB
from pyroute2 import netns


class TestNamespace(TestCase):

    def test_create_namespace_x2(self):
        link_iface_name = "eth0"
        vlan_iface_name = "vlan21"
        vlan_iface_id = 22
        namespace_name = "nsp21"

        for i in range(0,1):
            print("Create vlan1")
            ipdb = IPDB()
            link_iface = ipdb.interfaces[link_iface_name]
            with ipdb.create(kind="vlan", ifname=vlan_iface_name, link=link_iface, vlan_id=vlan_iface_id).commit() as i:
                i.add_ip("192.168.1.11", 24)
                i.mtu = 1400

            print("Create namespace1")
            ipdb_netns = IPDB(nl=NetNS(namespace_name))
            netns.setns(namespace_name)
            ipdb_netns.interfaces['lo'].up().commit()

            print("Encapsulate vlan1 in namespace1")
            with ipdb.interfaces[vlan_iface_name] as iface:
                iface.net_ns_fd = namespace_name
            with ipdb_netns.interfaces[vlan_iface_name] as iface:
                iface.add_ip("192.168.1.11/24")  # '192.168.1.11/24'
                iface.up()

            print("Delete vlan and namespace")
            ipdb_netns.interfaces[vlan_iface_name].remove().commit()
            netns.remove(namespace_name)
            ipdb_netns.release()

            #ipdb.interfaces[vlan_iface_name].remove().commit()
            ipdb.release()


'''
    def test_create_namespace(self):
        Logger().debug("TestNamespace: test_create_namespace ...")
        # Create VLAN
        ipdb = IPDB()
        vlan = Vlan(ipdb, 'enp0s25', 'vlan21', 10)
        assert isinstance(vlan, Vlan)
        vlan.create_interface("192.168.1.11", 24)

        # Create Namespace
        namespace = Namespace(ipdb,'nsp21')
        assert isinstance(namespace, Namespace)

        #encapsulate VLAN
        namespace.encapsulate_interface(vlan.vlan_iface_name)

        # Test if the namespace now exists
        #process = Popen(["ip", "netns"], stdout=PIPE, stderr=PIPE)
        #stdout, sterr = process.communicate()
        #assert sterr.decode('utf-8') == ""
        #assert namespace.nsp_name in stdout.decode('utf-8')

        # Remove the Namespace
        namespace.remove()
        #process = Popen(["ip", "netns"], stdout=PIPE, stderr=PIPE)
        #stdout, sterr = process.communicate()
        #print(str(stdout))
        #assert stdout.decode('utf-8') == ""
        vlan.delete_interface(close_ipdb=True)

        print("test2")
        # Create VLAN
        ipdb = IPDB()
        vlan = Vlan(ipdb, 'enp0s25', 'vlan21', 10)
        assert isinstance(vlan, Vlan)
        vlan.create_interface("192.168.1.11", 24)

        # Create Namespace
        namespace = Namespace(ipdb,'nsp21')
        assert isinstance(namespace, Namespace)

        #encapsulate VLAN
        namespace.encapsulate_interface(vlan.vlan_iface_name)

        # Test if the namespace now exists
        process = Popen(["ip", "netns"], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert sterr.decode('utf-8') == ""
        assert namespace.nsp_name in stdout.decode('utf-8')

        # Remove the Namespace
        namespace.remove()
        process = Popen(["ip", "netns"], stdout=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate()
        assert stdout.decode('utf-8') == ""
        vlan.delete_interface(close_ipdb=True)
'''