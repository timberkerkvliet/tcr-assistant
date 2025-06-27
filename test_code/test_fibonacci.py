from unittest import TestCase

from .fibo import fibo


class TestFibonacci(TestCase):
    def test_0(self):
        self.assertEqual(fibo(1), 1)

    def test_1(self):
        self.assertEqual(fibo(2), 1)

    def test_2(self):
        self.assertEqual(fibo(3), 2)

    def test_3(self):
        self.assertEqual(fibo(4), 3)

    def test_4(self):
        self.assertEqual(fibo(5), 5)

    def test_4(self):
        self.assertEqual(fibo(6), 8)
