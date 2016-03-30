from unittest import TestCase
from router.router import Router, Mode
from pyroute2.ipdb import IPDB
from util.dhclient import Dhclient
from subprocess import Popen, PIPE
from time import sleep


class TestDhclient(TestCase):

    def test_normal_functionality(self):
        print("Test Dhclient: update_ip")
        router = self._create_router()
        ipdb = IPDB()

        try:
            print("Get link-interface ...")
            # Get the real link interface
            link_iface = ipdb.interfaces["eth0"]
            # Create a Vlan
            print("Create VLAN ...")
            with ipdb.create(kind="vlan", ifname=router.vlan_iface_name, link=link_iface,
                             vlan_id=router.vlan_iface_id).commit() as iface:
                print("Update IP with Dhclient ...")
                Dhclient.update_ip(router.vlan_iface_name)
                iface.mtu = 1400
            # Because the IPDB need some time to update the given IP
            sleep(10)
            process = Popen(["ping", "-c", "1", "-I", router.vlan_iface_name, router.ip], stdout=PIPE, stderr=PIPE)
            stdout, sterr = process.communicate()
            if not(sterr.decode('utf-8') == "" and "Unreachable" not in stdout.decode('utf-8')):
                raise Exception(str(sterr.decode('utf-8')))
            print("[+] Test was successful")
        except Exception as e:
            print("Error: " + str(e))
            raise e
        finally:
            print("Delete VLAN ...")
            ipdb.interfaces[router.vlan_iface_name].remove().commit()
            ipdb.release()

    def test_timeout(self):
        print("Test Dhclient: timeout")
        router = self._create_router()
        # Set VLAN that doesn't exist, so no response occur.
        router._vlan_iface_id = 99
        router._vlan_iface_name = "vlan99"
        ipdb = IPDB()

        try:
            print("Get link-interface ...")
            # Get the real link interface
            link_iface = ipdb.interfaces["eth0"]
            # Create a Vlan
            print("Create VLAN ...")
            with ipdb.create(kind="vlan", ifname=router.vlan_iface_name, link=link_iface,
                             vlan_id=router.vlan_iface_id).commit() as iface:
                print("Update IP with Dhclient ...")
                Dhclient.update_ip(router.vlan_iface_name, timeout=10)
                iface.mtu = 1400
        except TimeoutError:
            print("[+] Test was successful")
        except Exception as e:
            print("Error: " + str(e))
            raise e
        finally:
            print("Delete VLAN ...")
            ipdb.interfaces[router.vlan_iface_name].remove().commit()
            ipdb.release()

    def _create_router(self):
        # Create router
        router = Router(0, "vlan21", 21, "10.223.254.254", 16, "192.168.1.1", 24, "root", "root", 1)
        router.model = "TP-LINK TL-WR841N/ND v9"
        router.mac = "e8:de:27:b7:7c:e2"
        # Has to be matched with the current mode (normal, configuration)
        router.mode = Mode.configuration
        assert isinstance(router, Router)
        return router
