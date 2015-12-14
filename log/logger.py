import logging
import os


class DebugLevel:
    """
    Contains the level for different debug modes
    """

    ONE = 1
    TWO = 2
    THREE = 3


class Singleton(type):
    """
    Holds instances of an object
    """

    _instances = {}

    def __call__(cls, *args, **kwargs) -> object:
        """
        Return an exists instance or create a new and return this instance
        :param args:
        :param kwargs:
        :return: instance of an object
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    """
    Logger class to log messages in a log file and on the console

    USE:

    logger = Logger()
    logger.setup()

    logger.info('INFO-MSG')
    logger.debug('DEBUG-MSG')
    logger.warning('WARNING-MSG')
    logger.error('ERROR-MSG')
    logger.critical('CRITICAL-MSG')

    OR:

    Logger().setup()

    Logger.info('INFO-MSG')
    Logger.debug('DEBUG-MSG')
    Logger.warning('WARNING-MSG')
    Logger.error('ERROR-MSG')
    Logger.critical('CRITICAL-MSG')
    """

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
    LOG_PATH = os.path.join(BASE_DIR, 'log')  # Join Project Root with log

    _logger = None
    _debug_level = None

    @property
    def logger(self) -> logging.Logger:
        """
        Instance of a logging.Logger object
        :return: logging.Logger
        """
        if self._logger is None:
            self.setup()
        return self._logger

    @property
    def is_loaded(self) -> bool:
        """
        Check if the logger has a instance
        :return: bool
        """
        if self._logger is None:
            return False
        return True

    @property
    def debug_level(self) -> DebugLevel:
        """
        Return the level of debug
        :return: DebugLevel
        """
        self._debug_level

    def setup(self, log_level: int = logging.INFO, file_log_level: int = logging.INFO,
              stream_log_level: int = logging.INFO, log_file_path: str = "logger.log",
              log_file_formatter: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
              log_stream_formatter: str = "%(asctime)s - %(levelname)s - %(message)s",
              debug_level: int = 0) -> None:
        """
        Create and initialize a new logging.Logger and create a new file and stream handler with the params
        :param log_level: Logging level for the logging.Logger
        :param file_log_level: Logging level for the file handler
        :param stream_log_level: Logging level for the stream handler
        :param log_file_path: Path for the log file
        :param log_file_formatter: Formatter for the output in the log file
        :param log_stream_formatter: Formatter for the output in the stream
        :param debug_level: explain the deep of the debug mode
        :return: None
        """
        try:
            self._logger = logging.getLogger(__name__)

            # set level
            self._logger.setLevel(log_level)

            # create a file handler
            if log_file_path == "":
                logging.error("Path of the log file is an empty string")
                return

            if log_file_path == "logger.log":
                file_handler = logging.FileHandler(os.path.join(self.LOG_PATH, 'logger.log'))
            else:
                file_handler = logging.FileHandler(log_file_path)

            file_handler.setLevel(file_log_level)

            # create StreamHandler
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(stream_log_level)

            # create a logging format
            file_formatter = logging.Formatter(log_file_formatter)
            file_handler.setFormatter(file_formatter)

            stream_formatter = logging.Formatter(log_stream_formatter)
            stream_handler.setFormatter(stream_formatter)

            # add the handlers to the logger
            if self._logger.hasHandlers():
                self._logger.handlers.clear()
            self._logger.addHandler(file_handler)
            self._logger.addHandler(stream_handler)

            self._debug_level = debug_level

        except logging.ERROR as ex:
            logging.error("Error at the setup of the logger object:\nError: {0}".format(ex))

    def info(self, msg: str = "", *args, **kwargs) -> None:
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        :param msg: Message to log
        :param args:
        :param kwargs:
        :return: None
        """
        if not self.is_loaded:
            self.setup()
        self._logger.info(msg, *args, **kwargs)

    def debug(self, debug_level: int = 0, msg: str = "", *args, **kwargs) -> None:
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", "interesting problem", exc_info=1)
        :param debug_level: explain the deep of the debug mode
        :param msg: Message to log
        :param args:
        :param kwargs:
        :return: None
        """
        if not self.is_loaded:
            self.setup()

        temp_str = ""
        for x in range(0, debug_level):
            temp_str += '\t'

        self._logger.debug("{0}{1}".format(temp_str, msg), *args, **kwargs)

    def warning(self, msg: str = "", *args, **kwargs) -> None:
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.warning("Houston, we have a %s", "interesting problem", exc_info=1)
        :param msg: Message to log
        :param args:
        :param kwargs:
        :return: None
        """
        if not self.is_loaded:
            self.setup()
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str = "", *args, **kwargs) -> None:
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", "interesting problem", exc_info=1)
        :param msg: Message to log
        :param args:
        :param kwargs:
        :return: None
        """
        if not self.is_loaded:
            self.setup()
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg: str = "", *args, **kwargs) -> None:
        """
        Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "interesting problem", exc_info=1)
        :param msg: Message to log
        :param args:
        :param kwargs:
        :return: None
        """
        if not self.is_loaded:
            self.setup()
        self._logger.critical(msg, *args, **kwargs)
