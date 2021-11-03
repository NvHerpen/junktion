import unittest
from math import cos, pi, sin

from src.path import Path
from src.position import Position

def compare_paths(path, exp_path):
    tc = unittest.TestCase()

    for i in range(len(path)):
        tc.assertAlmostEqual(path[i].x, exp_path[i].x)
        tc.assertAlmostEqual(path[i].y, exp_path[i].y)
        tc.assertAlmostEqual(path[i].theta, exp_path[i].theta)


class TestInterpolate(unittest.TestCase):
    def test_zero_zero(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(0, 0, 0)
        path = Path.interpolate(X_0, X_1, speed=0)

        exp_path = [Position(0, 0, 0), Position(0, 0, 0)]

        compare_paths(path, exp_path)
    
    def test_straight_horizontal(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(10, 0, 0)
        path = Path.interpolate(X_0, X_1, speed=1)

        exp_len_path = 11
        exp_path = [Position(i, 0, 0) for i in range(exp_len_path)]

        self.assertEqual(len(path), exp_len_path)
        compare_paths(path, exp_path)
    
    def test_straight_horizontal_fast(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(10, 0, 0)
        speed = 2
        path = Path.interpolate(X_0, X_1, speed=speed)

        exp_len_path = 6
        exp_path = [Position(i*speed, 0, 0) for i in range(exp_len_path)]

        self.assertEqual(len(path), exp_len_path)
        compare_paths(path, exp_path)

    def test_float_speed(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(10, 0, 0)
        speed = 1.5
        path = Path.interpolate(X_0, X_1, speed=speed)

        exp_len_path = 8
        self.assertEqual(len(path), exp_len_path)
        
        exp_pos_1 = Position(1.5, 0, 0)
        exp_pos_m2 = Position(9.0, 0, 0)
        self.assertAlmostEqual(path[1], exp_pos_1)
        self.assertAlmostEqual(path[-2], exp_pos_m2)

    def test_straight_vertical(self):
        X_0 = Position(0, 0, 0.5*pi)
        X_1 = Position(0, 10, 0.5*pi)
        speed = 1
        path = Path.interpolate(X_0, X_1, speed=speed)

        exp_len_path = 11
        exp_path = [Position(0, i*speed, 0.5*pi) for i in range(exp_len_path)]

        self.assertEqual(len(path), exp_len_path)
        compare_paths(path, exp_path)
    
    def test_straight_negative(self):
        X_0 = Position(10, 0, pi)
        X_1 = Position(0, 0, pi)
        speed = 1
        path = Path.interpolate(X_0, X_1, speed=speed)

        exp_len_path = 11
        exp_path = [Position(10 - i*speed, 0, pi) for i in range(exp_len_path)]

        self.assertEqual(len(path), exp_len_path)
        compare_paths(path, exp_path)

    def test_straight_negative_vertical(self):
        X_0 = Position(0, 10, 1.5*pi)
        X_1 = Position(0, 0, 1.5*pi)
        speed = 1
        path = Path.interpolate(X_0, X_1, speed=speed)

        exp_len_path = 11
        exp_path = [Position(0, 10 - i*speed, 1.5*pi) for i in range(exp_len_path)]

        self.assertEqual(len(path), exp_len_path)
        compare_paths(path, exp_path)
    

class TestGenerateCorner(unittest.TestCase):
    def test_right_up_turn(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(123, 123, 0.5 * pi)

        speed = 1
        n_segments = 4

        path = Path()
        corner = path.generate_corner(X_0, X_1, speed=speed)

        exp_len_corner = 5
        self.assertEqual(len(corner), exp_len_corner)

        thetas = [X_0.theta + ((X_1.theta - X_0.theta) / n_segments) * n for n in range(n_segments + 1)]
        corner_width = speed * sum([cos(t) for t in thetas])

        # Test point 1
        self.assertAlmostEqual(corner[1].theta, 0.5 * pi / n_segments)
        self.assertAlmostEqual(corner[1].x, 1.0)
        self.assertAlmostEqual(corner[1].y, 0.0)

        # Test point -1
        self.assertAlmostEqual(corner[-2].theta, (3/4) * (0.5 * pi))
        self.assertAlmostEqual(corner[-1].x, corner_width - cos(0.5 * pi))
        self.assertAlmostEqual(corner[-1].y, corner_width - sin(0.5 * pi))

    def test_down_left_turn(self):
        X_0 = Position(0, 0, 1.5 * pi)
        X_1 = Position(123, 123, pi)
        speed = 1
        n_segments = 4

        path = Path()
        corner = path.generate_corner(X_0, X_1, speed=speed)

        exp_len_corner = 5
        self.assertEqual(len(corner), exp_len_corner)

        thetas = [X_0.theta + ((X_1.theta - X_0.theta) / n_segments) * n for n in range(n_segments + 1)]
        corner_width = abs(speed * sum([cos(t) for t in thetas]))

        # Test point 1
        theta_1 = 1.5 * pi - 0.5 * pi / 4
        self.assertAlmostEqual(corner[1].theta, theta_1)
        self.assertAlmostEqual(corner[1].x, 0.0)
        self.assertAlmostEqual(corner[1].y, -1.0)

        # Test point -1
        theta_m2 = pi + 0.5 * pi / 4
        self.assertAlmostEqual(corner[-2].theta, theta_m2)
        self.assertAlmostEqual(corner[-1].x, -corner_width - cos(pi))
        self.assertAlmostEqual(corner[-1].y, -corner_width)
    
if __name__ == "__main__":
    unittest.main()
