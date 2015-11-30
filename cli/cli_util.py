
class CLIUtil:
    """Command Line Interface Utilities
    Contains utilities and formatting for the command line interface
    """

    def print_dynamic_table(self, content, headers):
        """prints a dynamically formatted table
        :param content: list of lists of data
        :param headers: list of headers
        """

        # Generate list of column widths
        width_list = [[len(str(x)) for x in row] for row in content]
        width_list = list(map(max, zip(*width_list)))

        # print headers
        print("+" + "=".join("={}=".format("".ljust(width_list[i], "=")) for i, x in enumerate(content[0])) + "+")
        print("|" + "|".join(" {} ".format(str(x).ljust(width_list[i])) for i, x in enumerate(headers)) + "|")
        print("+" + "=".join("={}=".format("".ljust(width_list[i], "=")) for i, x in enumerate(content[0])) + "+")

        # print content
        for c in range(len(content)):
            print("|" + "|".join(" {} ".format(str(x).ljust(width_list[i])) for i, x in enumerate(content[c])) + "|")
            if c == len(content) - 1:
                print("+" + "-".join("-{}-".format("".ljust(width_list[i], "-")) for i, x in enumerate(content[c])) + "+")
            else:
                print("|" + "+".join("-{}-".format("".ljust(width_list[i], "-")) for i, x in enumerate(content[c])) + "|")

    def print_status(self, routers):
        """Gibt Status der Router aus"""

        # Liste der Router nach Name sortieren
        routers.sort(key = lambda x : x[0])
        headers = ("Name", "IP", "MAC", "VLAN", "Mode")
        self.print_action("routers in network: " + str(len(routers)))
        self.print_dynamic_table(routers, headers)

    def print_action(self, message):
        print("[+]" + message)

    def print_warning(self, message):
        print("\nWarning: " +  message)

    def print_error(self, message):
        print("\nERROR: " + message)

    def print_bullet(self, message):
        print("(*) " + message)

    def print_header(self):
        print("\v\tFreifunk Testframework\v")

    def print_progress(self, router, tid, percentage):
        progress = int(percentage / 2)
        print("\t" + str(router) + ":  Test ID: " + str(tid) + "\t[" + "".join("{}".format("#") for i in range(progress)) +
              "".join("{}".format(" ") for j in range(50 - progress)) + "]\t" + str(percentage) + "%")

    def return_progressbar(self, router,  tid, percentage):
        progress = int(percentage / 2)
        return ("\t" + str(router) + ":   Test ID: " + str(tid) + "\t[" + "".join("{}".format("#") for i in range(progress)) +
               "".join("{}".format(" ") for j in range(50 - progress)) + "]\t" + str(percentage) + "%")
