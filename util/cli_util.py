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

            assert len(content[i]) == len(headers)

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
    def print_list(content, headers, sort: bool, ind_line: bool, in_table_param: str):
        """
        prints a simple list(table) sorted by the first row and formatted

        :param content: list of list (table)
        :param headers: list of headers for table, leave empty if not wanted
        :param sort: sort the list by first column, or not
        :param ind_line: is there content to be inserted as a new line
        :param in_table_param: which field contains the indent
        :return:
        """
        # generate list of column widths
        width_list = content.copy()
        width_list.append(headers)
        width_list = [[len(str(x)) for x in row] for row in width_list]
        width_list = list(map(max, zip(*width_list)))

        # line in table remove column
        pos = -1
        if ind_line:
            pos = headers.index(in_table_param)
            width_list[pos] = 0

        # sort content by the first row
        if sort:
            content.sort(key=lambda x: x[0])

        # print headers only if wanted
        if len(headers) > 0:
            print(" " + " ".join(" {} ".format(str(x).ljust(width_list[i]))
                                 for i, x in enumerate(headers) if i != pos) + "\n")

        # print list
        for c in content:
            print(" " + " ".join(" {} ".format(str(x).ljust(width_list[i]))
                                 for i, x in enumerate(c) if i != pos))
            if ind_line:
                if c[pos]:
                    print("\t" + c[pos])

    def print_router(self, router_list, if_list_headers, if_list, proc_list_headers, proc_list,
                     socket_list_headers, socket_list, mem_list, bat_list_headers, bat_list):
        """
        prints a detailed list of info on a router

        :param router_list: list of info on router
        :param if_list_headers: headers for the interfaces
        :param if_list: list of interfaces
        :param proc_list_headers: headers for the CPU Process table
        :param proc_list: list of CPU processes running on router
        :param socket_list_headers: header for the Socket table
        :param socket_list: list of the Sockets
        :param mem_list: list of info on memory
        :param bat_list_headers: headers for Bat Originators
        :param bat_list: list of Bat Originators
        :return:
        """
        print(OutputColors.bold + "------Detailed Router Info------" + OutputColors.clear)
        for elem in router_list:
            print("{:<15}{:<20}".format(str(elem[0]) + ":", str(elem[1])))

        print(OutputColors.bold + "\v------Memory------" + OutputColors.clear)
        for elem in mem_list:
            print("{:<15}{:<20}".format(str(elem[0]) + ":", str(elem[1])))

        print(OutputColors.bold + "\v------Interfaces------" + OutputColors.clear)
        self.print_list(if_list, if_list_headers, False, True, "Wifi Info")

        print(OutputColors.bold + "\v------CPU Processes------" + OutputColors.clear)
        self.print_list(proc_list, proc_list_headers, True, False, "")

        print(OutputColors.bold + "\v-------Sockets-------" + OutputColors.clear)
        self.print_list(socket_list, socket_list_headers, True, False, "")

        print(OutputColors.bold + "\v-----BatOriginators-----" + OutputColors.clear)
        self.print_list(bat_list, bat_list_headers, False, False, "")

    @staticmethod
    def print_test_sets(test_set_dict):
        """
        Prints a Test_Sets dict

        :param test_set_dict:
        """
        max_shown_tests = 4
        headers = ["Set ID", "Test"]
        content = []
        print("------TestSets------")
        for i in range(0, len(test_set_dict)):
            test_set = test_set_dict["set_"+str(i)]
            tests = ""
            for j, test in enumerate(test_set):
                if j > max_shown_tests:
                    tests += " ..."
                    break
                tests += test + " "
            content.append([str(i), tests])

        CLIUtil.print_dynamic_table(content, headers)

    @staticmethod
    def print_test_set(test_set_dict, test_set_id: int):
        """
        Prints the tests of one Test_Set.

        :param test_set_dict: Dictionary of Test-Sets
        :param test_set_id: The id of the chosen Test-Set
        """
        test_set = test_set_dict["set_" + str(test_set_id)]
        print("------Test of Test-Set" + str(test_set_id) + " ------")
        for test in test_set:
            print(test)

    @staticmethod
    def print_test_results(result_list: [(int, str, TestResult)]):
        """
        Prints a TestResult list

        :param result_list:
        :return:
        """
        headers = ["Index", "Router ID", "Test", "(S|F|E)"]
        content = []
        print("------Testresults------")
        if not result_list:
            print("No Tests to show")
        else:
            for i, result in enumerate(result_list):
                content.append([str(i), str(result[0]), result[1],
                                "(" + str(result[2].testsRun - len(result[2].failures) -
                                          len(result[2].errors)) +
                                "|" + str(len(result[2].failures)) +
                                "|" + str(len(result[2].errors)) + ")"])

            CLIUtil.print_dynamic_table(content, headers)

    @staticmethod
    def print_result_errors(err: TestResult):
        """
        Prints the error a Test produced

        :param err: unittest TestResult
        """
        if not err.errors:
            print("No Errors produced by this Test")
        else:
            print("\v" + "=" * 35)
            print("The following Errors were produced:")
            print("=" * 35)
            for e in err.errors:
                # print traceback of Errors
                print(e[1])
                print("-" * 35)

    @staticmethod
    def print_result_failures(fail: TestResult):
        """
        Prints the failures a Test produced

        :param fail: unittest TestResult
        """
        if not fail.failures:
            print("No Failures produced by this Test")
        else:
            print("\v" + "=" * 35)
            print("The following Failures occurred:")
            print("Total Failures: [" + str(len(fail.failures)) + "]")
            print("=" * 35)
            for f in fail.failures:
                # print traceback of Failures
                print(f[0])
                print(f[1])
                print("-" * 35)


class OutputColors:
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    clear = '\033[0m'
    bold = '\033[1m'
