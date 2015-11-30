import io
import logging


class FileManager:

    @staticmethod
    def read_file(path) -> []:
        try:
            file = io.open(path, "r", encoding="utf-8")
            output = file.read()
            file.close()
            return output
        except IOError as ex:
            logging.error("Error at read the file at path: {0}\nError: {1}".format(path, ex))

    @staticmethod
    def write_file(data, path) -> None:
        try:
            file = io.open(path, "w", encoding="utf-8")
            file.write(data)
            file.flush()
            file.close()
        except IOError as ex:
            logging.error("Error at write the file at path: {0}\nError: {1}".format(path, ex))
