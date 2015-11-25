from abc import ABCMeta


class ProxyObject(metaclass=ABCMeta):
    """" This class needed to share objects over IPC.
        ProxyObject saves on the server his id which marks the memory point on the server.
        The remote client get this object by copy so the reference is lost for the server.
        If the server get this object back, he can reconstruct reference to the origin object.
        But watch out in the reconstruction process!
        You have to proof that the reference is valid and the origin object still exist on the server.
    """""
    def __init__(self):
        self.__id = id(self)

    def get_id(self):
        """Get the ID from ProxyObject for reconstruction on the server"""
        return self.__id
