import math


class Position:
    def __init__(self, x, y, theta) -> None:
        self.x = x
        self.y = y
        self.theta = theta
    
    def __sub__(self, other):
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)
