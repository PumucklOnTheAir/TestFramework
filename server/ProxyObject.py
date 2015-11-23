class ProxyObject(object):
    __id = 0

    def __init__(self):
        self.__id = id(self)

    @property
    def get_id(self):
        """Get the ID from ProxyObject for reconstruction on the server"""
        return self.__id
