import unittest
from math import cos, pi, sin

from src.path import Path
from src.position import Position

from test.commons import assert_path_equal, assert_position_equal


class TestInterpolate(unittest.TestCase):
    def test_zero_zero(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(0, 0, 0)
        path = Path.interpolate(X_0, X_1, speed=0)

        exp_path = [Position(0, 0, 0), Position(0, 0, 0)]

        assert_path_equal(path, exp_path)
    
    def test_straight_horizontal(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(10, 0, 0)
        path = Path.interpolate(X_0, X_1, speed=1)

        exp_len_path = 11
        exp_path = [Position(i, 0, 0) for i in range(exp_len_path)]

        self.assertEqual(len(path), exp_len_path)
        assert_path_equal(path, exp_path)
    
    def test_straight_horizontal_fast(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(10, 0, 0)
        speed = 2
        path = Path.interpolate(X_0, X_1, speed=speed)

        exp_len_path = 6
        exp_path = [Position(i*speed, 0, 0) for i in range(exp_len_path)]

        self.assertEqual(len(path), exp_len_path)
        assert_path_equal(path, exp_path)

    def test_float_speed(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(10, 0, 0)

        path = Path.interpolate(X_0, X_1, speed=1.5)

        self.assertEqual(len(path), 8)
        assert_position_equal(path[1], Position(1.5, 0, 0))
        assert_position_equal(path[-2], Position(9.0, 0, 0))

    def test_straight_vertical(self):
        X_0 = Position(0, 0, 0.5*pi)
        X_1 = Position(0, 10, 0.5*pi)
        speed = 1
        path = Path.interpolate(X_0, X_1, speed=1)

        exp_len_path = 11
        exp_path = [Position(0, i*speed, 0.5*pi) for i in range(exp_len_path)]

        self.assertEqual(len(path), exp_len_path)
        assert_path_equal(path, exp_path)
    
    def test_straight_negative(self):
        X_0 = Position(10, 0, pi)
        X_1 = Position(0, 0, pi)
        speed = 1
        path = Path.interpolate(X_0, X_1, speed=speed)

        exp_len_path = 11
        exp_path = [Position(10 - i*speed, 0, pi) for i in range(exp_len_path)]

        self.assertEqual(len(path), exp_len_path)
        assert_path_equal(path, exp_path)

    def test_straight_negative_vertical(self):
        X_0 = Position(0, 10, 1.5*pi)
        X_1 = Position(0, 0, 1.5*pi)
        speed = 1
        path = Path.interpolate(X_0, X_1, speed=speed)

        exp_len_path = 11
        exp_path = [Position(0, 10 - i*speed, 1.5*pi) for i in range(exp_len_path)]

        self.assertEqual(len(path), exp_len_path)
        assert_path_equal(path, exp_path)
    

class TestGenerateCorner(unittest.TestCase):
    def test_right_up_turn(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(1, 1, 0.5 * pi)

        corner = Path.generate_corner(Path, X_0, X_1)

        assert_position_equal(corner[1], Position(1, 0, 0.5 * pi))

    
if __name__ == "__main__":
    unittest.main()
