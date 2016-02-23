import unittest
import logging
from log.loggersetup import LoggerSetup


class MyTestCase(unittest.TestCase):

    def test_setup(self):
        """
        Tests setup
        :return: Tests results
        """

        LoggerSetup.setup(10)

        self.assertEqual(True, LoggerSetup.is_setup_loaded())

        LoggerSetup.shutdown()

    def test_is_loaded(self):
        """
        Tests is loaded
        :return: Tests results
        """
        LoggerSetup.setup()
        result = LoggerSetup.is_setup_loaded()
        LoggerSetup.shutdown()

        self.assertEqual(True, result)

    def test_info(self):
        """
        Tests info
        :return: Tests results
        """
        LoggerSetup.setup(10)

        logging.info("Info")

        self.assertEqual(True, LoggerSetup.is_setup_loaded())

        LoggerSetup.shutdown()

    def test_debug(self):
        """
        Tests debug
        :return: Tests results
        """
        LoggerSetup.setup(10)

        logging.debug("Debug")

        self.assertEqual(True, LoggerSetup.is_setup_loaded())

        LoggerSetup.shutdown()

    def test_warning(self):
        """
        Tests warning
        :return: Tests results
        """
        LoggerSetup.setup(10)

        logging.warning("Warning")

        self.assertEqual(True, LoggerSetup.is_setup_loaded())

        LoggerSetup.shutdown()

    def test_error(self):
        """
        Tests error
        :return: Tests results
        """
        LoggerSetup.setup(10)

        logging.error("Error")

        self.assertEqual(True, LoggerSetup.is_setup_loaded())

        LoggerSetup.shutdown()

    def test_critical(self):
        """
        Tests critical
        :return: Tests results
        """
        LoggerSetup.setup(10)

        logging.critical("Critical")

        self.assertEqual(True, LoggerSetup.is_setup_loaded())

        LoggerSetup.shutdown()

    def test_debug_level(self):
        """
        Test debug level
        :return: Test results
        """
        LoggerSetup.setup(10, "logger.log", "", 5, None)
        deep = LoggerSetup._max_log_deep
        LoggerSetup.shutdown()

        self.assertEqual(True, deep == 5)

    def test_log_level_tab(self):
        """
        Test log level tab
        :return: Test results
        """
        LoggerSetup.setup(10)

        logging.info("%sInfo deep 2", LoggerSetup.get_log_deep(2))
        logging.info("%sInfo deep 3 with - as char", LoggerSetup.get_log_deep(3, '-'))

        self.assertEqual(True, LoggerSetup.is_setup_loaded())

        LoggerSetup.shutdown()

    def test_close(self):
        """
        Tests close
        :return: Tests results
        """
        LoggerSetup.setup()
        LoggerSetup.shutdown()

        self.assertEqual(False, LoggerSetup.is_setup_loaded())
