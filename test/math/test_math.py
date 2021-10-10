import pytest

from cythondemo.math.cmath import heron as c_heron
from cythondemo.math.math import heron as py_heron


@pytest.mark.unittest
class TestMathMath:
    def test_python_math(self):
        assert abs(py_heron(3, 4, 5) - 6.0) < 1e-6

    def test_c_math(self):
        assert abs(c_heron(3, 4, 5) - 6.0) < 1e-6


@pytest.mark.benchmark
class TestMathMathBench:
    N = 10000000

    def test_python_math(self):
        for _ in range(self.N):
            _ = py_heron(3, 4, 5)

    def test_c_math(self):
        for _ in range(self.N):
            _ = c_heron(3, 4, 5)
