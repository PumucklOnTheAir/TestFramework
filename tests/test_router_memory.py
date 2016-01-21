from unittest import TestCase
from router.memory import RAM, Flashdriver, Swap


class TestCPUProcess(TestCase):

    def test_RAM(self):
        ram = RAM(8000, 4000, 4000, 20, 250, 420)
        assert isinstance(ram ,RAM)
        self.assertEqual(8000, ram.total)
        self.assertEqual(4000, ram.used)
        self.assertEqual(4000, ram.free)
        self.assertEqual(20, ram.shared)
        self.assertEqual(250, ram.buffers)
        self.assertEqual(420, ram.cached)

    def test_Flashdriver(self):
        flashdriver = Flashdriver(8000, 4000, 4000)
        assert isinstance(flashdriver ,Flashdriver)
        self.assertEqual(8000, flashdriver.total)
        self.assertEqual(4000, flashdriver.used)
        self.assertEqual(4000, flashdriver.free)

    def test_Swap(self):
        swap = Swap(4000, 2000, 2000)
        assert isinstance(swap ,Swap)
        self.assertEqual(4000, swap.total)
        self.assertEqual(2000, swap.used)
        self.assertEqual(2000, swap.free)