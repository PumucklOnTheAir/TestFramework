import unittest

from log.logger import Logger


class MyTestCase(unittest.TestCase):
    def test_something(self):

        l = Logger()
        l.info("Hello from l {0}".format(Logger()))

        l1 = Logger()
        l1.info("Hello from l1 {0}".format(Logger()))

        Logger().info("Hello from Logger() {0}".format(Logger()))
        Logger().debug("Debug from Logger() {0}".format(Logger()))

        self.assertEqual(True, l is l1 is Logger())


if __name__ == '__main__':
    unittest.main()
