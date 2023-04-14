from typing import List, Tuple
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


def get_uvw_from_state(state: Tuple[int, ...]):
    u = [delta_u, delta_v, delta_w]
    v = [delta_v, delta_u, delta_w]
    w = [delta_w, delta_v, delta_u]

    u = delta_voltage(state, u)
    v = delta_voltage(state, v)
    w = delta_voltage(state, w)
    return u, v, w


def load_and_compare(state: Tuple[int, ...]):
    u, v, w = get_uvw_from_state(state)
    al, bet, _ = clark(np.array([u, v, w]))

    if not state[0] == 1:
        vectors[state] = tuple((al, bet))
    else:
        negated_state = tuple((1 - i for i in state))
        assert vectors[negated_state] == tuple((-al, -bet))


states = [to_binary_list(state) for state in range(64)]
for state in states:
    load_and_compare(state)


class BigSector:
    zero = (0, 0, 0, 0, 0, 0)

    class Point:
        def __init__(self, origin: Tuple[int, ...], end: List[Tuple[int, ...]]):
            al, bet, _ = clark(np.array(get_uvw_from_state(origin)))
            self.origin = al, bet
            for state in end:
                assert get_uvw_from_state(end[0]) == get_uvw_from_state(state)

            al, bet, _ = clark(np.array(get_uvw_from_state(end[0])))
            self.end = al,
            self.states = end

    def __init__(self):
        self.points = []
        point = self.Point
        s1 = (0, 0, 0, 0, 0, 1)
        s2 = (0, 1, 0, 0, 1, 1)
        self.points.append(point(self.zero, [s1, s2]))

        s1 = (0, 0, 0, 0, 1, 1)
        s2 = (1, 0, 0, 0, 0, 0)
        self.points.append(point(self.zero, [s1, s2]))

        s1 = (1, 0, 0, 0, 0, 1)
        s2 = (1, 1, 0, 0, 1, 1)
        self.points.append(point(self.zero, [s1, s2]))

        s1 = (1, 1, 0, 0, 0, 1)
        self.points.append(point(self.zero, [s1]))

        s1 = (1, 0, 0, 0, 1, 1)
        self.points.append(point(self.zero, [s1]))


sector = BigSector()
print()
