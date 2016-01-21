

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


class RAM(Memory):
    """
    This class represents a RAM object, with the extra properties shared, bufferes, cached memory.
    """""

    def __init__(self, total: int, used: int, free: int, shared: int, buffers: int, cached: int):
        """
        :param total: the total memory size
        :param used: the size of used memory
        :param free: the size of free memory
        :param shared: the size of shared memory
        :param buffers: the size of buffers memory
        :param cached: the size of cached memory
        """
        super().__init__(total, used, free)
        self._shared = shared
        self._buffers = buffers
        self._cached = cached

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

    @property
    def cached(self) -> int:
        """
        The size of cached memory

        :return: int
        """
        return self._cached


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
