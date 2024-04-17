'''
Implementation of class that parses lines.
'''
from dataclasses import dataclass
from typing import List

@dataclass
class ParseResults:
    '''
    Is returned from method parse()
    delta: where to move carriage
    newline: where to move code pointer
    newval: what to write under the carriage
    '''
    delta: int
    newline: int
    newval: bool


class ParseError(Exception):
    '''
    Is raised when line parser encounters error
    '''


class LineParser:
    '''
    Implementation of line parser, which can parse() each line independently
    '''
    @staticmethod
    def parse(line: str, line_number: int, current_value: bool) -> ParseResults:
        '''
        Parses line independently, returns ParseResults
        '''
        comment_start = line.find('#')
        if comment_start != -1:
            line = line[:comment_start]

        vals = line.split()
        if len(vals) == 0:
            raise ParseError(f'Failed to parse line {line_number}: line is empty')

        if vals[0] not in ['>', '<', '1', '0', '?']:
            raise ParseError(f'Failed to parse line {line_number}: unknown command {vals[0]}')

        argnum: int = 3 if vals[0] == '?' else 2
        if len(vals) < argnum:
            raise ParseError(f'Failed to parse line {line_number}: ' +
                             f'too few arguments for command "{vals[0]}"')
        if len(vals) > argnum:
            raise ParseError(f'Failed to parse line {line_number}: ' +
                             f'too many arguments for command "{vals[0]}"')

        try:
            args: List[int] = list(map(int, vals[1:]))
        except ValueError as e:
            new_err = ParseError(f'Failed to parse line {line_number}: arguments must be integers')
            raise new_err from e


        match vals[0]:
            case '>':
                return ParseResults(1, args[0], current_value)
            case '<':
                return ParseResults(-1, args[0], current_value)
            case '1':
                return ParseResults(0, args[0], True)
            case '0':
                return ParseResults(0, args[0], False)
            case '?':
                if current_value:
                    return ParseResults(0, args[0], current_value)
                return ParseResults(0, args[1], current_value)
            case _:
                raise ParseError(f'Failed to parse line {line_number}: unknown command')
