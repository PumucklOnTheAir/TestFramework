from server.ipc import IPC
from server.serverproxy import ServerProxy
from server.router import Router
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
    """global variable for the proxy server"""
    server_proxy = ipc_client.get_server_proxy()


"""def get_running_tests():
    tests = server_proxy.get_running_tests()
    if tests == ():
        util.print_action("No tests running")
    else:
        print("\tCurrently running Tests:")
        for i in range(len(tests)):
            util.print_progress(tests[i][0], tests[i][1], tests[i][2])
"""


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


def get_tests_progress():
    tests = server_proxy.get_running_tests()
    working = True
    lines = 0
    if tests == ():
        util.print_action("No running tests")
    else:
        try:
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

        except KeyboardInterrupt:
            print("\n" * lines)
            util.print_warning("Interrupted by user")


def open_test_selection():
    tests = server_proxy.get_tests()
    print("\tPlease select a test case or a set of tests to run.")
    tests.sort(key=lambda x: x[0])
    for i in range(len(tests)):
        util.print_bullet("Test #" + "%(n)03d\t" % {"n": tests[i][0]} + tests[i][1])


def setup_network():
    print("Current network settings:")
    x = input("Setup network? (y/n): ")
    if x.lower() == "y":
        print("Building network...")
    if x.lower() == "n":
        print("Abort.")


def check_status():
    util.print_warning("This is your last warning!!")
    util.print_error("Something terrible has happened D:")


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
    parser.add_argument("-s", "--status", help="return status of Routers",
                        action="store_true")
    # parser.add_argument("-r", "--runtest", nargs=2, default=[0, 0], action="store",
                        # help="run selected test, -r [RouterID] [TestID]")
    parser.add_argument("-t", "--tests", help="return currently running tests",
                        action="store_true")
    parser.add_argument("--setup", help="setup the network",
                        action="store_true")
    parser.add_argument("-l", "--testlist", help="list all available tests",
                        action="store_true")
    args = parser.parse_args()

    if args.status:
        """return status of routers"""
        routers = server_proxy.get_routers()
        headers = ["VLAN Name", "VLAN ID", "IP", "WLan Modus", "MAC"]
        string_list = []
        for i in range(len(routers)):
            string_list.append([routers[i].vlan_name, routers[i].vlan_id,
                                routers[i].ip + "/" + str(routers[i].ip_mask), routers[i].wlan_mode,
                                routers[i].mac])
        util.print_status(string_list, headers)

    '''if args.runtest:
        """runs test selection menu"""
        open_test_selection()
        print(args.runtest)
        server_proxy.start_test(args.runtest[0], args.runtest[1])'''

    if args.tests:
        """return running tests"""
        get_tests_progress()

    if args.setup:
        """sets up the network"""
        setup_network()

    if args.testlist:
        """list all tests"""
        print("TODO: Testlist")

    util.print_action("Shutting down server...")
    ipc_server.shutdown()
    util.print_action("...done")
    util.print_action("Exiting")


class DummyServer(ServerProxy):
    def start_test(self, router_id, test_id):
        print("Test {1} auf Router {0} gestartet".format(router_id, test_id))
        pass

    def get_running_tests(self):
        tests = [["Router 1", 1, 20], ["Router 2", 2, 5], ["Router 3", 5, 50], ["Router 4", 10, 100]]
        return tests
        pass

    def get_routers(self):
        router1 = Router("VLAN5", 1, "0.0.0.0", 24, "usr", "pw")
        router2 = Router("VLAN11", 1, "0.0.0.0", 24, "usr", "pw")
        router3 = Router("VLAN3", 1, "0.0.0.0", 24, "usr", "pw")
        router4 = Router("VLAN22", 1, "0.0.0.0", 24, "usr", "pw")
        routers = [router1, router2, router3, router4]
        return routers
        pass

    def get_reports(self) -> []:
        pass

    def get_tests(self) -> []:
        tests = [[1, "Configuration Test"], [2, "Firmware Test"], [5, "Random Test"],
                 [17, "Mesh Test"], [136, "Gateway Test"], [3, "Some Other Test"]]
        return tests
        pass

    def get_firmwares(self) -> []:
        pass


if __name__ == "__main__":
    main()


