import unittest
from util.cli_util import CLIUtil


class MyTestCase(unittest.TestCase):
    def test_create_util(self):
        global cli_util
        cli_util = CLIUtil()
        assert isinstance(cli_util, CLIUtil)

    def test_output_detailed(self):
        info = [["ID", "0"],
                ["Model", "Modell X"],
                ["MAC", "00:00:00:00:00:00"],
                ["IP", "0.0.0.0" + "/" + "24"],
                ["VLan Name", "Vlan0"],
                ["VLan ID", "0"],
                ["WLAN Modus", "Mode.unknown"],
                ["username", "admin"],
                ["password", "admin"],
                ["Firmware", "Firmware X"],
                ["Power Socket", "5"],
                ["Node Name", "Node X"],
                ["Public Key", "Keykeykey"]]

        if_list = [["0", "Name", "00:00:00:00:00:00", "STATUS", "0.0.0.0, " +
                    "111.111.1.1, " + "222.222.222.222"],
                   ["1", "Name2", "00:00:00:00:00:00", "STATUS", "0.0.0.0, " +
                    "111.111.1.1, " + "222.222.222.222"]]
        if_list_headers = ["ID", "Name", "MAC", "Status", "IP Addresses"]

        mem_list = [["Used", "3/5"],
                    ["Free", "2/5"],
                    ["Shared", "5"],
                    ["Buffers", "5"]]
        proc_list_headers = ["Proc"]
        proc_list = ["Process1"]
        socket_list_headers = ["Socket"]
        socket_list = ["Socket1"]
        bat_list_headers = ["Bat Originator"]
        bat_list = ["List Bat Originator"]

        cli_util.print_router(info, if_list_headers, if_list, proc_list_headers, proc_list,
                              socket_list_headers, socket_list, mem_list, bat_list_headers, bat_list)

    def test_status_all(self):
        headers = ["ID", "Router Model/Vers", "VLAN ID", "Router Name", "IP", "MAC"]
        content = [["0", "Model X", "21", "Freifunk", "0.0.0.0", "00:00:00:00:00:00"]]
        cli_util.print_dynamic_table(content, headers)
