import logging
import os
import sys


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


class ColoredFormatter(logging.Formatter):
    """
    Formatter instances are used to convert a LogRecord to text with color highlighting.
    """

    _use_color = None

    # These are the sequences need to get colored output
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[0;%dm"

    COLORS = {
        'WARNING': 31,
        'INFO': 31,
        'DEBUG': 31,
        'CRITICAL': 31,
        'ERROR': 31,
    }

    def __init__(self, fmt: str = "", use_color: bool = True) -> None:
        """
        Initialize the formatter with specified format strings.

        Initialize the formatter either with the specified format string, or a
        default as described above. Allow for specialized date formatting with
        the optional datefmt argument (if omitted, you get the ISO8601 format).

        Use a style parameter of '%', '{' or '$' to specify that you want to
        use one of %-formatting, :meth:`str.format` (``{}``) formatting or
        :class:`string.Template` formatting in your format string.
        """
        logging.Formatter.__init__(self, fmt)
        self._use_color = use_color

    def format(self, record) -> object:
        """
        Format the specified record as text.

        The record's attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory steps
        are carried out. The message attribute of the record is computed
        using LogRecord.getMessage(). If the formatting string uses the
        time (as determined by a call to usesTime(), formatTime() is
        called to format the event time. If there is exception information,
        it is formatted using formatException() and appended to the message.
        :param record
        :return: object
        """
        record.message = record.getMessage()
        level = record.levelname
        if self._use_color and level in self.COLORS:
            msg_color = self.COLOR_SEQ % (self.COLORS[level]) + record.message + self.RESET_SEQ
            record.message = msg_color
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s += "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s += "\n"
            s = s + self.formatStack(record.stack_info)
        return s


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

    logging.Level order
    NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
    """

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
    LOG_PATH = os.path.join(BASE_DIR, 'log')  # Join Project Root with log

    _logger = None
    _max_detail_log_level = None

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
    def max_detail_log_level(self) -> int:
        """
        Return the max detail level
        :return: int
        """
        return self._max_detail_log_level

    def setup(self, log_level: int = logging.DEBUG, file_log_level: int = logging.DEBUG,
              stream_log_level: int = logging.DEBUG, log_file_path: str = "logger.log", log_file_format: str = "",
              log_stream_format: str = "", max_detail_log_level: int = 5, log_filter: logging.Filter = None) -> None:
        """
        Create and initialize a new logging.Logger and create a new file and stream handler with the params
        :param log_level: Logging level for the logging.Logger
        :param file_log_level: Logging level for the file handler
        :param stream_log_level: Logging level for the stream handler
        :param log_file_path: Path for the log file
        :param log_file_format: Formatter for the output in the log file
        :param log_stream_format: Formatter for the output in the stream
        :param max_detail_log_level: Define the max level, how deep goes a detail of a log
        :param log_filter: filter for filter the log output
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
            # default is without param, than the handler is sys.stderr
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(stream_log_level)

            # create a logging format
            if log_file_format == "":
                log_file_format = "%(asctime)-23s - %(name)-10s - %(levelname)-8s : %(message)s"
            file_formatter = logging.Formatter(log_file_format)
            file_handler.setFormatter(file_formatter)

            if log_stream_format == "":
                log_stream_format = "%(asctime)-23s - %(levelname)-8s : %(message)s"
                stream_handler.setFormatter(ColoredFormatter(log_stream_format))
            else:
                stream_formatter = logging.Formatter(log_stream_format)
                stream_handler.setFormatter(stream_formatter)

            # add the handlers to the logger
            if self._logger.hasHandlers():
                self._logger.handlers.clear()
            self._logger.addHandler(file_handler)
            self._logger.addHandler(stream_handler)

            self._max_detail_log_level = max_detail_log_level

            # add Filter to logger
            if log_filter is not None:
                if len(self._logger.filters) > 0:
                    self._logger.filters.clear()
                self._logger.addFilter(log_filter)

        except logging.ERROR as ex:
            logging.error("Error at the setup of the logger object:\nError: {0}".format(ex))

    def get_log_level_tab(self, log_level: int = 0) -> str:
        """
        Return an string with tabulators. Count of tabulators are depend on log_level.
        log_level = 0 returns empty string
        :param log_level: deep of the level mode
        :return: String with tabulators
        """
        if log_level > self._max_detail_log_level:
            log_level = self._max_detail_log_level
        temp_str = ""
        for x in range(0, log_level):
            temp_str += '\t'
        return temp_str

    def info(self, msg: str = "", info_level: int = 0, *args, **kwargs) -> None:
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        :param msg: Message to log
        :param info_level: explain the deep of the info mode
        :param args:
        :param kwargs:
        :return: None
        """
        if not self.is_loaded:
            self.setup()
        if info_level <= self._max_detail_log_level:
            self._logger.info("{0}{1}".format(self.get_log_level_tab(info_level), msg), *args, **kwargs)

    def debug(self, msg: str = "", debug_level: int = 0, *args, **kwargs) -> None:
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", "interesting problem", exc_info=1)
        :param msg: Message to log
        :param debug_level: explain the deep of the debug mode
        :param args:
        :param kwargs:
        :return: None
        """
        if not self.is_loaded:
            self.setup()
        if debug_level <= self._max_detail_log_level:
            self._logger.debug("{0}{1}".format(self.get_log_level_tab(debug_level), msg), *args, **kwargs)

    def warning(self, msg: str = "", warning_level: int = 0, *args, **kwargs) -> None:
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.warning("Houston, we have a %s", "interesting problem", exc_info=1)
        :param msg: Message to log
        :param warning_level: explain the deep of the warning mode
        :param args:
        :param kwargs:
        :return: None
        """
        if not self.is_loaded:
            self.setup()
        if warning_level <= self._max_detail_log_level:
            self._logger.warning("{0}{1}".format(self.get_log_level_tab(warning_level), msg), *args, **kwargs)

    def error(self, msg: str = "", error_level: int = 0, *args, **kwargs) -> None:
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", "interesting problem", exc_info=1)
        :param msg: Message to log
        :param error_level: explain the deep of the error mode
        :param args:
        :param kwargs:
        :return: None
        """
        if not self.is_loaded:
            self.setup()
        if error_level <= self._max_detail_log_level:
            self._logger.error("{0}{1}".format(self.get_log_level_tab(error_level), msg), *args, **kwargs)

    def critical(self, msg: str = "", critical_level: int = 0, *args, **kwargs) -> None:
        """
        Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "interesting problem", exc_info=1)
        :param msg: Message to log
        :param critical_level: explain the deep of the critical mode
        :param args:
        :param kwargs:
        :return: None
        """
        if not self.is_loaded:
            self.setup()
        if critical_level <= self._max_detail_log_level:
            self._logger.critical("{0}{1}".format(self.get_log_level_tab(critical_level), msg), *args, **kwargs)

    def log(self, level: int = logging.NOTSET, msg: str = "", log_level: int = 0, *args, **kwargs) -> None:
        """
        Log 'msg % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.log(level, "We have a %s", "mysterious problem", exc_info=1)
        :param level: which logging.Level to log
        :param msg: Message to log
        :param log_level: explain the deep of the critical mode
        :param args:
        :param kwargs:
        :return: None
        """
        if not self.is_loaded:
            self.setup()
        if log_level <= self._max_detail_log_level:
            self._logger.log(level, "{0}{1}".format(self.get_log_level_tab(log_level), msg), *args, **kwargs)
