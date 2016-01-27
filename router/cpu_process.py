

class CPUProcess:
    """
    This class represents a CPU Process, with the process id, user name,
    cpu utilization, memory utilization, start time, and the actual command.
    """""

    def __init__(self, pid: int, user: str, mem: float, cpu: float, command: str):
        """
        This class represents a CPU Process.

        :param pid: process id
        :param user: user name
        :param cpu: cpu utilization
        :param mem: memory utilization
        :param command: actual command
        """
        self._pid = pid
        self._user = user
        self._cpu = cpu
        self._mem = mem
        self._command = command

    @property
    def pid(self) -> int:
        """
        The pid of the process

        :return: int
        """
        return self._pid

    @pid.setter
    def pid(self, value: int):
        """
        :type value: int
        """
        assert isinstance(value, int)
        self._pid = value

    @property
    def user(self) -> str:
        """
        The user of the process

        :return: str
        """
        return self._user

    @user.setter
    def user(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._user = value

    @property
    def cpu(self) -> float:
        """
        The cpu utilization of the process

        :return: float
        """
        return self._cpu

    @cpu.setter
    def cpu(self, value: float):
        """
        :type value: float
        """
        assert isinstance(value, float)
        self._cpu = value

    @property
    def mem(self) -> float:
        """
        The memory of the process

        :return: float
        """
        return self._mem

    @mem.setter
    def mem(self, value: float):
        """
        :type value: float
        """
        assert isinstance(value, float)
        self._mem = value

    @property
    def command(self) -> str:
        """
        The command of the process

        :return: str
        """
        return self._command

    @command.setter
    def command(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._command = value

    def __str__(self):
        return str(self._pid) + " " + self.user + " " + str(self.mem) + "% " + str(self.cpu) + "% " + self.command
