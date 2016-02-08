from log.logger import Logger


class CLIUtil:
    """
    Command Line Interface Utilities
    Contains utilities and formatting for the command line interface
    """

    @staticmethod
    def print_dynamic_table(content, headers):
        """
        prints a dynamically formatted table
        :param content: list of lists of data
        :param headers: list of headers
        """

        # check for correct list lengths
        for i in content:
            if len(i) != len(headers):
                Logger().warning("Content and headers do not match")

            assert(len(i) == len(headers))

        # generate list of column widths, compare with strings in header
        table = [headers]
        for i in content:
            table.append(i)
        width_list = [[len(str(x)) for x in row] for row in table]
        width_list = list(map(max, zip(*width_list)))

        # print headers
        print("+" + "=".join("={}=".format("".ljust(width_list[i], "=")) for i, x in enumerate(content[0])) + "+")
        print("|" + "|".join(" {} ".format(str(x).ljust(width_list[i])) for i, x in enumerate(headers)) + "|")
        print("+" + "=".join("={}=".format("".ljust(width_list[i], "=")) for i, x in enumerate(content[0])) + "+")

        # print content
        for c in content:
            print("|" + "|".join(" {} ".format(str(x).ljust(width_list[i]))
                                 for i, x in enumerate(c)) + "|")
            if c == len(content) - 1:
                print("+" + "-".join("-{}-".format("".ljust(width_list[i], "-"))
                                     for i, x in enumerate(c)) + "+")
            else:
                print("|" + "+".join("-{}-".format("".ljust(width_list[i], "-"))
                                     for i, x in enumerate(c)) + "|")

    def print_status(self, routers, headers):
        """
        prints the status of all routers
        :param routers: list of routers
        :param headers: list of headers
        """

        # sort list of routers by first row
        routers.sort(key=lambda x: x[0])

        print("Routers in network: " + str(len(routers)))
        self.print_dynamic_table(routers, headers)

    @staticmethod
    def print_header():
        """
        prints header for the command line
        :return:
        """
        print("\v\t" + OutputColors.bold + "Freifunk Testframework\v" + OutputColors.clear)

    @staticmethod
    def return_progressbar(router, tid, percentage):
        """
        returns the visual progress of a test on a router
        :param router: router name
        :param tid: ID of test
        :param percentage: progress of test in percent
        :return: string with progress bar
        """
        progress = int(percentage / 2)
        return ("\t" + str(router) + ":   Test ID: " + str(tid) + "\t[" +
                "".join("{}".format("#") for _ in range(progress)) +
                "".join("{}".format(" ") for _ in range(50 - progress)) + "]\t" + str(percentage) + "%")

    @staticmethod
    def print_list(content, headers):
        """
        prints a simple list(table) sorted by the first row and formatted
        :param content: list of list (table)
        :param headers: list of headers for table, leave empty if not wanted
        :return:
        """
        # generate list of row widths
        width_list = content.copy()
        width_list.append(headers)
        width_list = [[len(str(x)) for x in row] for row in width_list]
        width_list = list(map(max, zip(*width_list)))

        # sort content by the first row
        content.sort(key=lambda x: x[0])

        line = "+" + "-".join("-{}-".format("-".ljust(width_list[i], "-"))
                              for i, x in enumerate(content[0])) + "+"

        # print headers only if wanted
        if len(headers) > 0:
            print(line)
            print(" " + " ".join(" {} ".format(str(x).ljust(width_list[i]))
                                 for i, x in enumerate(headers)))

        # print list
        print(line)
        for c in content:
            print(" " + " ".join(" {} ".format(str(x).ljust(width_list[i]))
                                 for i, x in enumerate(c)))
        print(line)

    def print_router(self, router_list, if_list_headers, if_list, proc_list_headers, proc_list):
        """
        prints a detailed list of info on a router
        :param router_list: list of info on router
        :param if_list_headers: headers for the interfaces
        :param if_list: list of interfaces
        :param proc_list_headers: headers for the CPU Process table
        :param proc_list: list of CPU processes running on router
        :return:
        """
        print(OutputColors.bold + "------Detailed Router Info------" + OutputColors.clear)
        for elem in router_list:
            print("{:<15}{:<20}".format(str(elem[0]) + ":", str(elem[1])))

        print(OutputColors.bold + "\v------Interfaces------" + OutputColors.clear)
        self.print_list(if_list, if_list_headers)

        print(OutputColors.bold + "\v------CPU Processes------" + OutputColors.clear)
        self.print_list(proc_list, proc_list_headers)


class OutputColors:
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    clear = '\033[0m'
    bold = '\033[1m'
