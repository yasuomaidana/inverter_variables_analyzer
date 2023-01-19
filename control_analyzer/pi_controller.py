from control.matlab import tf


class PIController:

    def __init__(self, gain: float, time_constant: float):
        self.transfer_function = gain * tf([time_constant, 1.0], [time_constant, 0.0])
