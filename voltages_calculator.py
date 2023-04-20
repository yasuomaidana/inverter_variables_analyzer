from typing import List
from typing import Tuple
from fractions import Fraction

import matplotlib.pyplot as plt

from transformations.Clarke import clark
import numpy as np

delta_u = 0, 3
delta_v = 1, 4
delta_w = 2, 5


def to_binary_list(number: int) -> Tuple[int]:
    return tuple([int(bit) for bit in "{0:06b}".format(number)])


def get_delta(state: Tuple[int, ...], delta: Tuple[int, int]) -> float:
    gate_1 = delta[0]
    gate_2 = delta[1]
    voltage_1 = 1 / 2 if state[gate_1] == 1 else -1 / 2
    voltage_2 = 1 / 2 if state[gate_2] == 1 else -1 / 2
    return voltage_1 - voltage_2


def delta_voltage(state: Tuple[int, ...], order: List[Tuple[int, int]]) -> float:
    delta_x = get_delta(state, order[0])
    delta_y = get_delta(state, order[1])
    delta_z = get_delta(state, order[2])
    return 2 / 3 * delta_x - 1 / 3 * (delta_y + delta_z)


def print_voltages(state: Tuple[int], voltage_number: int):
    u = [delta_u, delta_v, delta_w]
    v = [delta_v, delta_u, delta_w]
    w = [delta_w, delta_v, delta_u]

    u = Fraction(delta_voltage(state, u)).limit_denominator(6)
    v = Fraction(delta_voltage(state, v)).limit_denominator(6)
    w = Fraction(delta_voltage(state, w)).limit_denominator(6)

    al, bet, _ = clark(np.array([u, v, w]))

    p_labels = points.get((al, bet), list())
    p_labels.append(label_format.format(*tuple(state)) + f":{voltage_number}")

    points[(al, bet)] = p_labels

    al, bet = Fraction(al).limit_denominator(3), Fraction(bet).limit_denominator(3)

    alphas.append(al)
    betas.append(bet)

    to_print = tuple(state) + (str(u), str(v), str(w)) + (str(al), str(bet))
    print(table_format.format(*to_print))


if __name__ == "__main__":
    table_format = " {:<4} " * 6 + " | " + " {:<4} " * 3 + " | " + " {:<4} " * 2
    header = table_format.format("U1", "V2", "W1", "U2", "V2", "W2", "U", "V", "W", "alp", "bet")
    label_format = "({},{},{})({},{},{})"
    labels = []
    alphas = []
    betas = []
    points = dict()

    states = [to_binary_list(state) for state in range(64)]
    print(header)
    n = 0
    for i in states:
        print_voltages(i, n)
        n += 1
    plt.scatter(alphas, betas)

    i = 0
    for alpha, beta in points.keys():
        text = "\n".join(points[(alpha, beta)])
        plt.annotate(text, (alpha, beta))
        print("{} labels:{}".format(i, points[(alpha, beta)]))
        i += 1

    plt.show()
