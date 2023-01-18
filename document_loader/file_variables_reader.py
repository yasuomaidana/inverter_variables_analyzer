import pathlib
import re
import math

from typing import Dict

program_path = pathlib.Path(__file__).parent
psim_path = program_path.parent.parent.resolve()
variables_path = psim_path.joinpath(psim_path, "variables")

prefix = {"k": 1000}


def is_number_regex(s):
    """ Returns True if string is a number. """
    if re.match("^\d+?\.\d+?$", s) is None:
        return s.isdigit()
    return True


def value_extractor(word: str):
    number = re.search('(\d+\.?\d*)', word)
    if number is None or re.search('[*+/-]',word):
        return word
    number = number.group()
    reminder = word.replace(number, "")
    number = float(number)
    if reminder != "":
        if "sqrt(" in reminder:
            reminder = reminder[:-1]
            return math.sqrt(value_extractor(reminder))
        number = prefix[reminder] * number
    return number


class Operation:

    def __init__(self, raw_operation: str):
        arguments = re.split('[*+/-]', raw_operation, 1)

        if len(arguments) == 1:
            self.value = value_extractor(arguments[0])
        else:
            self.operator = re.search('[*+/-]', raw_operation).group()
            self.first_operator = value_extractor(arguments[0])
            self.second_operator = value_extractor(arguments[1])
            self.value = None


def read_variables() -> Dict:
    variables = {}
    to_process = set([])
    for variable_file in variables_path.iterdir():
        for variable in variable_file.open().readlines():
            variable = re.sub('(//)(.*)', "", variable).replace("\n", '').replace(" ", '')
            if variable.strip():
                symbol, value = variable.split("=")
                variables[symbol.strip()] = Operation(value)
                to_process.add(symbol.strip())
    return variables


read_variables()
