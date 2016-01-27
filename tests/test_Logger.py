import unittest
from log.logger import Logger


class MyTestCase(unittest.TestCase):

    def test_setup(self):
        """
        Tests setup
        :return: Tests results
        """
        l = Logger()

        l.setup(False, 10)

        self.assertEqual(True, l.is_loaded)

        l.close()

    def test_is_loaded(self):
        """
        Tests is loaded
        :return: Tests results
        """
        Logger().setup()
        result = Logger().is_loaded
        Logger().close()

        self.assertEqual(True, result)

    def test_logger(self):
        """
        Tests logger
        :return: Tests results
        """
        result = Logger().logger

        self.assertEqual(True, Logger().logger is result)

        Logger().close()

    def test_info(self):
        """
        Tests info
        :return: Tests results
        """
        Logger().info("Hello from logger: {0}".format(Logger()))
        Logger().close()

        self.assertEqual(True, True)

    def test_debug(self):
        """
        Tests debug
        :return: Tests results
        """
        Logger().debug("Debug from Logger() {0}".format(Logger()))
        Logger().close()

        self.assertEqual(True, True)

    def test_warning(self):
        """
        Tests warning
        :return: Tests results
        """
        Logger().warning("Warning from Logger() {0}".format(Logger()))
        Logger().close()

        self.assertEqual(True, True)

    def test_error(self):
        """
        Tests error
        :return: Tests results
        """
        Logger().error("Error from Logger() {0}".format(Logger()))
        Logger().close()

        self.assertEqual(True, True)

    def test_critical(self):
        """
        Tests critical
        :return: Tests results
        """
        Logger().critical("Critical from Logger() {0}".format(Logger()))
        Logger().close()

        self.assertEqual(True, True)

    def test_log(self):
        """
        Tests critical
        :return: Tests results
        """
        Logger().log(20, "Log from Logger() {0}".format(Logger()))
        Logger().close()

        self.assertEqual(True, True)

    def test_debug_level(self):
        """
        Test debug level
        :return: Test results
        """
        logger = Logger()
        logger.setup(False, 10, 10, 10, "logger.log", "", "", 5, None)
        level = logger.max_detail_log_level()
        logger.close()

        self.assertEqual(True, level == 5)

    def test_log_level_tab(self):
        """
        Test log level tab
        :return: Test results
        """
        tabs = Logger().get_log_level_tab(2)
        Logger().close()

        self.assertEqual(True, tabs == "\t\t")

    def test_close(self):
        """
        Tests close
        :return: Tests results
        """
        logger = Logger()
        logger.setup()
        logger.close()

        self.assertEqual(False, logger.is_loaded)

if __name__ == '__main__':
    unittest.main()
