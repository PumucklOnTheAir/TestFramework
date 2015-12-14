import logging
import os


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
    LOG_PATH = os.path.join(BASE_DIR, 'log')  # Join Project Root with log

    _logger = None

    @property
    def logger(self) -> logging.Logger:
        """
        Instance of a logging.Logger object
        :return:
        """
        if self._logger is None:
            self.setup()
        return self._logger

    @property
    def is_loaded(self) -> bool:
        """
        check if the logger has a instance
        :return:
        """
        if self._logger is None:
            return False
        return True

    def setup(self, log_level: int = logging.INFO, file_log_level: int = logging.INFO,
              stream_log_level: int = logging.INFO, log_file_path: str = "logger.log",
              log_file_formatter: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
              log_stream_formatter: str = "%(asctime)s - %(levelname)s - %(message)s") -> None:

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
            self._logger.addHandler(file_handler)
            self._logger.addHandler(stream_handler)

        except logging.ERROR as ex:
            logging.error("Error at the setup of the logger object:\nError: {0}".format(ex))

    def info(self, msg: str, *args, **kwargs) -> None:
        if not self.is_loaded:
            self.setup()
        self._logger.info(msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs) -> None:
        if not self.is_loaded:
            self.setup()
        self._logger.debug(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        if not self.is_loaded:
            self.setup()
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        if not self.is_loaded:
            self.setup()
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        if not self.is_loaded:
            self.setup()
        self._logger.critical(msg, *args, **kwargs)
