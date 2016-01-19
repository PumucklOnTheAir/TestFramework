from abc import ABCMeta, abstractproperty, abstractmethod
from log.logger import Logger
from threading import Thread
# from server.server import Server


class RemoteSystem(metaclass=ABCMeta):

    def __init__(self):
        # test/task handling
        self.running_task = None
        self.waiting_tasks = []

    def __str__(self):
        return "RemoteSystem{IP:%s, VLAN ID:%s, NS:%s}" % (self.ip, self.vlan_iface_id, self.namespace_name)

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

    def prepare(self, remote_sys: RemoteSystem, data: {} = None) -> None:
        """
        Prepares the system job before the run method will started

        :param remote_sys: the RemoteSystem which are connected to this job
        :param data: Arbitrary data as an dictionary
        """
        Logger().debug("Job prepare", 3)
        self.remote_system = remote_sys
        self.data = data

    @abstractmethod
    def pre_process(self, server) -> {}:
        """
        Pre process and aggregate data in the main process

        :param server: the Server
        :return: Arbitrary data as an dictionary for the run method
        """
        return None

    @abstractmethod
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
