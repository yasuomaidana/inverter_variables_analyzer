import matplotlib.pyplot as plt
from typing import Tuple
from math import cos, sin, radians


def draw_sectors(origin: Tuple[float, float] = (0, 0)):
    for i in range(6):
        x = [origin[0], origin[0] + cos(radians(i * 60))]
        y = [origin[1], origin[1] + sin(radians(i * 60))]
        plt.plot(x, y, linestyle='dashed', color="black")


def draw_all_sectors():
    for i in range(6):
        x = cos(radians(i * 60))
        y = sin(radians(i * 60))
        print(x, y)
        draw_sectors((x, y))


draw_all_sectors()
plt.show()
