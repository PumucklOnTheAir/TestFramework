import unittest

from log.logger import Logger


class MyTestCase(unittest.TestCase):
    def test_something(self):

        l = Logger()
        l.info("Hello from l {0}".format(Logger()))

        l1 = Logger()
        l1.info("Hello from l1 {0}".format(Logger()))

        Logger().info("Hello from Logger() {0}".format(Logger()))

        # .info('Hello')
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
