#!/usr/bin/env python3

from server.ipc import IPC
from util.cli_util import CLIUtil
import logging
import argparse
import sys
import subprocess


def connect_to_server():
    """
    Initiates connection to the IPC server by creating a client
    """

    global ipc_client
    ipc_client = IPC()
    ipc_client.connect()

    server_proxy = ipc_client.get_server_proxy()

    # register console for cli
    name = subprocess.getoutput('tty')
    server_proxy.register_tty(name)

    return server_proxy


def print_routers(routers):
    """
    Collects data for routers and sets headers for a table

    :param routers: list of routers
    :return:
    """

    # Headers for table
    headers = ["ID", "Router Model/Vers", "VLAN ID", "Mode", "IP", "MAC"]
    string_list = []

    # Collect info on routers
    for i in range(len(routers)):
        string_list.append([routers[i].id,
                            routers[i].model,
                            routers[i].vlan_iface_id,
                            routers[i].mode.name,
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
        logging.info("No such router found, check the list again")
    else:
        # Collect info on router [["header", info],...]
        router = router[0]
        info = [["ID", router.id],
                ["Model", router.model],
                ["MAC", router.mac],
                ["IP", router.ip + "/" + str(router.ip_mask)],
                ["VLan Name", router.vlan_iface_name],
                ["VLan ID", router.vlan_iface_id],
                ["Mode", router.mode.name],
                ["Username", router.usr_name],
                ["Password", router.usr_password],
                ["Firmware", router.firmware.name],
                ["Power Socket", router.power_socket],
                ["Node Name", router.public_name],
                ["Public Key", router.public_key]]

        # Info on Memory
        mem_list = [["Used", str(router.ram.used) + "/" + str(router.ram.total)],
                    ["Free", str(router.ram.free) + "/" + str(router.ram.total)],
                    ["Shared", router.ram.shared],
                    ["Buffers", router.ram.buffers]]

        # Info on all Interfaces on the router
        if_list_headers = ["ID", "Name", "MAC", "Status", "IP Addresses", "Wifi Info"]
        if_list = []

        for i in sorted(router.interfaces.values(), key=lambda if_id: if_id.id):
            wifi_info = ""
            if i.wifi_information:
                wifi_info = str(i.wifi_information.wdev) + ": " + str(i.wifi_information.ssid)
                wifi_info += "\tType: " + str(i.wifi_information.type.name)
                wifi_info += "\tCh: " + str(i.wifi_information.channel)
                wifi_info += "\tWidth: " + str(i.wifi_information.channel_width) + "MHz"
                wifi_info += "\tCenter: " + str(i.wifi_information.channel_center1) + "MHz"
            ip_list = i.ipaddress_lst.copy()
            # if more than 1 ip,
            if len(ip_list) > 1:
                ip = str(ip_list[0])
                del ip_list[0]
                li = [str(i.id), i.name, i.mac, i.status.name, ip, wifi_info]
                if_list.append(li)
                for ip in ip_list:
                    li = ["", "", "", "", ip, ""]
                    if_list.append(li)
            # only 1 ip in the ip list
            elif len(ip_list) == 1:
                li = [str(i.id), i.name, i.mac, i.status.name, ip_list[0], wifi_info]
                if_list.append(li)
            # no ip in list
            else:
                li = [str(i.id), i.name, i.mac, i.status.name, "", wifi_info]
                if_list.append(li)

        # Info on processes on the router
        proc_list_headers = ["PID", "User", "CPU", "MEM", "Command"]
        proc_list = []
        for p in router.cpu_processes:
            li = [p.pid, p.user, str(p.cpu) + "%", str(p.mem) + "%", p.command]
            proc_list.append(li)

        # Info on sockets on the router
        socket_list_headers = ["PID", "Protocol", "Local Address", "L. Port",
                               "Foreign Address", "F. Port", "Status", "Program"]
        socket_list = []
        for s in router.sockets:
            if not s.state:
                state = ""
            else:
                state = str(s.state.name)
            li = [s.pid, s.protocol.name, s.local_address, s.local_port, s.foreign_address, s.foreign_port,
                  state, s.program_name]
            socket_list.append(li)

        # Info on Bat Originators
        bat_list = []
        bat_list_headers = ["MAC", "Seen[s]", "Next Node", "Iface", "Alt. Nodes"]
        for b in router.bat_originators:
            next_hops = ""
            for hop in b.potential_next_hops:
                next_hops += hop + " "
            li = [b.mac, str(b.last_seen), b.next_hop, b.outgoing_iface, next_hops]
            bat_list.append(li)

        util.print_router(info, if_list_headers, if_list, proc_list_headers, proc_list,
                          socket_list_headers, socket_list, mem_list, bat_list_headers, bat_list)


def create_parsers():
    """
    Creates parser and subparsers for the command line

    :return: parser
    """

    # Argument Parsing
    parser = argparse.ArgumentParser(description="\tA program to test the firmware on Freifunk routers")
    subparsers = parser.add_subparsers(help="help for subcommands", dest="mode")

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
    parser_webconfig.add_argument("-w", "--wizard", action="store_true", default=False,
                                  help="start in Wizard Mode, if False start in Expert Mode")

    # subparser for update_info
    parser_update_info = subparsers.add_parser("update_info", help="Updates the router info")
    parser_update_info.add_argument("-r", "--routers", metavar="Router ID", type=int,
                                    default=[], action="store", help="List of routers", nargs="+")
    parser_update_info.add_argument("-a", "--all", action="store_true", default=False,
                                    help="Apply to all routers")

    # subparser for online
    parser_online = subparsers.add_parser("online", help="Ping routers to check IP")
    parser_online.add_argument("-r", "--routers", metavar="Router ID", type=int, default=[], action="store",
                               help="List of routers", nargs="+")
    parser_online.add_argument("-a", "--all", action="store_true", default=False, help="Apply to all routers")

    # subparser for power strip
    parser_power = subparsers.add_parser("power", help="Switch power on router on or off")
    parser_power.add_argument("-r", "--routers", metavar="Router ID", type=int,
                              default=[], action="store", help="List of routers", nargs="+")
    parser_power.add_argument("-a", "--all", action="store_true", default=False,
                              help="Apply to all routers")
    parser_power.add_argument("-on", "--on", action="store_true", default=False, help="turn on")
    parser_power.add_argument("-off", "--off", action="store_true", default=False, help="turn off")

    # subparser for test set
    parser_test_set = subparsers.add_parser("start", help="Start a test set")
    parser_test_set.add_argument("-r", "--routers", metavar="Router ID", type=int, default=[], action="store",
                                 help="", nargs="+")
    parser_test_set.add_argument("-a", "--all", action="store_true", default=False, help="Apply to all routers")
    parser_test_set.add_argument("-s", "--set", metavar="Test set", type=str, default=[], action="store",
                                 help="Name of set")
    parser_test_set.add_argument("-b", "--blocking", help="Blocks until finished", default=False,
                                 action="store_true")

    # subparser for test results
    parser_test_result = subparsers.add_parser("results", help="Manage the test results")
    parser_test_result.add_argument("-r", "--routers", metavar="Router ID", type=int, default=[], action="store",
                                    help="", nargs="+")
    parser_test_result.add_argument("-a", "--all", action="store_true", default=False, help="Apply to all routers")
    parser_test_result.add_argument("-rm", "--remove", action="store_true", default=False,
                                    help="Remove all results. Ignoring parameter -r.")

    # subparser for register keys
    parser_reg_key = subparsers.add_parser("register_key", help="Registers the key for the node")
    parser_reg_key.add_argument("-r", "--routers", metavar="Router ID", type=int,
                                default=[], action="store", help="List of routers", nargs="+")
    parser_reg_key.add_argument("-a", "--all", action="store_true", default=False,
                                help="Apply to all routers")

    return parser


def main():
    """
    Freifunk TestFramework Command Line Interface
    """

    # Parse Arguments
    parser = create_parsers()
    args = parser.parse_args()

    global util
    util = CLIUtil()
    # Isn't necessary
    # util.print_header()

    try:
        server_proxy = connect_to_server()
    except ConnectionError as e:
        logging.warning("Failed to establish connection: " + str(e))
        sys.exit(1)

    if args.mode == "status":
        """
        subparse: status
        """
        if args.all:
            # return status of all routers
            routers = server_proxy.get_routers()
            if not routers:
                logging.warning("No routers in network")
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
        toggle_wizard = args.wizard

        server_proxy.setup_web_configuration(args.routers, config_all, toggle_wizard)

    elif args.mode == "update_info":
        """
        subparse: update_info
        """
        update_all = args.all

        server_proxy.update_router_info(args.routers, update_all)

    elif args.mode == "online":
        """
        subparse: online
        """
        online_all = args.all
        server_proxy.router_online(args.routers, online_all)

    elif args.mode == "power":
        """
        subparse: power
        """
        switch_all = args.all
        on_or_off = True
        if args.on:
            on_or_off = True
        elif args.off:
            on_or_off = False
        server_proxy.control_switch(args.routers, switch_all, on_or_off)

    elif args.mode == "start":
        """
        subparse: start
        """
        if args.all:
            router_id = -1
        else:
            router_id = args.routers[0]
        set_name = args.set

        if args.blocking:
            wait = 5000  # seconds
        else:
            wait = -1  # don't wait

        server_proxy.start_test_set(router_id, set_name, wait)

    elif args.mode == "results":
        """
        subparse: results
        """

        if args.remove:
            removed = server_proxy.delete_test_results()
            print("Removed all " + str(removed) + " results.")
        else:
            if args.all:
                router_id = -1
            else:
                router_id = args.routers[0]
            util.print_test_results(server_proxy.get_test_results(router_id))

    elif args.mode == "register_key":
        """
        subparse: register key
        """
        register_all = args.all
        server_proxy.register_key(args.routers, register_all)

    else:
        logging.info("Check --help for help")


if __name__ == "__main__":
    main()
