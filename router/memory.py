

class Memory:
    """
    This class represents a Memory object, with the total, used and free memory.
    """""

    def __init__(self, total: int, used: int, free: int):
        """
        :param total: the total memory size
        :param used: the size of used memory
        :param free: the size of free memory
        """
        self._total = total
        self._used = used
        self._free = free

    @property
    def total(self) -> int:
        """
        The total memory size

        :return: int
        """
        return self._total

    @property
    def used(self) -> int:
        """
        The size of used memory

        :return: int
        """
        return self._used

    @property
    def free(self) -> int:
        """
        The size of free memory

        :return: int
        """
        return self._free

    def __str__(self):
        return str(self.total) + " " + str(self.used) + " " + str(self.free)


class RAM(Memory):
    """
    This class represents a RAM object, with the extra properties shared, bufferes, cached memory.
    """""

    def __init__(self, total: int, used: int, free: int, shared: int, buffers: int):
        """
        :param total: the total memory size
        :param used: the size of used memory
        :param free: the size of free memory
        :param shared: the size of shared memory
        :param buffers: the size of buffers memory
        """
        super().__init__(total, used, free)
        self._shared = shared
        self._buffers = buffers

    @property
    def shared(self) -> int:
        """
        The size of shared memory

        :return: int
        """
        return self._shared

    @property
    def buffers(self) -> int:
        """
        The size of buffers memory

        :return: int
        """
        return self._buffers

    def __str__(self):
        return str(self.total) + " " + str(self.used) + " " + str(self.free) + " " + \
               str(self.shared) + " " + str(self.buffers)


class Swap(Memory):
    """
    This class represents a SWAP object.
    """""
    def __init__(self, total: int, used: int, free: int):
        """
        :param total: the total memory size
        :param used: the size of used memory
        :param free: the size of free memory
        """
        super().__init__(total, used, free)


class Flashdriver(Memory):
    """
    This class represents a Flashdriver object resp. USB and SDCards.
    """""
    def __init__(self, total: int, used: int, free: int):
        """
        :param total: the total memory size
        :param used: the size of used memory
        :param free: the size of free memory
        """
        super().__init__(total, used, free)
