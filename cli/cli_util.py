
class CLIUtil:
    """Command Line Interface Utilities
    Contains utilities and formatting for the command line interface
    """

    @staticmethod
    def print_dynamic_table(content, headers):
        """prints a dynamically formatted table
        :param content: list of lists of data
        :param headers: list of headers
        """

        # check for correct list lengths
        for i in range(len(content)):
            assert(len(content[i]) == len(headers))

        # generate list of column widths, compare with strings in header
        table = []
        table.append(headers)
        for i in range(len(content)):
            table.append(content[i])
        width_list = [[len(str(x)) for x in row] for row in table]
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

    def print_status(self, routers, headers):
        """Gibt Status der Router aus
        :param routers list of routers
        :param headers list of headers
        """

        # Liste der Router nach Name sortieren
        routers.sort(key=lambda x: x[0])
        self.print_action("routers in network: " + str(len(routers)))
        self.print_dynamic_table(routers, headers)

    @staticmethod
    def print_action(message):
        print("[+]" + message)

    @staticmethod
    def print_warning(message):
        print(OutputColors.yellow + "Warning: " + message + OutputColors.clear)

    @staticmethod
    def print_error(message):
        print(OutputColors.red + "\nERROR: " + message + OutputColors.clear)

    @staticmethod
    def print_bullet(message):
        print("(*) " + message)

    @staticmethod
    def print_header():
        print("\v\t" + OutputColors.bold + "Freifunk Testframework\v" + OutputColors.clear)

    @staticmethod
    def print_progress(router, tid, percentage):
        progress = int(percentage / 2)
        print("\t" + str(router) + ":  Test ID: " + str(tid) + "\t[" + "".join("{}".format("#") for i in range(progress)) +
              "".join("{}".format(" ") for j in range(50 - progress)) + "]\t" + str(percentage) + "%")

    @staticmethod
    def return_progressbar(router,  tid, percentage):
        progress = int(percentage / 2)
        return ("\t" + str(router) + ":   Test ID: " + str(tid) + "\t[" + "".join("{}".format("#") for i in range(progress)) +
                "".join("{}".format(" ") for j in range(50 - progress)) + "]\t" + str(percentage) + "%")


class OutputColors:
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    clear = '\033[0m'
    bold = '\033[1m'
