from server.ipc import IPC
from server.serverproxy import ServerProxy
from cli.cli_util import CLIUtil
import sys
import argparse
import time


def connect_to_server():
    """ Initiates connection to the IPC server by creating a client
    """
    dummy_runtime_server = DummyServer()
    # dummy_runtime_server = ServerProxy

    ipc_server = IPC()
    ipc_server.start_ipc_server(dummy_runtime_server)

    print("Setting up server...")
    time.sleep(5)
    print("...done.")

    global ipc_client
    """Global Variable for the IPC Client"""
    ipc_client = IPC()
    ipc_client.connect()

    global server_proxy
    """Global Variable for the proxy server"""
    server_proxy = ipc_client.get_server_proxy()

def open_testselection():
    print("Please select a testcase or a set of tests to run.")
    print("[X] TEST #001...")

def setup_network():
    print("Current network settings:")
    x = input("Setup network? (y/n): ")
    if x.lower() == "y":
        print("Building network...")
    if x.lower() == "n":
        n = input("Edit network configuration? (y/n): ")
        if n.lower() == "y":
            print("//open text editor to edit config")
        else:
            print("return....")


def check_status():
    return_status = 1;
    if return_status == 1 :
        utilities.print_action("Status: connected")
    else:
        utilities.print("Status: not connected")
        exit()


def main(args = None):
    """Freifunk TestFramework Command Line Interface"""
    command = " "
    if args is None:
        args = sys.argv[1:]

    global utilities
    utilities = CLIUtil()
    utilities.print_header()
    connect_to_server() #--> remember to uncomment ipc shutdown
    check_status()

    #Argument Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--status", help = "returns status of Routers",
                        action = "store_true")
    parser.add_argument("-r", "--runtest", help = "runs selected test",
                        action = "store_true")
    parser.add_argument("--setup", help = "setup the network",
                        action = "store_true")
    args = parser.parse_args()



    if args.status:
        """return status of routers"""
        #routers = server_proxy.get_routers()
        routers = [("Router 4", "0.0.0.0", "ff:ff:ff:ff:ff:ff", "VLAN1", "mode"),
                   ("Router 2", "0.0.0.0", "ff:ff:ff:ff:ff:ff", "VLAN2blablabla", "mode"),
                   ("Router 1", "0.0.0.0", "ff:ff:ff:ff:ff:ff", "VLAN3", "mode"),
                   ("Router 3", "127.0.0.1", "ff:ff:ff:ff:ff:ff", "VLAN4", "mode")]
        utilities.print_status(routers)

    if args.runtest:
        """runs test selection menue"""
        open_testselection()

    if args.setup:
        """sets up the network"""
        setup_network()

    ipc_client.shutdown
    print("Exiting")

class DummyServer(ServerProxy):
    def start_test(self, router_id, test_id):
        pass

    def get_running_tests(self) -> []:
        pass

    def get_routers(self):
        routers = [["Router 4", "0.0.0.0", "ff:ff:ff:ff:ff:ff", "VLAN1", "mode"],
              ["Router 2", "0.0.0.0", "ff:ff:ff:ff:ff:ff", "VLAN2", "mode"],
              ["Router 1", "0.0.0.0", "ff:ff:ff:ff:ff:ff", "VLAN3", "mode"],
              ["Router 3", "0.0.0.0", "ff:ff:ff:ff:ff:ff", "VLAN4", "mode"]]
        return routers
        pass

    def get_reports(self) -> []:
        pass

    def get_tests(self) -> []:
        pass

    def get_firmwares(self) -> []:
        pass

if __name__ == "__main__":
    main()


