import unittest
from log.logger import Logger


class MyTestCase(unittest.TestCase):

    def test_something(self):
        """
        Tests the logger and all log levels
        :return: Tests results
        """
        l = Logger()

        l.info("Hello from logger Nr. 1 with same instance as logger Nr. 2: {0}".format(Logger()))

        l1 = Logger()
        l1.info("Hello from logger Nr. 2 with same instance as logger Nr. 1: {0}".format(Logger()))

        Logger().info("Hello from Logger() {0}".format(Logger()))
        Logger().debug("Debug from Logger() {0}".format(Logger()))
        Logger().error("Error from Logger() {0}".format(Logger()))
        Logger().warning("Warning from Logger() {0}".format(Logger()))
        Logger().critical("Critical from Logger() {0}".format(Logger()))
        Logger().debug("Debug from level 2", 2)

        self.assertEqual(True, l is l1 is Logger())


if __name__ == '__main__':
    unittest.main()
