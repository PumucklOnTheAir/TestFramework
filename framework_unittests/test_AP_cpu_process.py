from unittest import TestCase
from router.cpu_process import CPUProcess


class TestCPUProcess(TestCase):

    def test_create_CPUProcess(self):
        cpu_process = CPUProcess(1919, "root", 3.4, 7.4, "firefox")
        assert isinstance(cpu_process, CPUProcess)

        self.assertEqual(1919, cpu_process.pid)
        self.assertEqual("root", cpu_process.user)
        self.assertEqual(7.4, cpu_process.cpu)
        self.assertEqual(3.4, cpu_process.mem)
        self.assertEqual("firefox", cpu_process.command)
