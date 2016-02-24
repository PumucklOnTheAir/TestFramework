import logging
import logging.handlers
import os
import threading
import multiprocessing
import sys
import traceback


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


class MultiProcessingHandler(logging.Handler):

    def __init__(self, name: str="", sub_handler: logging.Handler=None) -> None:
        """

        :param name:
        :param sub_handler:
        :return:
        """
        super(MultiProcessingHandler, self).__init__()

        if sub_handler is None:
            sub_handler = logging.StreamHandler()

        self.sub_handler = sub_handler
        self.queue = multiprocessing.Queue(-1)
        self.setLevel(self.sub_handler.level)
        self.setFormatter(self.sub_handler.formatter)
        # The thread handles receiving records asynchronously.
        t = threading.Thread(target=self.receive, name=name)
        t.daemon = True
        t.start()

    def setFormatter(self, fmt: logging.Formatter=None) -> None:
        """

        :param fmt:
        :return:
        """
        logging.Handler.setFormatter(self, fmt)
        self.sub_handler.setFormatter(fmt)

    def receive(self) -> None:
        """

        :return:
        """
        while True:
            try:
                record = self.queue.get()
                self.sub_handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            # except:
            #     traceback.print_exc(file=sys.stderr)

    def send(self, s: logging.LogRecord=None) -> None:
        """

        :param s:
        :return:
        """
        self.queue.put_nowait(s)

    def _format_record(self, record: logging.LogRecord=None) -> logging.LogRecord:
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
        try:
            s = self._format_record(record)
            self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        # except Exception as ex:
        #     self.handleError(record)

    def close(self) -> None:
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

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
    LOG_PATH = os.path.join(BASE_DIR, 'log')  # Join Project Root with log

    _is_setup_loaded = False
    _max_log_deep = 0

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

            file_handler = None
            try:
                if log_file_path == "logger.log":
                    file_handler = logging.handlers.RotatingFileHandler(os.path.join(LoggerSetup.LOG_PATH,
                                                                                     log_file_path))
                else:
                    file_handler = logging.handlers.RotatingFileHandler(log_file_path)
            except Exception as ex:
                logging.warning("Logger can not create {0}: {1}".format(log_file_path, ex))

            # create StreamHandler
            stream_handler = logging.StreamHandler()

            # create ConsoleHandler
            console_handler = None
            try:
                console_handler = logging.StreamHandler(open('/dev/console', 'w'))
            except Exception as ex:
                logging.warning("Logger can not log on {0}: {1}".format('/dev/console', ex))

            # create a SysLogHandler
            syslog_handler = None
            try:
                syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
            except Exception as ex:
                logging.warning("Logger can not log on {0}: {1}".format('/dev/log', ex))

            # create a logging format
            if log_format == "":
                log_format = "%(asctime)-23s - %(levelname)-8s : %(message)s"
            if file_handler is not None:
                file_handler.setFormatter(ColoredFormatter(log_format, use_color=False))
            stream_handler.setFormatter(ColoredFormatter(log_format))
            if console_handler is not None:
                console_handler.setFormatter(ColoredFormatter(log_format))
            if syslog_handler is not None:
                syslog_handler.setFormatter(ColoredFormatter(log_format, use_color=False))

            # add the handlers to the logger
            logger = logging.getLogger()
            if logger.hasHandlers():
                logger.handlers.clear()
            if file_handler is not None:
                logger.addHandler(file_handler)
            logger.addHandler(stream_handler)
            if console_handler is not None:
                logger.addHandler(console_handler)
            if syslog_handler is not None:
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

        except logging.ERROR as ex:
            logging.error("Error at the setup of the logger object:\nError: {0}".format(ex))

    @staticmethod
    def shutdown() -> None:
        """
        Close open streams and handlers
        :return: None
        """
        LoggerSetup.de_register_multiprocess_handlers()
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
        :return:
        """
        if logger is None:
            logger = logging.getLogger()

        for i, orig_handler in enumerate(list(logger.handlers)):
            handler = MultiProcessingHandler('mp-handler-{0}'.format(i), sub_handler=orig_handler)
            logger.removeHandler(orig_handler)
            logger.addHandler(handler)

    @staticmethod
    def de_register_multiprocess_handlers(logger: logging=None) -> None:
        """

        :param logger:
        :return:
        """
        if logger is None:
            logger = logging.getLogger()

        for handler in logger.handlers:
            handler.close()
            logger.removeHandler(handler)
