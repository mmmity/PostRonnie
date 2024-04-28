'''
Implementation of basic interpreter. Class Interpreter is used to interpret code
'''
from __future__ import annotations
from typing import List

from .dllist import DLList, nxt, prv
from .line_parser import LineParser, ParseResults


class EndOfProgram(Exception):
    '''
    Is thrown when program reaches the end
    '''


class UndefinedError(Exception):
    '''
    Is thrown when program reaches the maximum steps count
    The return value is considered undefined
    '''


class Interpreter:
    '''
    Implementation of interpreter
    '''
    MAX_STEP_COUNT = 1000
    def __init__(self, input_str: str, program: List[str]):
        '''
        Initializes dllist of bools as current data and program as list of commands
        '''
        self.data = DLList()
        self.step_count = 0
        for c in input_str:
            if c == '1':
                self.data.push_back(True)
            elif c == '0':
                self.data.push_back(False)
            else:
                raise ValueError('Weird input')

        self.carriage: DLList.Iterator = self.data.begin()

        self.program = program

        try:
            self.current_index = program.index('BEGIN')
        except ValueError as e:
            raise SyntaxError('Failed to parse the program: no BEGIN keyword') from e

        self.current_index += 1

    def interpret_current_line(self):
        '''
        Interprets current line, changes data, moves carriage and line accordingly
        '''
        if self.current_index >= len(self.program) or self.current_index < 0:
            raise SyntaxError('Failed to parse the program:' +
                              f'line {self.current_index + 1} does not exist')

        if self.program[self.current_index] == 'END':
            raise EndOfProgram()
    
        self.step_count += 1
        if (self.step_count >= self.MAX_STEP_COUNT):
            raise UndefinedError()

        results: ParseResults = LineParser.parse(
            self.program[self.current_index],
            self.current_index + 1,
            self.carriage.get_value()
        )
            

        self.carriage.set_value(results.newval)

        if results.delta == -1:
            if self.carriage == self.data.begin():
                self.data.push_front(False)
            self.carriage = prv(self.carriage)
        elif results.delta == 1:
            if self.carriage == prv(self.data.end()):
                self.data.push_back(False)
            self.carriage = nxt(self.carriage)

        self.current_index = results.newline - 1

    def get_results(self) -> str:
        '''
        Returns pretty formatted string as result
        '''
        while not self.data.empty() and not self.data.back():
            self.data.pop_back()
        self.data.push_back(False)

        while not self.data.empty() and not self.data.front():
            self.data.pop_front()
        self.data.push_front(False)

        out_arr = []
        iterator = self.data.begin()
        while iterator != self.data.end():
            out_arr.append(str(int(iterator.get_value())))
            iterator = nxt(iterator)

        return ''.join(out_arr)

    def debug(self) -> str:
        '''
        Prints formatted current data
        '''
        out_arr = []
        iterator = self.data.begin()
        while iterator != self.data.end():
            strval = str(int(iterator.get_value()))
            if iterator == self.carriage:
                out_arr.append('\033[94m\033[1m' + strval + '\033[0m')
            else:
                out_arr.append(strval)
            iterator = nxt(iterator)

        return ''.join(out_arr) + f' on line {self.current_index + 1}'

    @staticmethod
    def load_from_files(input_file: str, program_file: str) -> Interpreter:
        '''
        Loads input from input_file, program from program_file
        '''
        with open(input_file, 'r') as f:
            inp = f.read().strip()

        with open(program_file, 'r') as f:
            program = f.read().split('\n')
            # print(program)

        return Interpreter(inp, program)
