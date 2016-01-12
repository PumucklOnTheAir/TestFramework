from server.ipc import IPC
from cli.cli_util import CLIUtil
from log.logger import Logger
import argparse
import time
import random


def connect_to_server():
    """ Initiates connection to the IPC server by creating a client
    """

    if verbose:
        Logger().info("Setting up IPC client")

    global ipc_client
    """Global Variable for the IPC Client"""
    ipc_client = IPC()
    ipc_client.connect()

    # Wait for connection
    time.sleep(1)

    if verbose:
        Logger().info("Client succesfully setup")

    global server_proxy
    """global variable for the proxy server"""
    server_proxy = ipc_client.get_server_proxy()


def print_routers(routers):
    headers = ["ID", "Router Model/Vers", "VLAN ID", "Router Name", "IP", "MAC"]
    string_list = []
    for i in range(len(routers)):
        string_list.append([routers[i].id,
                            routers[i].model,
                            routers[i].vlan_iface_id,
                            routers[i].wlan_mode,
                            routers[i].ip + "/" + str(routers[i].ip_mask),
                            routers[i].mac])
    util.print_status(string_list, headers)


def print_router_info(router_list, rid):
    router = [elem for elem in router_list if str(elem.id) == str(rid)]
    if not router:
        Logger().info("No such router found, check the list again")
    else:
        router = router[0]
        info = [["ID", router.id]
                ["Model", router.model],
                ["MAC", router.mac],
                ["IP", router.ip + "/" + str(router.ip_mask)],
                ["VLan Name", router.vlan_iface_name],
                ["VLan ID", router.vlan_iface_id],
                ["WLAN Modus", router.wlan_mode],
                ["username", router.usr_name],
                ["password", router.usr_password],
                ["SSID", router.ssid],
                ["Firmware", router.firmware.name]]

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
            Logger().info("No running tests")
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
        Logger().info("Interrupted")


def get_tests_progress():
    tests = server_proxy.get_running_tests()
    # initialize variables
    working = True
    lines = 0
    i = 0

    # no tests returned
    if not tests:
        Logger().info("No running tests")
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
                    Logger().info("All tests completed")

        except KeyboardInterrupt:
            print("\n" * lines)
            Logger().info("Interrupted by user")


def list_all_tests():
    tests = server_proxy.get_tests()

    if not tests:
        Logger().info("No tests found")
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
    parser_status.add_argument("-a", "--all", help="Return status of all routers in network",
                               action="store_true")
    parser_status.add_argument("-r", "--router", help="Return detailed info on router", nargs=1,
                               action="store", metavar="Router ID")
    parser_status.add_argument("-t", "--test", help="Return currently running tests", action="store_true")
    parser_status.add_argument("-l", "--list", help="List all available tests", action="store_true")

    # subparser for actions
    parser_action = subparsers.add_parser("run", help="Execute different actions on the server")
    parser_action.add_argument("-vid", "--vlanid", metavar="VLan ID", type=int,
                               default=0, action="store",
                               help="Runs selected test on")
    parser_action.add_argument("-tid", "--testid", metavar="Test ID", type=int,
                               default=0, action="store")

    # subparser for sysupgrade
    parser_upgrade = subparsers.add_parser("sysupgrade", help="Upgrades the routers")
    parser_upgrade.add_argument("-r", "--routers", metavar="Router ID", type=int,
                                default=[], action="store", help="List of routers to be upgraded", nargs="+")
    parser_upgrade.add_argument("-a", "--all", action="store_true", default=False,
                                help="Apply to all routers")
    parser_upgrade.add_argument("-n", "--n", action="store_true", default=False,
                                help="Do not save existing configuration")

    # subparser for sysupdate
    parser_update = subparsers.add_parser("sysupdate", help="Fetches the updates for the routers")
    parser_update.add_argument("-r", "--routers", metavar="Router ID", type=int,
                               default=[], action="store", help="List of routers to be updated", nargs="+")
    parser_update.add_argument("-a", "--all", action="store_true", default=False,
                               help="Apply to all routers")

    # subparser for reboot
    parser_reboot = subparsers.add_parser("reboot", help="Reboots one or multiple routers")
    parser_reboot.add_argument("-r", "--routers", metavar="Router ID", type=int,
                               default=[], action="store", help="List of routers to be rebooted", nargs="+")
    parser_reboot.add_argument("-a", "--all", action="store_true", default=False,
                               help="Apply to all routers")
    parser_reboot.add_argument("-c", "--config", action="store_true", default=False,
                               help="Reboot to Configuration Mode")

    # subparser for webconfig
    parser_webconfig = subparsers.add_parser("webconfig", help="Sets up the web configuration")
    parser_webconfig.add_argument("-r", "--routers", metavar="Router ID", type=int,
                                  default=[], action="store", help="List of routers to be configured", nargs="+")
    parser_webconfig.add_argument("-a", "--all", action="store_true", default=False,
                                  help="Apply to all routers")

    args = parser.parse_args()

    global verbose
    verbose = args.verbose

    global util
    util = CLIUtil()
    util.print_header()
    connect_to_server()

    if verbose:
        Logger().info("Mode set to verbose")

    if args.mode == "status":
        if args.all:
            """return status of routers"""
            routers = server_proxy.get_routers()
            if not routers:
                Logger().warning("No routers in network")
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
            Logger().info("Please specify. See status -h")
    elif args.mode == "run":
        Logger().info("Run run run")
    elif args.mode == "sysupgrade":
        if args.all:
            server_proxy.sysupgrade_firmware([], True, args.n)
        else:
            server_proxy.sysupgrade_firmware(args.routers, False, args.n)
    elif args.mode == "sysupdate":
        if args.all:
            server_proxy.sysupdate_firmware([], True)
        else:
            server_proxy.sysupdate_firmware(args.routers, False)
    elif args.mode == "reboot":
        if args.all:
            if args.config:
                server_proxy.reboot_router([], True, True)
            else:
                server_proxy.reboot_router([], True, False)
        elif args.config:
            server_proxy.reboot_router(args.routers, False, True)
        else:
            server_proxy.reboot_router(args.routers, False, False)
    elif args.mode == "webconfig":
        if args.all:
            server_proxy.setup_web_configuration([], True)
        else:
            server_proxy.setup_web_configuration(args.routers, False)
    else:
        Logger().info("Check -h for help")


if __name__ == "__main__":
    main()
