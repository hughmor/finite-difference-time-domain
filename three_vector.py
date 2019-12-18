from cmath import sqrt


class ThreeVector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return ThreeVector(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return ThreeVector(x, y, z)

    def __mul__(self, other):
        x = other * self.x
        y = other * self.y
        z = other * self.z
        return ThreeVector(x, y, z)

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)
