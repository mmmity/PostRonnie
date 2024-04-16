from dataclasses import dataclass
from typing import List

@dataclass
class ParseResults:
    delta: int
    newline: int
    newval: bool


class ParseError(Exception):
    pass

class LineParser:
    def parse(line: str, line_number: int, current_value: bool) -> ParseResults:
        comment_start = line.find('#')
        if (comment_start != -1):
            line = line[:comment_start]
        
        vals = line.split()
        if len(vals) == 0:
            raise ParseError(f'Failed to parse line {line_number}: line is empty')
        
        if vals[0] not in ['>', '<', '1', '0', '?']:
            raise ParseError(f'Failed to parse line {line_number}: unknown command')

        argnum: int = 3 if vals[0] == '?' else 2
        if len(vals) < argnum:
            raise ParseError(f'Failed to parse line {line_number}: too few arguments for command "{vals[0]}"')
        elif len(vals) > argnum:
            raise ParseError(f'Failed to parse line {line_number}: too many arguments for command "{vals[0]}"')
        
        try:
            args: List[int] = list(map(int, vals[1:]))
        except ValueError:
            ParseError(f'Failed to parse line {line_number}: arguments must be integers')


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
                else:
                    return ParseResults(0, args[1], current_value)
            case _:
                raise ParseError(f'Failed to parse line {line_number}: unknown command')
