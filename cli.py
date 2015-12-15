from server.ipc import IPC
from cli.cli_util import CLIUtil
import argparse
import time
import random


def connect_to_server():
    """ Initiates connection to the IPC server by creating a client
    """

    if verbose:
        util.print_action("Setting up client...")

    global ipc_client
    """Global Variable for the IPC Client"""
    ipc_client = IPC()
    ipc_client.connect()

    # Wait for connection
    time.sleep(1)

    if verbose:
        util.print_action("...done.")

    global server_proxy
    """global variable for the proxy server"""
    server_proxy = ipc_client.get_server_proxy()


def print_routers(routers):
    headers = ["Router Model/Vers", "VLAN ID", "VLAN Name", "Router Name", "IP", "MAC"]
    string_list = []
    for i in range(len(routers)):
        string_list.append([routers[i].model,
                            routers[i].vlan_iface_id,
                            routers[i].vlan_iface_name,
                            routers[i].wlan_mode,
                            routers[i].ip + "/" + str(routers[i].ip_mask),
                            routers[i].mac])
    util.print_status(string_list, headers)


def print_router_info(router_list, rid):
    router = [elem for elem in router_list if str(elem.vlan_iface_id) == str(rid)]
    if not router:
        util.print_action("No such router found, check the list again")
    else:
        router = router[0]
        info = [["Model", router.model],
                ["MAC", router.mac],
                ["IP", router.ip + "/" + str(router.ip_mask)],
                ["VLan Name", router.vlan_iface_name],
                ["VLan ID", router.vlan_iface_id],
                ["WLAN Modus", router.wlan_mode],
                ["username", router.usr_name],
                ["password", router.usr_password],
                ["SSID", router.ssid]]

        util.print_router(info)


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
    connect_to_server()

    if verbose:
        util.print_bullet("Mode set to verbose")

    if args.mode == "status":
        if args.all_routers:
            """return status of routers"""
            routers = server_proxy.get_routers()
            if not routers:
                util.print_bullet("No routers in network")
            else:
                print_routers(routers)

        elif args.router:
            routers = server_proxy.get_routers()
            print_router_info(routers, args.router[0])
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


if __name__ == "__main__":
    main()
