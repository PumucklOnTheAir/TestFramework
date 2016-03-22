import unittest
from server.server import Server
import os


class MyTestCase(unittest.TestCase):

    def test_clear_all(self):
        """

        :return:
        """
        Server.start()
        Server.delete_test_results()
        Server.stop()

    def test_run_test(self):
        """

        :return:
        """
        Server.start()
        os.system(self.path_cli + " start -s set_1 -a")
        Server.stop()
