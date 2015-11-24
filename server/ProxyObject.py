from abc import ABCMeta


class ProxyObject(metaclass=ABCMeta):

    def __init__(self):
        self.__id = id(self)

    def get_id(self):
        """Get the ID from ProxyObject for reconstruction on the server"""
        return self.__id
