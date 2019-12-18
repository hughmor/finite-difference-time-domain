from three_vector import ThreeVector
from numpy import array


class FDTDPoint:
    def __init__(self, typ='Space'):
        self.type = typ

        # fields
        self.E = ThreeVector()
        self.H = ThreeVector()

        # currents
        self.J = ThreeVector()
        self.M = ThreeVector()

        # densities
        self.sig_e = ThreeVector()
        self.sig_m = ThreeVector()

        # properties
        self.eps_r = 1
        self.mu_r = 1


class FDTDGrid:
    def __init__(self, size=()):
        self.size = size
        self._internalgrid = [[FDTDPoint() for _ in range(size[0])] for _ in range(size[1])]

    def __getitem__(self, item):
        return self._internalgrid[item[1]][item[0]]

    def E(self):
        return array([[self[i, j].E.magnitude() for i in range(self.size[0])] for j in range(self.size[1])])

    def Ex(self):
        return array([[self[i, j].E.x for i in range(self.size[0])] for j in range(self.size[1])])

    def Ey(self):
        return array([[self[i, j].E.y for i in range(self.size[0])] for j in range(self.size[1])])

    def Ez(self):
        return array([[self[i, j].E.z for i in range(self.size[0])] for j in range(self.size[1])])

    def H(self):
        return array([[self[i, j].H.magnitude() for i in range(self.size[0])] for j in range(self.size[1])])

    def Hx(self):
        return array([[self[i, j].H.x for i in range(self.size[0])] for j in range(self.size[1])])

    def Hy(self):
        return array([[self[i, j].H.y for i in range(self.size[0])] for j in range(self.size[1])])

    def Hz(self):
        return array([[self[i, j].H.z for i in range(self.size[0])] for j in range(self.size[1])])




