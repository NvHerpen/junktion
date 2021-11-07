import unittest
from src.position import Position
from src.path import Path


def assert_position_equal(val: Position, exp: Position, places: int = 7):
    tc = unittest.TestCase()

    tc.assertAlmostEqual(val.x, exp.x, places=places)
    tc.assertAlmostEqual(val.y, exp.y, places=places)
    tc.assertAlmostEqual(val.theta, exp.theta, places=places)


def assert_path_equal(val: Path, exp: Path, places: int = 7):
    tc = unittest.TestCase()
    tc.assertEqual(len(val), len(exp))

    for v, e in zip(val, exp):
        assert_position_equal(v, e, places=places)
