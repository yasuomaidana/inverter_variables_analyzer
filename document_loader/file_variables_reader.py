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
    if number is None or re.search('[*+/-]', word):
        return word
    number = number.group()
    reminder = word.replace(number, "")
    number = float(number)
    if reminder != "":
        if "sqrt(" in reminder:
            return math.sqrt(number)
        number = prefix[reminder] * number
    return number


class Operation:

    def __init__(self, raw_operation: str):
        self.value = None
        self.symbol = None
        if raw_operation[0] == "(":
            raw_operation = raw_operation[1:-1]
        arguments = re.split('[*+/-]', raw_operation, 1)
        if len(arguments) == 1:
            value = value_extractor(arguments[0])
            if isinstance(value, float):
                self.value = value
            else:
                self.symbol = value
        else:
            self.operator = re.search('[*+/-]', raw_operation).group()
            self.first_operator = Operation(arguments[0])
            self.second_operator = Operation(arguments[1])

    def get_symbols(self) -> set:
        symbols = set()
        if self.value:
            return symbols
        if self.symbol:
            symbols.add(self.symbol)
            return symbols
        symbols = symbols.union(self.first_operator.get_symbols())
        symbols = symbols.union(self.second_operator.get_symbols())
        return symbols

    def get_value(self, values: dict):
        constants = {"pi": math.pi}
        if self.symbol in constants:
            return constants[self.symbol]
        if self.value:
            return self.value
        if self.symbol:
            return values[self.symbol].value
        op = {'+': lambda x, y: x + y,
              '-': lambda x, y: x - y,
              '*': lambda x, y: x * y,
              '/': lambda x, y: x / y
              }
        self.value = op[self.operator](self.first_operator.get_value(values), self.second_operator.get_value(values))
        return self.value


def read_variables() -> Dict:
    variables = {}
    to_process = set()
    for variable_file in variables_path.iterdir():
        for variable in variable_file.open().readlines():
            variable = re.sub('(//)(.*)', "", variable).replace("\n", '').replace(" ", '')
            if variable.strip():
                symbol, value = variable.split("=")
                variables[symbol.strip()] = Operation(value)
                if variables[symbol.strip()].value is None:
                    to_process.add(symbol.strip())
    while len(to_process) > 0:
        for processing in to_process.copy():
            if not variables[processing].get_symbols().intersection(to_process):
                variables[processing].get_value(variables)
                to_process.remove(processing)
    return variables
