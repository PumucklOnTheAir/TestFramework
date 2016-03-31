from abc import ABCMeta, abstractproperty, abstractmethod, abstractstaticmethod
from log.loggersetup import LoggerSetup
from typing import List
import logging
# from server.server import Server


class RemoteSystem(metaclass=ABCMeta):
    """
    This abstract-class/interface provides the attributes that are necessary if we want to communicate
    with a system through the network.
    """""

    @abstractproperty
    def id(self) -> int:
        """
        The id to identify a RemoteSystem.

        :return: RemoteSystem_id
        """
        pass

    @abstractproperty
    def ip(self) -> str:
        """
        The IP on which the RemoteSystem is listening.

        :return: RemoteSystem_ip
        """
        pass

    @abstractproperty
    def ip_mask(self) -> int:
        """
        Mask of the IP on which the RemoteSystem is listening.

        :return: RemoteSystem_ip_mask
        """
        pass

    @abstractproperty
    def vlan_iface_id(self) -> int:
        """
        The id of the VLAN, which the RemoteSystem is connected to.

        :return: VLAN-iface_id
        """
        pass

    @abstractproperty
    def vlan_iface_name(self) -> str:
        """
        The name of the VLAN, which the RemoteSystem is connected to.

        :return: VLAN_iface_name
        """
        pass

    @abstractproperty
    def namespace_name(self) -> str:
        """
        The name of the Namespace, where the VLAN, that is used to communicate to the RemoteSystem, is encapsulated.

        :return: Namespace_name
        """
        pass

    @abstractproperty
    def usr_name(self) -> str:
        """
        The user-name that is used via SSH.

        :return: RemoteSystem_user_name
        """
        pass

    @abstractproperty
    def usr_password(self) -> str:
        """
        The password that is used via SSH.

        :return: Remotesystem_user_password
        """
        pass

    def __str__(self):
        return "RemoteSystem{IP:%s, VLAN ID:%s, NS:%s}" % (self.ip, self.vlan_iface_id, self.namespace_name)


class RemoteSystemJob(metaclass=ABCMeta):
    """
    The abstract class for Tasks which are executed in the specific namespace of a remote system.

    It has the vars self/cls.remote_system and self/cls.all_routers.

    The Server handles the job and is working in the following order:
        - data = job.pre_process(Server)
        -    job.prepare(remote_sys)
        -    executeWithVLAN: result = job.run()
        - job.post_process(result)

    """""

    def __init__(self):
        self.remote_system = None
        self.all_routers = None
        self.__return_data = None

    def __str__(self):
        return self.__class__.__name__  # TODO: __str__ remotesystemjob"

    def prepare(self, remote_sys: RemoteSystem, routers: List):
        """
        Prepares the system job before the run method will started.

        :param remote_sys: the RemoteSystem which are connected to this job
        :param routers: all routers as a copy
        """
        logging.debug("%sPrepare job", LoggerSetup.get_log_deep(5))
        self.remote_system = remote_sys
        self.all_routers = routers
        RemoteSystemJob._prepare(remote_sys, routers)

    @classmethod
    def _prepare(cls, remote_sys: RemoteSystem, routers: List):
        # TODO: doc
        cls.remote_system = remote_sys
        cls.all_routers = routers

    @abstractstaticmethod
    def pre_process(self, server) -> {}:
        """
        Pre process and aggregate data in the main process.

        :param server: the Server
        :return: Arbitrary data as an dictionary for the run method
        """
        return None

    @abstractstaticmethod
    def post_process(self, data: {}, server):
        """
        Post process the result data from RemoteSystemJob in the main process.

        :param data: result from run()
        :param server: the Server
        """
        pass

    @abstractmethod
    def run(self) -> {}:
        """
        The run method which will execute in the proper VLAN.
        As default you get a RemoteSystem with self.remote_system
        and optional the data from pre_process method with self.data.

        :return Result data as dictionary for the post_process method:
        """
        pass
