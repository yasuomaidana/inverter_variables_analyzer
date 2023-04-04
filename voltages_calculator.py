from typing import List
from typing import Tuple
from fractions import Fraction

delta_u = 0, 3
delta_v = 1, 4
delta_w = 2, 5

table_format = " {:<4} " * 6 + " | " + " {:<4} " * 3
header = table_format.format("U1", "V2", "W1", "U2", "V2", "W2", "U", "V", "W")


def to_binary_list(number: int) -> List[int]:
    return [int(i) for i in "{0:06b}".format(number)]


def get_delta(state: List[int], delta: Tuple[int, int]) -> float:
    gate_1 = delta[0]
    gate_2 = delta[1]
    voltage_1 = 1 / 2 if state[gate_1] == 1 else -1 / 2
    voltage_2 = 1 / 2 if state[gate_2] == 1 else -1 / 2
    return voltage_1 - voltage_2


def delta_voltage(state: List[int], order: List[Tuple[int, int]]) -> float:
    delta_x = get_delta(state, order[0])
    delta_y = get_delta(state, order[1])
    delta_z = get_delta(state, order[2])
    return 2 / 3 * delta_x - 1 / 3 * (delta_y + delta_z)


def print_voltages(state: List[int]):
    u = [delta_u, delta_v, delta_w]
    v = [delta_v, delta_u, delta_w]
    w = [delta_w, delta_v, delta_u]
    U = Fraction(delta_voltage(state, u)).limit_denominator(6)
    V = Fraction(delta_voltage(state, v)).limit_denominator(6)
    W = Fraction(delta_voltage(state, w)).limit_denominator(6)

    to_print = tuple(state) + (str(U), str(V), str(W))
    print(table_format.format(*to_print))


states = [to_binary_list(state) for state in range(64)]
print(header)
for i in states:
    print_voltages(i)
