import math
from typing import NamedTuple

class Vector(NamedTuple):
    x: float
    y: float

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def angle(self):
        return math.atan2(self.y, self.x)
    
    def normalize(self):
        if self.magnitude() == float(0):
            return self
        return self / self.magnitude()

    def rotate_vector(self, tetha) -> 'Vector':
        """
        Rotate a 2D vector by a given tetha.

        :param tetha: The tetha in radians by which to rotate the vector.
        :return: The rotated vector.
        """
        cos_theta = math.cos(tetha)
        sin_theta = math.sin(tetha)

        self.x = self.x * cos_theta - self.y * sin_theta,
        self.y = self.x * sin_theta + self.y * cos_theta

        return self
