import unittest
from src.position import Position
from src.path import Path


def assert_position_equal(val: Position, exp: Position):
    tc = unittest.TestCase()

    tc.assertAlmostEqual(val.x, exp.x)
    tc.assertAlmostEqual(val.y, exp.y)
    tc.assertAlmostEqual(val.theta, exp.theta)


def assert_path_equal(val: Path, exp: Path):
    for v, e in zip(val, exp):
        assert_position_equal(v, e)
