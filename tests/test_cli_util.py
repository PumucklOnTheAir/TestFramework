import unittest
from util.cli_util import CLIUtil


class MyTestCase(unittest.TestCase):
    def test_create_util(self):
        global cli_util
        cli_util = CLIUtil()
        assert isinstance(cli_util, CLIUtil)

if __name__ == '__main__':
    unittest.main()
