import unittest
from math import cos, pi, sin

from src.path import Path, RightAngleException
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
    def test_no_corner(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(1, 1, 0.5 * pi)

        with self.assertRaises(RightAngleException):
            _ = Path.generate_corner(X_0, X_1, n_segments=0)
    
    def test_1_segment(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(1, 1, 0.5 * pi)

        corner = Path.generate_corner(X_0, X_1, n_segments=1)
        exp_p0 = Position(0, 0, 0.25 * pi)
        exp_p1 = Position(1, 1, 0.5 * pi)

        assert_path_equal(corner, [exp_p0, exp_p1])

    def test_2_segments(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(1, 1, 0.5 * pi)
        n_segments = 2

        corner = Path.generate_corner(X_0, X_1, n_segments=n_segments)

        exp_theta0 = (0.5 * pi) * (1 / 3)
        exp_theta1 = (0.5 * pi) * (2 / 3)
        exp_L = 1/(cos(exp_theta0) + cos(exp_theta1))
        exp_p0 = Position(0, 0, exp_theta0)
        exp_p1 = Position(exp_L * cos(exp_theta0), exp_L * sin(exp_theta0), exp_theta1)
        exp_p2 = Position(1, 1, 0.5 * pi)

        assert_path_equal(corner, [exp_p0, exp_p1, exp_p2])
    
    def test_10_segments(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(1, 1, 0.5 * pi)

        corner = Path.generate_corner(X_0, X_1)

        exp_L = 0.15406
        exp_theta_0 = 0.14279
        exp_p_1 = Position(0.15249, 0.02192, 0.28559)

        exp_theta_m1 = 0.5 * pi - exp_theta_0
        exp_p_m1 = Position(1 - exp_L * cos(exp_theta_m1), 1 - exp_L * sin(exp_theta_m1), exp_theta_m1)

        assert_position_equal(corner[1], exp_p_1, places=3)
        assert_position_equal(corner[-2], exp_p_m1, places=3)

    
if __name__ == "__main__":
    unittest.main()
