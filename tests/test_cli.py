import unittest
import cli


class MyTestCase(unittest.TestCase):
    def test_create_cli(self):
        global cli
        cli = cli.CLI()

if __name__ == '__main__':
    unittest.main()
