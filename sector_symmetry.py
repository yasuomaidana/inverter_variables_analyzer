from fractions import Fraction
from functools import reduce
from typing import List, Tuple, Union, Any
from transformations.Clarke import clark
import numpy as np
import matplotlib.pyplot as plt

from voltages_calculator import to_binary_list, delta_voltage, delta_u, delta_v, delta_w


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


def get_number_from_state(state: Tuple[int, ...]):
    return reduce(lambda n, x: n + 2 ** (len(state) - 1 - x[0]) * x[1], enumerate(state), 0)


def load_and_compare(state: Tuple[int], saved_vectors: dict):
    u, v, w = get_uvw_from_state(state)
    al, bet, _ = clark(np.array([u, v, w]))

    if not state[0] == 1:
        saved_vectors[state] = tuple((al, bet))
    else:
        negated_state = tuple((1 - i for i in state))
        assert saved_vectors[negated_state] == tuple((-al, -bet))


class Point:
    def __init__(self, voltage_numbers: Union[int, Tuple[int, ...]]):
        """

        :type voltage_numbers: Voltage number :int or voltage number :list
        """
        self.voltage_numbers = voltage_numbers
        if isinstance(voltage_numbers, int):
            voltage_numbers = tuple([voltage_numbers])

        self.states = [to_binary_list(voltage_number) for voltage_number in voltage_numbers]

        for state in self.states:
            assert get_uvw_from_state(self.states[0]) == get_uvw_from_state(state)
        al, bet, _ = clark(np.array(get_uvw_from_state(self.states[0])))

        self.alpha, self.beta = al, bet

    def symmetric(self):
        negated_states = tuple(negate(state) for state in self.states)
        numbers = tuple(get_number_from_state(ns) for ns in negated_states)
        if len(numbers) == 1:
            numbers = numbers[0]
        return Point(numbers)

    def __sub__(self, other):
        return self.alpha - other.alpha, self.beta - other.beta

    def __str__(self):
        return f"Numbers {self.voltage_numbers}, States {self.states}, Alpha: {self.alpha}, Beta: {self.beta}"

    def state_str(self, show_number: bool = False):
        state_format = "({},{},{})({},{},{})"
        state_str = ""
        if isinstance(self.voltage_numbers, int):
            numbers = [self.voltage_numbers]
        else:
            numbers = self.voltage_numbers

        for state, number in zip(self.states, numbers):
            state_str += state_format.format(*state) + f":{number}\n" if show_number else "\n"

        return state_str


class Vector:
    def __init__(self, origin: Point, end: Point):
        self.origin = origin
        self.end = end
        self.delta_alpha, self.delta_beta = end - origin

    def plot(self):
        return self.origin.alpha, self.origin.beta, self.delta_alpha, self.delta_beta

    def symmetric(self):
        return Vector(self.origin.symmetric(), self.end.symmetric())

    def __str__(self):
        return f"Origin: {self.origin}\nEnd: {self.end}\nDelta Alpha: {self.delta_alpha}, Delta Beta: {self.delta_beta}"


if __name__ == "__main__":
    states = [to_binary_list(state) for state in range(64)]

    vectors = dict()
    for state in states:
        load_and_compare(state, vectors)

    point0 = Point(0)
    point1 = Point((1, 19, 37, 48, 55, 57))
    point2 = Point((3, 32, 39, 41, 50, 59))
    point3 = Point(35)
    point4 = Point((33, 51))
    point5 = Point(49)

    testing_vectors = [Vector(point0, point1), Vector(point0, point2), Vector(point2, point3), Vector(point1, point4),
                       Vector(point1, point5)]

    lims = (-1.75, 1.75)
    plt.xlim(lims)
    plt.ylim(lims)
    i = 0
    for vector in testing_vectors:
        plt.arrow(*vector.plot(), ls=':', color="black")
        plt.annotate("P:" + str(i + 1) + ":\n" + vector.end.state_str(True), xy=(vector.end.alpha, vector.end.beta))
        plt.plot(vector.end.alpha, vector.end.beta, marker="o", color="black")
        print(i, vector)

        # point2 = vector.symmetric()
        #
        # plt.arrow(point2.origin[0], point2.origin[1], point2.end[0] - point2.origin[0],
        #           point2.end[1] - point2.origin[1],
        #           linestyle='--', color="red")
        # plt.annotate(str(i) + "':\n" + point2.states_str(), xy=(point2.end[0], point2.end[1]))
        # plt.plot(point2.end[0], point2.end[1], marker="o", color="red")
        # print(str(i) + "'", point2)

        i += 1

    plt.show()
