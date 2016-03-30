import logging
from logging import handlers
from os import path
from threading import Thread
from multiprocessing import Queue


class ColoredFormatter(logging.Formatter):
    """
    Formatter instances are used to convert a LogRecord to text with color highlighting.
    """

    _use_color = False

    # These are the sequences need to get colored output
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[0;%dm"

    # Colors: 30=black ,31=rot ,32=green ,33=orange ,34=blue ,35=rosa, 36=cyan ,37=white/gray
    COLORS = {
        'WARNING': 33,
        'INFO': 37,
        'DEBUG': 37,
        'CRITICAL': 31,
        'ERROR': 31,
    }

    def __init__(self, fmt: str = "", use_color: bool = True):
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


class MultiProcessingHandler(logging.Handler):

    def __init__(self, name: str="", sub_handler: logging.Handler=None):
        """
        Create new multiprocess handler instance
        :param name: name of the handler
        :param sub_handler: logging handler e.g. FileHandler
        :return: MultiProcessingHandler
        """
        super(MultiProcessingHandler, self).__init__()

        if sub_handler is None:
            sub_handler = logging.StreamHandler()

        self.sub_handler = sub_handler
        self.queue = Queue(-1)
        self.setLevel(self.sub_handler.level)
        self.setFormatter(self.sub_handler.formatter)
        # The thread handles receiving records asynchronously.
        t = Thread(target=self.receive, name=name)
        t.daemon = True
        t.start()

    def setFormatter(self, fmt: logging.Formatter=None) -> None:
        """
        Set formatter
        :param fmt: formatter
        :return: None
        """
        logging.Handler.setFormatter(self, fmt)
        self.sub_handler.setFormatter(fmt)

    def receive(self) -> None:
        """
        Receive a message from the queue
        :return: None
        """
        while True:
            try:
                record = self.queue.get()
                self.sub_handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break

    def send(self, s: logging.LogRecord=None) -> None:
        """
        Set a message at the queue
        :param s: LogRecord with the message info
        :return: None
        """
        self.queue.put_nowait(s)

    def _format_record(self, record: logging.LogRecord=None) -> logging.LogRecord:
        """
        Formatted the LogRecord
        :param record: LogRecord with the message info
        :return: LogRecord with formatted message
        """
        # ensure that exc_info and args
        # have been stringified. Removes any chance of
        # unpickleable things inside and possibly reduces
        # message size sent over the pipe.
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            self.format(record)
            record.exc_info = None

        return record

    def emit(self, record: logging.LogRecord=None) -> None:
        """
        Do whatever it takes to actually log the specified logging record.

        This version is intended to be implemented by subclasses and so
        raises a NotImplementedError.
        :param record: LogRecord with the message info
        :return: None
        """
        try:
            s = self._format_record(record)
            self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise

    def close(self) -> None:
        """
        Close the handler
        :return: None
        """
        self.sub_handler.close()
        logging.Handler.close(self)


class LoggerSetup:
    """
    LoggerSetup class to log messages in a log file and on the console and SyslogHandler of the system

    USE:
    import logging
    from log.loggersetup import LoggerSetup

    LoggerSetup.setup()

    logging.info('INFO-MSG')
    logging.debug('DEBUG-MSG')
    logging.warning('WARNING-MSG')
    logging.error('ERROR-MSG')
    logging.critical('CRITICAL-MSG')

    message with log level deep:
    logging.info("%sInfo deep 2", LoggerSetup.get_log_deep(2))

    logging.Level order:
    0      < 10    < 20   < 30      < 40    < 50
    NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL

    LoggerSetup.close()
    """

    BASE_DIR = path.dirname(path.dirname(__file__))  # This is your Project Root
    LOG_PATH = path.join(BASE_DIR, 'log')  # Join Project Root with log

    _is_setup_loaded = False
    _max_log_deep = 0
    _stream_paths = []
    _log_format = ""

    @staticmethod
    def is_setup_loaded() -> bool:
        """
        Check if the logger has run the setup routine
        :return: bool
        """
        return LoggerSetup._is_setup_loaded

    @staticmethod
    def setup(log_level: int = logging.DEBUG, log_file_path: str = "logger.log", log_format: str = "",
              max_log_deep: int = 5, log_filter: logging.Filter = None) -> None:
        """
        Create and initialize a new logging.Logger and create a new file and stream handler with the params
        :param log_level: Logging level
        :param log_file_path: Path for the log file
        :param log_format: Formatter for the output
        :param max_log_deep: Define the max level, how deep goes a detail of a log
        :param log_filter: filter for filter the log output
        :return: None
        """
        try:
            # set config at highest Logger in the hierarchical
            # set level
            logging.basicConfig(level=log_level)

            # create a file handler
            if log_file_path == "":
                logging.error("Path of the log file is an empty string")
                return

            file_handler = LoggerSetup.create_file_handler(log_file_path)

            # create ConsoleHandler
            dev_console_handler = LoggerSetup.create_stream_handler('/dev/tty1')

            # create a SysLogHandler
            syslog_handler = LoggerSetup.create_syslog_handler()

            # create a logging format
            if log_format == "":
                log_format = "%(asctime)-23s - %(levelname)-8s : %(message)s"

            # add the handlers to the logger and add formatter
            logger = logging.getLogger()
            if logger.hasHandlers():
                logger.handlers.clear()

            if file_handler is not None:
                file_handler.setFormatter(ColoredFormatter(log_format, use_color=False))
                logger.addHandler(file_handler)

            if dev_console_handler is not None:
                dev_console_handler.setFormatter(ColoredFormatter(log_format))
                logger.addHandler(dev_console_handler)

            if syslog_handler is not None:
                syslog_handler.setFormatter(ColoredFormatter(log_format, use_color=False))
                logger.addHandler(syslog_handler)

            # add Filter to logger
            if log_filter is not None:
                if len(logger.filters) > 0:
                    logger.filters.clear()
                logger.addFilter(log_filter)

            # register multiprocess handlers
            LoggerSetup.register_multiprocess_handlers(logger)

            # set LoggerSetup variables
            LoggerSetup._max_log_deep = max_log_deep
            LoggerSetup._is_setup_loaded = True
            LoggerSetup._log_format = log_format
            LoggerSetup._stream_paths.append('/dev/tty1')

            # set log level from paramiko and selenium to warning
            selenium_logger = logging.getLogger('selenium')
            selenium_logger.setLevel(logging.WARNING)
            paramiko_logger = logging.getLogger('paramiko')
            paramiko_logger.setLevel(logging.WARNING)

        except logging.ERROR as ex:
            logging.error("Error at the setup of the logger object:\nError: {0}".format(ex))

    @staticmethod
    def add_handler(stream_path: str = "") -> bool:
        """
        Add new console output to logger handlers
        :param stream_path Path of the stream
        :return: None
        """
        # if path exists do nothing
        if stream_path in LoggerSetup._stream_paths:
            return False

        # register new handler
        logger = logging.getLogger()
        handler = MultiProcessingHandler('mp-handler-{0}'.format(len(logger.handlers)),
                                         sub_handler=LoggerSetup.create_stream_handler(stream_path))
        handler.setFormatter(ColoredFormatter(LoggerSetup._log_format))
        logger.addHandler(handler)

        # add path to collection
        LoggerSetup._stream_paths.append(stream_path)

        return True

    @staticmethod
    def create_syslog_handler() -> logging.Handler:
        """
        Create a SyslogHandler
        :return: SyslogHandler
        """
        try:
            return handlers.SysLogHandler(address='/dev/log')
        except Exception as ex:
            logging.warning("Logger can not log on {0}: {1}".format('/dev/log', ex))
            return None

    @staticmethod
    def create_stream_handler(stream_path: str = "") -> logging.Handler:
        """
        Create a StreamHandler
        :param stream_path Path of the stream
        :return: StreamHandler
        """
        try:
            # console handler
            if stream_path is "":
                return logging.StreamHandler()

            return logging.StreamHandler(open(stream_path, 'w'))
        except Exception as ex:
            logging.warning("Logger can not log on {0}: {1}".format(stream_path, ex))
            # create StreamHandler because can not register console handler
            return logging.StreamHandler()

    @staticmethod
    def create_file_handler(log_file_path: str="") -> logging.Handler:
        """
        Create a FileHandler
        :param log_file_path Path from the file
        :return: FileHandler
        """
        try:
            if log_file_path == "logger.log":
                return handlers.RotatingFileHandler(path.join(LoggerSetup.LOG_PATH, log_file_path))
            else:
                return handlers.RotatingFileHandler(log_file_path)
        except Exception as ex:
            logging.warning("Logger can not create {0}: {1}".format(log_file_path, ex))
            return None

    @staticmethod
    def shutdown() -> None:
        """
        Close open streams and handlers
        :return: None
        """
        LoggerSetup.un_register_multiprocess_handlers()
        logging.shutdown()
        LoggerSetup._is_setup_loaded = False

    @staticmethod
    def get_log_deep(deep: int = 0, deep_char: chr = '\t') -> str:
        """
        Return an string with tabulators. Count of tabulators are depend on log_level.
        log_level = 0 returns empty string
        :param deep: deep of the level mode
        :param deep_char: the character to show the deep
        :return: String with tabulators
        """
        if deep > LoggerSetup._max_log_deep:
            deep = LoggerSetup._max_log_deep
        temp_str = ""
        for x in range(0, deep):
            temp_str += deep_char
        return temp_str

    @staticmethod
    def register_multiprocess_handlers(logger: logging=None)-> None:
        """
        Wraps the handlers in the given Logger with an MultiProcessingHandler.
        :param logger: whose handlers to wrap. By default, the root logger.
        :return: None
        """
        if logger is None:
            logger = logging.getLogger()

        for i, orig_handler in enumerate(list(logger.handlers)):
            handler = MultiProcessingHandler('mp-handler-{0}'.format(i), sub_handler=orig_handler)
            logger.removeHandler(orig_handler)
            logger.addHandler(handler)

    @staticmethod
    def un_register_multiprocess_handlers(logger: logging=None) -> None:
        """
        Un register the multiprocess handler
        :param logger: logging.logger
        :return: None
        """
        if logger is None:
            logger = logging.getLogger()

        for handler in logger.handlers:
            handler.close()
            logger.removeHandler(handler)
