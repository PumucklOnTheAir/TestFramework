from server.ipc import IPC
from server.serverproxy import ServerProxy
from cli.cli_util import CLIUtil
import argparse
import time
import random


def connect_to_server():
    """ Initiates connection to the IPC server by creating a client
    """

    dummy_runtime_server = DummyServer

    global ipc_server
    ipc_server = IPC()
    try:
        ipc_server.start_ipc_server(dummy_runtime_server)
    except:
        print("couldn't start server")

    util.print_action("Setting up client...")
    time.sleep(1)

    global ipc_client
    """Global Variable for the IPC Client"""
    ipc_client = IPC()
    ipc_client.connect()

    util.print_action("...done.")

    global server_proxy
    """Global Variable for the proxy server"""
    server_proxy = ipc_client.get_server_proxy()


def get_running_tests():
    tests = server_proxy.get_running_tests()
    if tests == ():
        util.print_action("No tests running")
    else:
        print("\tCurrently running Tests:")
        for i in range(len(tests)):
            util.print_progress(tests[i][0], tests[i][1])


def update_running_test(test):
    update = test
    if update[2] < 100:
        update[2] += 1
    return update


def get_test_progress():
    try:
        tests = server_proxy.get_running_tests()
        if tests == ():
            util.print_action("No running tests")
        else:
            print("\tCurrently running Test: " + str(tests[0][0]))
            test = tests[1]
            while test[1] <= 100:
                print(util.return_progressbar(test[0], test[1], test[2]), end="\r")
                test = update_running_test(test)
                t = random.random()
                time.sleep(t)
            print("\n")

    except KeyboardInterrupt:
        util.print_warning("Interrupted")


def tests_progress():
    tests = server_proxy.get_running_tests()
    working = True
    if tests == ():
        util.print_action("No running tests")
    else:
        while working:
            time.sleep(0.75)
            working = False
            print("\tCurrently running tests: ")
            for i in range(len(tests)):
                test = tests[i]
                test = update_running_test(test)
                print(util.return_progressbar(test[0], test[1], test[2]))
                if test[2] < 100:
                    working = True
            lines = i + 3
            # go back to first line
            if working:
                print("\033[" + str(lines) + "A")
            else:
                util.print_action("All tests completed")


def open_test_selection():
    server_proxy.get_running_tests()
    tests = [1, 2, 3, 4, 5, 6, 7, 8]
    print("\tPlease select a test case or a set of tests to run.")
    for i in range(len(tests)):
        util.print_bullet("Test #" + "%(n)03d" % {"n": tests[i]})
    util.print_action("TODO")


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
    return_status = 1
    if return_status == 1:
        util.print_action("Status: connected")
    else:
        util.print_action("Status: not connected")
        exit()


def main():
    """Freifunk TestFramework Command Line Interface
    """

    global util
    util = CLIUtil()
    util.print_header()
    connect_to_server()  # --> remember to uncomment ipc shutdown
    check_status()

    # Argument Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--status", help="returns status of Routers",
                        action="store_true")
    parser.add_argument("-r", "--runtest", help="runs selected test",
                        action="store_true")
    parser.add_argument("-t", "--tests", help="returns currently running tests",
                        action="store_true")
    parser.add_argument("--setup", help="setup the network",
                        action="store_true")
    parser.add_argument("-st", "--singletest", help="view progress of single test",
                        action="store_true")
    parser.add_argument("-l", "--testlist", help="view progress of all tests",
                        action="store_true")
    args = parser.parse_args()

    if args.status:
        """return status of routers"""
        routers = server_proxy.get_routers()
        util.print_status(routers)

    if args.runtest:
        """runs test selection menu"""
        open_test_selection()

    if args.tests:
        """return running tests"""
        get_running_tests()

    if args.setup:
        """sets up the network"""
        setup_network()

    if args.singletest:
        """view single test progress"""
        get_test_progress()

    if args.testlist:
        """view progress of all tests"""
        tests_progress()

    util.print_action("Shutting down server...")
    ipc_server.shutdown()
    util.print_action("...done")
    util.print_action("Exiting")


class DummyServer(ServerProxy):
    def start_test(self, router_id, test_id):
        pass

    def get_running_tests(self):
        tests = [["Router 1", 1, 98], ["Router 2", 2, 5], ["Router 3", 5, 50], ["Router 4", 10, 100]]
        return tests
        pass

    def get_routers(self):
        routers = [["Router 4", "0.0.0.0", "ff:ff:ff:ff:ff:ff", "VLAN1", 5],
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


