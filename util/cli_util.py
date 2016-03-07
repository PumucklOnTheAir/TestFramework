import logging
from unittest import TestResult


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
        for i in range(len(content)):
            if len(content[i]) != len(headers):
                logging.warning("Content and headers do not match")

            assert(len(content[i]) == len(headers))

        # generate list of column widths, compare with strings in header
        table = [headers]
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
            print("|" + "|".join(" {} ".format(str(x).ljust(width_list[i]))
                                 for i, x in enumerate(content[c])) + "|")
            if c == len(content) - 1:
                print("+" + "-".join("-{}-".format("".ljust(width_list[i], "-"))
                                     for i, x in enumerate(content[c])) + "+")
            else:
                print("|" + "+".join("-{}-".format("".ljust(width_list[i], "-"))
                                     for i, x in enumerate(content[c])) + "|")

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
    def print_list(content):
        """
        prints a simple list(table) sorted by the first row and formatted

        :param content: list of list (table)
        :return:
        """
        # generate list of row widths
        width_list = [[len(str(x)) for x in row] for row in content]
        width_list = list(map(max, zip(*width_list)))

        # sort content by the first row
        content.sort(key=lambda x: x[0])

        # print list
        line = "+" + "-".join("-{}-".format("-".ljust(width_list[i], "-"))
                              for i, x in enumerate(content[0])) + "+"
        print(line)
        for c in range(len(content)):
            print(" " + " ".join(" {} ".format(str(x).ljust(width_list[i]))
                                 for i, x in enumerate(content[c])))
        print(line)

    @staticmethod
    def print_router(router_list):
        """
        prints a detailed list of info on a router

        :param router_list: list of info on router
        :return:
        """
        print("------Detailed Router Info------")
        for elem in router_list:
            print("{:<15}{:<20}".format(str(elem[0]) + ":", str(elem[1])))

    @staticmethod
    def print_test_results(result_list: [(int, str, TestResult)]):
        """
        Prints a the TestResult list

        :param result_list:
        :return:
        """
        headers = ["Router ID", "Test", "(S|F|E)"]
        content = []
        print("------Testresults------")
        for result in result_list:
            content.append([str(result[0]), result[1], "(" + str(result[2].testsRun - len(result[2].failures) -
                                                                 len(result[2].errors)) +
                            "|" + str(len(result[2].failures)) +
                            "|" + str(len(result[2].errors)) + ")"])

        CLIUtil.print_dynamic_table(content, headers)


class OutputColors:
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    clear = '\033[0m'
    bold = '\033[1m'
