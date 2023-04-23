from fractions import Fraction
from functools import reduce
from typing import List, Tuple, Union, Any
from transformations.Clarke import clark
import numpy as np
import matplotlib.pyplot as plt

from voltages_calculator import to_binary_list, delta_voltage, delta_u, delta_v, delta_w, get_number_from_state, \
    convert_number_to_convention


def negate(or_state) -> Tuple[Union[int, Any], ...]:
    return tuple((1 - gate for gate in or_state))


def get_uvw_from_state(state: Tuple[int, ...]):
    u = [delta_u, delta_v, delta_w]
    v = [delta_v, delta_u, delta_w]
    w = [delta_w, delta_v, delta_u]

    u = delta_voltage(state, u)
    v = delta_voltage(state, v)
    w = delta_voltage(state, w)
    return u, v, w


def load_and_compare(state: Tuple[int], saved_vectors: dict):
    u, v, w = get_uvw_from_state(state)
    al, bet, _ = clark(np.array([u, v, w]))

    if not state[0] == 1:
        saved_vectors[state] = tuple((al, bet))
    else:
        negated_state = tuple((1 - i for i in state))
        assert saved_vectors[negated_state] == tuple((-al, -bet))


class Point:
    def __init__(self, alpha: float, beta: float):
        self.alpha, self.beta = alpha, beta

    def __sub__(self, other):
        return self.alpha - other.alpha, self.beta - other.beta

    def __str__(self):
        return f"Alpha: {self.alpha:0.3f}, Beta: {self.beta:0.3f}"

    def plot(self, plotter=plt, color="black", marker="o", point_message=None):
        plotter.plot(self.alpha, self.beta, marker=marker, color=color)
        if point_message:
            plotter.annotate(point_message, xy=(self.alpha, self.beta))


class PointFromNumber(Point):
    def __init__(self, voltage_numbers: Union[int, Tuple[int, ...]]):
        """

        :type voltage_numbers: Voltage number :int or voltage number :list
        """

        if isinstance(voltage_numbers, int):
            voltage_numbers = tuple([voltage_numbers])

        self.states = [to_binary_list(voltage_number) for voltage_number in voltage_numbers]
        self.voltage_numbers = voltage_numbers

        for state in self.states:
            assert get_uvw_from_state(self.states[0]) == get_uvw_from_state(state)
        al, bet, _ = clark(np.array(get_uvw_from_state(self.states[0])))
        super().__init__(al, bet)

    def symmetric(self):
        negated_states = tuple(negate(state) for state in self.states)
        numbers = tuple(get_number_from_state(ns) for ns in negated_states)
        if len(numbers) == 1:
            numbers = numbers[0]
        return PointFromNumber(numbers)

    def __str__(self):
        return f"Numbers {self.voltage_numbers}, States {self.states}, " + Point.__str__(self)

    def state_str(self, show_number: bool = False):
        state_format = "({},{},{})({},{},{})"
        state_str = ""

        numbers = self.voltage_numbers

        for state, number in zip(self.states, numbers):
            inv1, inv2 = convert_number_to_convention(number)
            state_str += state_format.format(*state) + f":({inv1},{inv2})\n" if show_number else "\n"

        return state_str


class Vector:
    def __init__(self, origin: Point, end: Point):
        self.origin = origin
        self.end = end
        self.delta_alpha, self.delta_beta = end - origin

    def plot(self, plotter=plt, color="black", ls=":", marker="o", show_end=True, end_message=None, show_begin=False,
             begin_message=None):
        to_plot = self.origin.alpha, self.origin.beta, self.delta_alpha, self.delta_beta

        plotter.arrow(*to_plot, ls=ls, color=color)
        if show_end:
            self.end.plot(plotter=plotter, color=color, marker=marker, point_message=end_message)
        if show_begin:
            self.origin.plot(plotter=plotter, color=color, marker=marker, point_message=begin_message)

    def to_array(self):
        return np.array([[self.delta_alpha], [self.delta_beta]])

    def __str__(self):
        al, bet = Fraction(self.origin.alpha).limit_denominator(3), Fraction(self.origin.beta).limit_denominator(3)
        eal, ebet = Fraction(self.end.alpha).limit_denominator(3), Fraction(self.end.beta).limit_denominator(3)
        return f"Origin:\n\t al: {al}, bet: {bet},\nEnd: \n\t al: {eal}, " \
               f"bet: {ebet}\nDelta Alpha: {self.delta_alpha}, Delta Beta: {self.delta_beta}"

    def __mul__(self, other: float):
        n_d_al = other * self.delta_alpha
        n_d_bet = other * self.delta_beta
        new_end = Point(self.origin.alpha + n_d_al, self.origin.beta + n_d_bet)
        return Vector(self.origin, new_end)

    def concatenate(self, other):
        last_al = other.end.alpha
        last_bet = other.end.beta
        end = Point(self.delta_alpha + last_al, self.delta_beta + last_bet)
        return Vector(other.end, end)


class VoltageLevelVector(Vector):
    def __init__(self, origin: PointFromNumber, end: PointFromNumber):
        self.origin = origin
        self.end = end
        super().__init__(origin, end)

    def symmetric(self):
        return VoltageLevelVector(self.origin.symmetric(), self.end.symmetric())


if __name__ == "__main__":
    states = [to_binary_list(state) for state in range(64)]

    vectors = dict()
    for state in states:
        load_and_compare(state, vectors)

    point0 = PointFromNumber(0)
    point1 = PointFromNumber((1, 19, 37, 48, 55, 57))
    point2 = PointFromNumber((3, 32, 39, 41, 50, 59))
    point3 = PointFromNumber(35)
    point4 = PointFromNumber((33, 51))
    point5 = PointFromNumber(49)

    testing_vectors = [VoltageLevelVector(point0, point1), VoltageLevelVector(point0, point2),
                       VoltageLevelVector(point2, point3), VoltageLevelVector(point1, point4),
                       VoltageLevelVector(point1, point5)]

    lims = (-1.75, 1.75)
    plt.xlim(lims)
    plt.ylim(lims)
    i = 0
    for vector in testing_vectors:
        message = "P:" + str(i + 1) + ":\n" + vector.end.state_str(True)
        vector.plot(plotter=plt, end_message=message)

        print("P:" + str(i + 1) + ":\n" + str(vector))
        print(":" * 15)

        vector_s = vector.symmetric()
        message = "P:" + str(i + 1) + "':\n" + vector_s.end.state_str(True)
        vector_s.plot(plotter=plt, color="red", end_message=message)

        print("P:" + str(i + 1) + "':\n" + str(vector_s))
        print("--" * 15)

        i += 1

    plt.show()
