from abc import ABCMeta, abstractproperty, abstractmethod, abstractstaticmethod
from log.logger import Logger
from threading import Thread, Event
# from server.server import Server


class RemoteSystem(metaclass=ABCMeta):

    def __str__(self):
        return "RemoteSystem{IP:%s, VLAN ID:%s, NS:%s}" % (self.ip, self.vlan_iface_id, self.namespace_name)

    @abstractproperty
    def id(self) -> int:
        pass

    # TODO docu
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


class RemoteSystemJob(Thread, metaclass=ABCMeta):
    """
    An extended Thread for job which are associated with an RemoteSystem.
    The Server handles the job and is working in the following order:
        - data = job.pre_process(Server)
        -    job.prepare(data)
        -    executeWithVLAN: result = job.run()
        - job.post_process(result)

    """""
    def __init__(self):
        self.remote_system = None
        self.data = None
        self.__done_event = None
        self.__return_data = None

    def __str__(self):
        return "TODO: __str__ remotesystemjob"

    def prepare(self, remote_sys: RemoteSystem, data: {} = None) -> None:
        """
        Prepares the system job before the run method will started

        :param remote_sys: the RemoteSystem which are connected to this job
        :param data: Arbitrary data as an dictionary
        """
        Logger().debug("Prepare job", 5)
        self.remote_system = remote_sys
        self.data = data

    def set_done_event(self, done_event: Event = None) -> None:
        """

        :param done_event: Optional Event which will be called at the end
        :return:
        """
        self.__done_event = done_event

    def done(self) -> None:
        """
        Will be called by the Server
        :return:
        """
        if self.__done_event is not None:
            self.__done_event.set()

    def return_data(self, return_data: {}):
        self.__return_data = return_data

    def get_return_data(self) -> {}:
        return self.__return_data

    @abstractstaticmethod
    def pre_process(self, server) -> {}:
        """
        Pre process and aggregate data in the main process

        :param server: the Server
        :return: Arbitrary data as an dictionary for the run method
        """
        return None

    @abstractstaticmethod
    def post_process(self, data: {}, server) -> None:
        """
        Post process the result data from RemoteSystemJob in the main process

        :param data: result from run()
        :param server: the Server
        :return:
        """
        pass

    @abstractmethod
    def run(self) -> {}:
        """
        The run method which will execute in the proper VLAN.
        As default you get a RemoteSystem with self.remote_system
        and optional the data from pre_process method with self.data

        :return Result data as dictionary for the post_process method:
        """
        pass
