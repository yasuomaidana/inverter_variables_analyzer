from typing import List, Tuple
from typing import Tuple
from fractions import Fraction
from transformations.Clarke import clark
import numpy as np

delta_u = 0, 3
delta_v = 1, 4
delta_w = 2, 5

vectors = dict()


def to_binary_list(number: int) -> Tuple[int, ...]:
    return tuple([int(i) for i in "{0:06b}".format(number)])


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


def load_and_compare(state: Tuple[int, ...]):
    u = [delta_u, delta_v, delta_w]
    v = [delta_v, delta_u, delta_w]
    w = [delta_w, delta_v, delta_u]

    u = Fraction(delta_voltage(state, u)).limit_denominator(6)
    v = Fraction(delta_voltage(state, v)).limit_denominator(6)
    w = Fraction(delta_voltage(state, w)).limit_denominator(6)

    al, bet, _ = clark(np.array([u, v, w]))

    if not state[0] == 1:
        vectors[state] = tuple((al, bet))
    else:
        negated_state = tuple((1 - i for i in state))
        print("Symmetry in {} and {} at {}".format(negated_state, state, vectors[negated_state]))
        assert vectors[negated_state] == tuple((-al, -bet))


states = [to_binary_list(state) for state in range(64)]
for state in states:
    load_and_compare(state)
