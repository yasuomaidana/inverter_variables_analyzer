from control_analyzer.pi_controller import PIController
from document_loader.file_variables_reader import read_variables
from control.matlab import *
import matplotlib.pyplot as plt

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    variables = read_variables()
    pi_q = PIController(variables["PI_gain_q"].value, variables["PI_time_constant_q"].value)

    yout, T = step(pi_q.transfer_function)
    plt.plot(T.T, yout.T)
    plt.show()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
