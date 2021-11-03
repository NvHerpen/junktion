from math import cos, pi, sin
from typing import List, Tuple

from src.position import Position


class Path(list):
    def __init__(self):
        self.path = []
    
    @staticmethod
    def interpolate(X_0: Position, X_1: Position, speed: float = 1) -> List[Position]:
        x_distance = abs(X_1.x - X_0.x)
        y_distance = abs(X_1.y - X_0.y)

        if speed == 0:
            return [X_0, X_1]

        n_elements = int(max(x_distance, y_distance) / speed)

        positions = [X_0]
        for i in range(n_elements):
            x_0 = positions[i].x
            y_0 = positions[i].y
            theta_0 = X_0.theta

            x_1 = x_0 + speed*cos(theta_0)
            y_1 = y_0 + speed*sin(theta_0)
            theta_1 = X_1.theta

            p_1 = Position(x_1, y_1, theta_1)
            positions.append(p_1)
        
        if X_1 - positions[-1] > 0.001:
            positions.append(X_1)

        return positions

    def generate_corner(self, X_a: Position, X_b: Position, speed: float = 1) -> List[Position]:
        n_segments = 4
        thetas = [X_a.theta + ((X_b.theta - X_a.theta) / n_segments) * n for n in range(n_segments + 1)]

        corner = [X_a]
        for i in range(n_segments):
            X_0 = corner[-1]

            x_1 = X_0.x + speed * cos(thetas[i])
            y_1 = X_0.y + speed * sin(thetas[i])
            theta_1 = thetas[i+1]
            X_1 = Position(x_1, y_1, theta_1)

            segment = self.interpolate(X_0, X_1, speed=speed)
            [corner.append(position) for position in segment[1:]]
        
        return corner