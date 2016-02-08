#!/usr/bin/env python3

from server.ipc import IPC
from util.cli_util import CLIUtil
from log.logger import Logger
import argparse
import time
import sys


def connect_to_server():
    """
    Initiates connection to the IPC server by creating a client
    """

    if verbose:
        Logger().info("Setting up IPC client")

    global ipc_client
    ipc_client = IPC()
    ipc_client.connect()

    # Wait for connection
    time.sleep(1)

    if verbose:
        Logger().info("Client successfully connected")

    server_proxy = ipc_client.get_server_proxy()
    return server_proxy


def print_routers(routers):
    """
    Collects data for routers and sets headers for a table

    :param routers: list of routers
    :return:
    """

    # Headers for table
    headers = ["ID", "Router Model/Vers", "VLAN ID", "Router Name", "IP", "MAC"]
    string_list = []

    # Collect info on routers
    for i in range(len(routers)):
        string_list.append([routers[i].id,
                            routers[i].model,
                            routers[i].vlan_iface_id,
                            routers[i].wlan_mode,
                            routers[i].ip + "/" + str(routers[i].ip_mask),
                            routers[i].mac])

    util.print_status(string_list, headers)


def print_router_info(router_list, rid):
    """
    Prints information on a single router

    :param router_list: list of all routers
    :param rid: ID of router to be printed
    :return:
    """
    router = [elem for elem in router_list if str(elem.id) == str(rid)]
    if not router:
        Logger().info("No such router found, check the list again")
    else:
        # Collect info on router [["header", info],...]
        router = router[0]
        info = [["ID", router.id],
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


def create_parsers():
    """
    Creates parser and subparsers for the command line

    :return: parser
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
                               type=int, action="store", metavar="Router ID")

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

    # subparser for connect
    parser_connect = subparsers.add_parser("connect", help="")
    parser_connect.add_argument("-r", "--routers", metavar="Router ID", type=int,
                                default=[], action="store", help="List of routers", nargs="+")
    parser_connect.add_argument("-a", "--all", action="store_true", default=False,
                                help="Apply to all routers")

    return parser


def main():
    """
    Freifunk TestFramework Command Line Interface
    """

    # Parse Arguments
    parser = create_parsers()
    args = parser.parse_args()

    global verbose
    verbose = args.verbose

    global util
    util = CLIUtil()
    util.print_header()

    try:
        server_proxy = connect_to_server()
    except ConnectionError as e:
        Logger().warning("Failed to establish connection: " + str(e))
        Logger().info("Exiting")
        sys.exit(1)

    if verbose:
        Logger().info("Mode set to verbose")

    if args.mode == "status":
        """
        subparse: status
        """
        if args.all:
            # return status of all routers
            routers = server_proxy.get_routers()
            if not routers:
                Logger().warning("No routers in network")
            else:
                print_routers(routers)

        elif args.router:
            routers = server_proxy.get_routers()
            print_router_info(routers, args.router[0])
        else:
            parser.print_help()
    elif args.mode == "sysupgrade":
        """
        subparse: sysupgrade
        """
        upgrade_all = args.all
        not_saving_config = args.n

        server_proxy.sysupgrade_firmware(args.routers, upgrade_all, not_saving_config)

    elif args.mode == "sysupdate":
        """
        subparse: sysupdate
        """
        update_all = args.all

        server_proxy.sysupdate_firmware(args.routers, update_all)

    elif args.mode == "reboot":
        """
        subparse: reboot
        """
        config_mode = args.config
        reboot_all = args.all

        server_proxy.reboot_router(args.routers, reboot_all, config_mode)

    elif args.mode == "webconfig":
        """
        subparse: webconfig
        """
        config_all = args.all

        server_proxy.setup_web_configuration(args.routers, config_all)

    elif args.mode == "connect":
        """
        subparse: connect
        """
        connect_all = args.all
        server_proxy.router_online(args.routers, connect_all)

    else:
        Logger().info("Check --help for help")


if __name__ == "__main__":
    main()
