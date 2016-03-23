import unittest
from server.server import Server
import os


class MyTestCase(unittest.TestCase):

    path_cli = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cli.py')

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
