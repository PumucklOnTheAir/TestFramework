from unittest import TestCase
from network.vlan import Vlan
from network.namespace import Namespace
from subprocess import Popen, PIPE
from log.logger import Logger
from multiprocessing import Process
import os
import time


class TestNamespace(TestCase):

    def test_create_namespace(self):
        for i in range(0,2):
            Logger().debug("TestNamespace: test_create_namespace ...")
            # Create VLAN
            vlan = Vlan('eth0', 'vlan21', 10, '192.168.1.10', 24)
            assert isinstance(vlan, Vlan)
            vlan.create_interface("192.168.1.11", 24)

            # Create Namespace
            namespace = Namespace('nsp21', vlan.ipdb)
            assert isinstance(namespace, Namespace)

            # encapsulate VLAN
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

    # demonstrates only the workflow auf enetering an existing namespace
    def test_enterns(self):
        print("Beginn test_enterns")

        p = Process(target=self.process1, args=())
        p.start()
        # p.join() # something in Vlan or Namespace hanging this process up
        time.sleep(2)

        p2 = Process(target=self.process2, args=())
        p2.start()
        p2.join()

    def process1(self):
        print("Process 1")
        # Create VLAN
        vlan = Vlan('eth0', 'vlan21', 10, '192.168.1.10', 24)
        assert isinstance(vlan, Vlan)
        vlan.create_interface("192.168.1.11", 24)

        # Create Namespace
        namespace = Namespace('nsp21', vlan.ipdb)
        assert isinstance(namespace, Namespace)

        # encapsulate VLAN
        namespace.encapsulate_interface(vlan.vlan_iface_name)

        os.system('ip link list')

        # time.sleep(6)

    def process2(self):
        print('Process2')
        print("before")
        os.system('ip link list')

        import ctypes
        libc = ctypes.CDLL('libc.so.6')
        fd = open('/var/run/netns/nsp21')
        libc.setns(fd.fileno(), 0)

        print("after")
        os.system('ip link list')
