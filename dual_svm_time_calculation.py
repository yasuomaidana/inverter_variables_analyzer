import numpy
from numpy import arctan2, radians
from typing import Tuple, Optional

from sector_symmetry import BigSector


class BigSectorWithCalculator(BigSector):

    def __init__(self, lower_angle=0.0, upper_angle=60.0):
        super().__init__()
        self.sub_sectors = [(0, 1, 2), (1, 3, 2), (1, 4, 3), (2, 3, 5)]
        self.lower_angle = radians(lower_angle)
        self.upper_angle = radians(upper_angle)

    def find_times(self, alpha: float, beta: float) -> Optional[Tuple[int, int]]:
        theta = arctan2(beta, alpha)
        theta = theta if theta > 0 else theta + 2 * numpy.pi

        if theta > self.upper_angle or theta < self.lower_angle:
            return None

        return 0, 0


sector = BigSectorWithCalculator()
test = 0.5, .5
assert sector.find_times(*test) is not None
test = 0, -.5
assert sector.find_times(*test) is None
