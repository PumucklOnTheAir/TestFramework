from server.ipc import IPC
# from server.serverproxy import ServerProxy
from server.server import Server
from cli.cli_util import CLIUtil
import argparse
import time
import random


def connect_to_server():
    """ Initiates connection to the IPC server by creating a client
    """

    Server.start(True, "", False)
    if verbose:
        util.print_action("Setting up client...")
    time.sleep(1)

    # util.print_error("Direkt vom server: " + str(len(Server.get_routers())))

    global ipc_client
    """Global Variable for the IPC Client"""
    ipc_client = IPC()
    ipc_client.connect()

    if verbose:
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
    # initialize variables
    working = True
    lines = 0
    i = 0

    # no tests returned
    if not tests:
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


def list_all_tests():
    tests = server_proxy.get_tests()

    if not tests:
        util.print_warning("No tests found")
    else:
        print("\tList of all Tests in Framework")
        util.print_list(tests)
    dummy_tests = [[1, "Configuration Test"], [2, "Dummy Test"],
                   [355, "Gateway Test"], [15, "Some other test"]]
    util.print_list(dummy_tests)


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

    # Argument Parsing
    parser = argparse.ArgumentParser(description="\tA program to test the firmware on Freifunk routers")
    subparsers = parser.add_subparsers(help="help for subcommands", dest="mode")

    # Verbose mode
    parser.add_argument("-v", "--verbose", help="returns results in verbose mode",
                        action="store_true")

    # subparser for status requests
    parser_status = subparsers.add_parser("status", help="Show status of routers, network or tests")
    parser_status.add_argument("-a", "--all_routers", help="return status of all routers in network",
                               action="store_true")
    parser_status.add_argument("-r", "--router", help="return detailed info on router", nargs=1,
                               action="store", metavar="Router ID")
    parser_status.add_argument("-t", "--test", help="return currently running tests", action="store_true")
    parser_status.add_argument("-l", "--list", help="list all available tests", action="store_true")

    # subparser for actions
    parser_action = subparsers.add_parser("run", help="Execute different actions on the server")
    parser_action.add_argument("-vid", "--vlanid", metavar="VLan ID", type=int,
                               default=0, action="store",
                               help="run selected test, -r [RouterID] [TestID]")
    parser_action.add_argument("-tid", "--testid", metavar="Test ID", type=int,
                               default=0, action="store")

    # subparser for setup
    parser_setup = subparsers.add_parser("setup", help="Setup the VLans")
    parser_setup.add_argument("--setup", help="setup the network", action="store_true")

    args = parser.parse_args()

    global verbose
    verbose = args.verbose

    global util
    util = CLIUtil()
    util.print_header()
    connect_to_server()  # --> remember to uncomment ipc shutdown

    if verbose:
        util.print_error("VERBOSE!!!!!!")

    if args.mode == "status":
        if args.all_routers:
            """return status of routers"""
            routers = Server.get_routers()
            if verbose:
                util.print_warning("Router vom Server direkt: " + str(len(routers)))
            if not routers:
                util.print_bullet("No routers in network")
            else:
                headers = ["Router ID", "VLAN Name", "VLAN ID", "IP", "WLan Modus", "MAC", "SSID", "User"]
                string_list = []
                for i in range(len(routers)):
                    string_list.append([str(routers[i].get_id()),
                                       routers[i].vlan_iface_name,
                                       routers[i].vlan_iface_id,
                                       routers[i].ip + "/" + str(routers[i].ip_mask),
                                       routers[i].wlan_mode,
                                       routers[i].mac,
                                       routers[i].ssid,
                                       routers[i].usr_name])
                util.print_status(string_list, headers)
        elif args.router:
            # routers = Server.get_routers()
            # router = routers.sort()
            print("Detailed Info on Router here....")
        elif args.test:
            get_tests_progress()
        elif args.list:
            list_all_tests()
        else:
            print("Please specify. See status -h")
    elif args.mode == "run":
        print("Run run run")
    elif args.mode == "setup":
        print("setup setup setup")

    if verbose:
        util.print_action("Shutting down server...")
    Server.stop()
    if verbose:
        util.print_action("...done")
        util.print_action("Exiting")

if __name__ == "__main__":
    main()
