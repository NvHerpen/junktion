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
    
    @staticmethod
    def generate_corner(X_a: Position, X_b: Position, n_segments: int = 0) -> List[Position]:
        # if n_segments == 0:
        #     return []
        
        n_positions = n_segments + 1
        
        thetas = [((X_b.theta- X_a.theta) / n_positions) * (i + 1) for i in range(n_positions)]
        
        L_segment = (X_b.x - X_a.x) / sum([cos(theta) for theta in thetas])

        x_i = [X_a.x]
        [x_i.append(x_i[i] + L_segment * cos(thetas[i])) for i in range(n_segments)]

        y_i = [X_a.y]
        [y_i.append(y_i[i] + L_segment * sin(thetas[i])) for i in range(n_segments)]

        return [Position(x_i[i], y_i[i], thetas[i]) for i in range(n_positions)]

    @staticmethod
    def generate_corner2(self, X_a: Position, X_b: Position, speed: float = 1, n_segments: int = 2) -> List[Position]:
        x_i = X_a.x + cos(X_a.theta)*speed
        y_i = X_a.y + sin(X_a.theta)*speed
        theta_i = X_b.theta
        X_i = Position(x_i, y_i, theta_i)

        segment_1 = self.interpolate(X_a, X_i, speed=speed)
        segment_2 = self.interpolate(X_i, X_b, speed=speed)
        
        return [X_a, *segment_1[1:], *segment_2[1:]]