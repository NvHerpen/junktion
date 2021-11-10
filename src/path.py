from math import ceil, cos, sin
from typing import List

from src.position import Position


class Path(list):
    CORNER_RADIUS = 3

    def __init__(self, X_0: Position, X_1: Position, speed: float):
        self.X_0 = X_0

        self.pre_calculated_path = self.pre_calculate_path(
            self.X_0,
            X_1,
            speed
        )

    @staticmethod
    def pre_calculate_path(X_0, X_1, speed):
        AB = Path.calculate_AB(X_0, X_1)
        X_a = AB[0]

        if len(AB) == 1:
            return [X_a]
        
        X_b = AB[1]
        
        corner = Path.generate_corner(X_a, X_b, speed)
        exit = Path.interpolate(X_b, X_1, speed)

        return [*corner[:-1], *exit]
        
    @staticmethod
    def calculate_AB(X_0: Position, X_1: Position):
        if X_0.theta == X_1.theta:
            return [X_1]

        X_a = Position(
            X_0.x + (abs(X_1.x - X_0.x) - Path.CORNER_RADIUS) * cos(X_0.theta),
            X_0.y + (abs(X_1.y - X_0.y) - Path.CORNER_RADIUS) * sin(X_0.theta),
            X_0.theta
        )
        
        X_b = Position(
            X_1.x + (Path.CORNER_RADIUS - abs(X_1.x - X_0.x)) * cos(X_1.theta),
            X_1.y + (Path.CORNER_RADIUS - abs(X_1.y - X_0.y)) * sin(X_1.theta),
            X_1.theta
        )

        return [X_a, X_b]
    
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
    def generate_corner(X_a: Position, X_b: Position, speed: float) -> List[Position]:
        corner_angle = abs(X_b.theta - X_a.theta)
        corner_radius = abs(X_b.x - X_a.x)
        L_corner = corner_angle * corner_radius

        n_segments = ceil(L_corner / speed)
        n_positions = n_segments + 1
        
        thetas = [X_a.theta + ((X_b.theta- X_a.theta) / n_positions) * (i + 1) for i in range(n_positions)]
        L_segment = (X_b.x - X_a.x) / sum([cos(theta) for theta in thetas])

        x_i = [X_a.x]
        [x_i.append(x_i[i] + L_segment * cos(thetas[i])) for i in range(n_segments)]

        y_i = [X_a.y]
        [y_i.append(y_i[i] + L_segment * sin(thetas[i])) for i in range(n_segments)]

        return [Position(x_i[i], y_i[i], thetas[i]) for i in range(n_positions)]
