import unittest
from src.position import Position

class TestPosition(unittest.TestCase):
    def test_position(self):
        p = Position(1, 2, 3)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        self.assertEqual(p.theta, 3)
    
    def test_sub(self):
        a = Position(3, 4, 0)
        b = Position(6, 8, 0)
        self.assertAlmostEqual(b-a, 5)