
def natural_sampling(carrier_signal, modulated_signal):
    output = [-1 if carrier > modulated else 1 for carrier, modulated in zip(carrier_signal.out, modulated_signal.out)]
    return output


def uniform_sampling(carrier_signal, modulated_signal, enable_read, read):
    output = []
    old_value = 0
    old_delta = 0
    hold = 0
    output.append(0)
    sampled = [0]
    read_enabled = False
    for y, ym in zip(carrier_signal.out, modulated_signal.out):
        delta = y - old_value

        if old_delta == 0:
            old_delta = delta
            continue
        read_enabled = enable_read(delta, old_delta, read_enabled, y)
        if read_enabled:
            hold, read_enabled = read(read_enabled, ym, y, old_value, hold)

        state = 1
        if hold < y:
            state = -1

        old_delta = delta
        old_value = y
        sampled.append(hold)
        output.append(state)
    return output, sampled


def symmetrical_sampling(carrier_signal, modulated_signal):
    def read(read_enabled, ym, y, old_value, hold):
        if old_value > ym > y:
            hold = ym
            read_enabled = False
        return hold, read_enabled

    def enable_read(delta, old_delta, read_enabled, y):
        if delta * old_delta < 0 < y:
            return True
        return read_enabled

    return uniform_sampling(carrier_signal, modulated_signal, enable_read, read)


def asymmetrical_sampling(carrier_signal, modulated_signal):
    def read(read_enabled, ym, y, old_value, hold):
        if old_value > ym > y or old_value < ym < y:
            hold = ym
            read_enabled = False
        return hold, read_enabled

    def enable_read(delta, old_delta, read_enabled, y):
        if delta * old_delta < 0:
            return True
        return read_enabled

    return uniform_sampling(carrier_signal, modulated_signal, enable_read, read)
