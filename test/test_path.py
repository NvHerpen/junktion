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
    SPEED = 0.3
    N_POINTS = 7
    L_SEGMENT = 0.253960
    DELTA_THETA = 0.2243994

    def test_1_segment(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(1, 1, 0.5 * pi)
        speed = 2   # Make speed so high, that 1 frame already encompasses total corner length

        corner = Path.generate_corner(X_0, X_1, speed)
        exp_p0 = Position(0, 0, 0.25 * pi)
        exp_p1 = Position(1, 1, 0.5 * pi)

        assert_path_equal(corner, [exp_p0, exp_p1])

    def test_low_speed(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(1, 1, 0.5 * pi)

        corner = Path.generate_corner(X_0, X_1, self.SPEED)

        exp_p_1 = Position(
            self.L_SEGMENT * cos(self.DELTA_THETA),
            self.L_SEGMENT * sin(self.DELTA_THETA),
            2 * self.DELTA_THETA
        )
        exp_p_m2 = Position(
            1 - self.L_SEGMENT * sin(self.DELTA_THETA),
            1 - self.L_SEGMENT * cos(self.DELTA_THETA),
            0.5 * pi - self.DELTA_THETA
        )

        self.assertEqual(len(corner), self.N_POINTS)
        assert_position_equal(corner[1], exp_p_1, places=3)
        assert_position_equal(corner[-2], exp_p_m2, places=3)
        assert_position_equal(corner[-1], X_1, places=3)
    
    def test_left_down_corner(self):
        X_0 = Position(1, 1, pi)
        X_1 = Position(0, 0, 1.5 * pi)

        corner = Path.generate_corner(X_0, X_1, self.SPEED)

        exp_p_1 = Position(
            1 - self.L_SEGMENT * cos(self.DELTA_THETA), 
            1 - self.L_SEGMENT * sin(self.DELTA_THETA), 
            pi + 2 * self.DELTA_THETA
        )
        exp_p_m1 = Position(
            self.L_SEGMENT * sin(self.DELTA_THETA),
            self.L_SEGMENT * cos(self.DELTA_THETA),
            1.5 * pi - self.DELTA_THETA
        )

        assert_position_equal(corner[1], exp_p_1, places=3)
        assert_position_equal(corner[-2], exp_p_m1, places=3)


class TestCalculateAB(unittest.TestCase):
    def test_straight_path(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(10, 0, 0)

        AB = Path.calculate_AB(X_0, X_1)

        self.assertEqual(len(AB), 1)
        assert_position_equal(AB[0], X_1)
        
    def test_corner_right_up(self):
        X_0 = Position(2, 0, 0)
        X_1 = Position(8, 8, 0.5 * pi)

        AB = Path.calculate_AB(X_0, X_1)

        exp_x_a = Position(5, 0, 0)
        exp_x_b = Position(8, 3, 0.5 * pi)

        self.assertEqual(len(AB), 2)
        assert_position_equal(AB[0], exp_x_a)
        assert_position_equal(AB[1], exp_x_b)
    
    def test_down_left(self):
        X_0 = Position(4, 5, 1.5 * pi)
        X_1 = Position(-2, -1, pi)

        AB = Path.calculate_AB(X_0, X_1)

        exp_x_a = Position(4, 2, 1.5 * pi)
        exp_x_b = Position(1, -1, pi)

        self.assertEqual(len(AB), 2)
        assert_position_equal(AB[0], exp_x_a)
        assert_position_equal(AB[1], exp_x_b)


class TestPreCalculatePath(unittest.TestCase):
    def test_straight_path(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(10, 0, 0)

        path = Path.pre_calculate_path(X_0, X_1, 1)

        assert_path_equal(path, [X_1])
    
    def test_corner_right_up(self):
        X_0 = Position(0, 0, 0)
        X_1 = Position(10, 10, 0.5 * pi)
        speed = 1

        pre_calculated_path = Path.pre_calculate_path(X_0, X_1, speed)

        exp_n_positions = 13
        exp_x_a = Position(10 - Path.CORNER_RADIUS, 0, 0.2617)
        exp_x_b = Position(10, Path.CORNER_RADIUS, 0.5 * pi)
        exp_x_b_1 = Position(10, Path.CORNER_RADIUS + 1, 0.5 * pi) 
        exp_x_b_m2 = Position(10, 9, 0.5 * pi)

        self.assertEqual(len(pre_calculated_path), exp_n_positions)
        assert_position_equal(pre_calculated_path[0], exp_x_a, places=3)
        assert_position_equal(pre_calculated_path[5], exp_x_b)
        assert_position_equal(pre_calculated_path[6], exp_x_b_1)
        assert_position_equal(pre_calculated_path[-2], exp_x_b_m2)


if __name__ == "__main__":
    unittest.main()
