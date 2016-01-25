from abc import ABCMeta, abstractproperty


class RemoteSystem(metaclass=ABCMeta):

    @abstractproperty
    def ip(self) -> str:
        pass

    @abstractproperty
    def vlan_iface_id(self) -> int:
        pass

    @abstractproperty
    def vlan_iface_name(self) -> str:
        pass

    @abstractproperty
    def namespace_name(self) -> str:
        pass

    @abstractproperty
    def ip_mask(self) -> int:
        pass

    @abstractproperty
    def usr_name(self) -> str:
        pass

    @abstractproperty
    def usr_password(self) -> str:
        pass
