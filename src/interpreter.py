from __future__ import annotations
from dllist import DLList, next, prev
from line_parser import LineParser, ParseResults
from typing import List
import time


class SyntaxError(Exception):
    pass


class EndOfProgram(Exception):
    pass


class Interpreter:
    def __init__(self, input: str, program: List[str]):
        self.data = DLList()
        for c in input:
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
        except ValueError:
            raise SyntaxError('Failed to parse the program: no BEGIN keyword')
        
        self.current_index += 1
    
    def interpret_current_line(self):
        print(self.current_index)
        if self.program[self.current_index] == 'END':
            raise EndOfProgram()

        try:
            results: ParseResults = LineParser.parse(self.program[self.current_index], self.current_index + 1, self.carriage.get_value())
        except IndexError:
            raise SyntaxError(f'Failed to parse the program: line {self.current_index + 1} does not exist')

        self.carriage.set_value(results.newval)

        if results.delta == -1:
            if self.carriage == self.data.begin():
                self.data.push_front(False)
            self.carriage = prev(self.carriage)
        elif results.delta == 1:
            if self.carriage == prev(self.data.end()):
                self.data.push_back(False)
            self.carriage = next(self.carriage)
        
        self.current_index = results.newline - 1
    
    def get_results(self) -> str:

        while not self.data.empty() and self.data.back() == False:
            self.data.pop_back()
        self.data.push_back(False)

        while not self.data.empty() and self.data.front() == False:
            self.data.pop_front()
        self.data.push_front(False)

        out_arr = []
        iter = self.data.begin()
        while iter != self.data.end():
            out_arr.append(str(int(iter.get_value())))
            iter = next(iter)

        return ''.join(out_arr)

    def debug(self) -> str:

        out_arr = []
        iter = self.data.begin()
        while iter != self.data.end():
            if iter == self.carriage:
                out_arr.append('C')
            out_arr.append(str(int(iter.get_value())))
            iter = next(iter)

        return ''.join(out_arr)
    
    def load_from_files(input_file: str, program_file: str) -> Interpreter:
        with open(input_file, 'r') as f:
            inp = f.read().strip()
        
        with open(program_file, 'r') as f:
            program = f.read().split('\n')
            # print(program)
        
        return Interpreter(inp, program)


inter: Interpreter = Interpreter.load_from_files('input', 'examples/mod.post')

while True:
    try:
        inter.interpret_current_line()
        print(inter.debug())
        time.sleep(0.5)
    except EndOfProgram:
        break

print(inter.get_results())
