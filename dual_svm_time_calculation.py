import numpy as np
from typing import Tuple, Optional
from matplotlib import pyplot as plt
from sector_symmetry import PointFromNumber, Point, VoltageLevelVector, Vector

point0 = PointFromNumber(0)
point1 = PointFromNumber((1, 19, 37, 48, 55, 57))
point2 = PointFromNumber((3, 32, 39, 41, 50, 59))
point3 = PointFromNumber(35)
point4 = PointFromNumber((33, 51))
point5 = PointFromNumber(49)


class Space:
    def __init__(self, point_a: PointFromNumber, point_b: PointFromNumber, point_c: PointFromNumber):
        self.A = point_a
        self.B = point_b
        self.C = point_c
        ab = VoltageLevelVector(point_a, point_b)
        ac = VoltageLevelVector(point_a, point_c)
        bc = VoltageLevelVector(point_b, point_c)
        self.voltage_vectors = [ab, ac, bc]

        self.space = np.vstack((ab.to_array().reshape(1, -1), ac.to_array().reshape(1, -1))).reshape(2, 2).transpose()

    def calculate_components(self, point: Point) -> Tuple[float, float]:
        u, v = np.linalg.solve(self.space, Vector(self.A, point).to_array())
        return u[0], v[0]

    def __str__(self):
        return f"A {self.A}\nB {self.B}\nC {self.C}"

    def plot(self, plotter=plt, color="black", ls=":", marker="o", end_message=None):
        for vector in self.voltage_vectors:
            vector.plot(plotter=plotter, color=color, ls=ls, marker=marker, end_message=end_message)
        self.A.plot(plotter, color, marker)


class Sector(Space):
    zero = PointFromNumber(0)

    def __init__(self, p1, p2, p3, p4, p5):
        z = self.zero
        super().__init__(z, p5, p3)
        self.sub_sectors = [Space(z, p2, p1), Space(p2, p3, p4), Space(p1, p2, p4), Space(p1, p4, p5)]

    def plot(self, plotter=plt, color="black", ls=":", marker="o", end_message=None):
        for sector in self.sub_sectors:
            sector.plot(plotter, color, ls, marker, end_message)

    def find_components(self, point: Point) -> Optional[Tuple[float, float, Space]]:
        t1, t2 = self.calculate_components(point)
        if t1 > 1 or t2 > 1 or t1 < 0 or t2 < 0:
            return None
        for sub_sector in self.sub_sectors:
            t1, t2 = sub_sector.calculate_components(point)
            if t1 + t2 > 1 or t1 < 0 or t2 < 0:
                continue
            return t1, t2, sub_sector


def check_in_sector(sub_sector: Sector, point_to_test: Point):
    found = sub_sector.find_components(point_to_test)
    if found is None:
        point_to_test.plot(marker="x", color="red", point_message="outside")
        return
    u, v, sect = found
    u_component = sect.voltage_vectors[0] * u
    v_component = sect.voltage_vectors[1] * v
    u_component.plot(color="blue", marker=None)
    found = v_component.concatenate(u_component)
    found.plot(color="blue")
    found.end.plot(color="blue", point_message=f"({found.end.alpha:0.2f},{found.end.beta:0.2f})\nv1:{u:0.3f} v2:{v:0.3f}")


if __name__ == "__main__":
    sub_sector_test = Sector(point1, point2, point3, point4, point5)
    sub_sector_test.plot()

    x = Point(0.1, 0.2)
    check_in_sector(sub_sector_test, x)

    x2 = Point(point1.alpha * .2, point1.beta * .6)
    check_in_sector(sub_sector_test, x2)

    x3 = Point(point1.alpha * .5, point1.beta * .5)
    check_in_sector(sub_sector_test, x3)

    x4 = Point(0.75, 0.4)
    check_in_sector(sub_sector_test, x4)

    x4 = Point(0.75, 0.8)
    check_in_sector(sub_sector_test, x4)

    check_in_sector(sub_sector_test, point5)

    x6 = Point(1.25, 0.2)
    check_in_sector(sub_sector_test, x6)

    x7 = Point(0.5, 0.2)
    check_in_sector(sub_sector_test, x7)

    x7 = Point(1.5, 0.8)
    check_in_sector(sub_sector_test, x7)

    x9 = Point(1.5, -0.3)
    check_in_sector(sub_sector_test, x9)

    plt.show()
