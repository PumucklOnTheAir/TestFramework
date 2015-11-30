from server.proxyobject import ProxyObject


class Router(ProxyObject):

    def __init__(self, ip4):
        ProxyObject.__init__(self)

        self._ip4 = None
        self.ip4 = ip4

    @property
    def ip4(self): #TODO -> ?
        return self._ip4

    @ip4.setter
    def ip4(self, value):
        #TODO type => add assert
        self._ip4 = value
        pass


