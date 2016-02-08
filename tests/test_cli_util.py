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
                ["SSID", "none"],
                ["Firmware", "Firmware X"],
                ["Power Socket", "5"]]

        if_list = [["0", "Name", "00:00:00:00:00:00", "STATUS", "0.0.0.0, " +
                    "111.111.1.1, " + "222.222.222.222"],
                   ["1", "Name2", "00:00:00:00:00:00", "STATUS", "0.0.0.0, " +
                    "111.111.1.1, " + "222.222.222.222"]]

        cli_util.print_router(info, ["ID", "Name", "MAC", "Status", "IP Addresses"],
                              if_list, ["PID", "User", "CPU", "MEM", "Command"],
                              [["0", "User X", "CPU", "MEM",
                                "blablablablablablablablablalbalblalbalblabla"],
                               ["0", "User X", "CPU", "MEM",
                               "blablablablablablablablablalbalblalbalblabla"]])

    def test_status_all(self):
        headers = ["ID", "Router Model/Vers", "VLAN ID", "Router Name", "IP", "MAC"]
        content = [["0", "Model X", "21", "Freifunk", "0.0.0.0", "00:00:00:00:00:00"]]
        cli_util.print_dynamic_table(content, headers)
