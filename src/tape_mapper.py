'''
This module implements functions for converting sets of human-readable numbers
into tape input for interpreter
'''
from typing import List


class TapeMapper:
    '''
    Class with static methods numbers_to_tape and tape_to_numbers
    which convert numbers to tape or vice versa
    '''

    @staticmethod
    def numbers_to_tape(*numbers: int) -> str:
        '''
        Converts set of numbers k1, k2, ..., kn
        to a tape with strings of ones of lengths k1, ..., kn, 
        separated by one zero each.
        '''
        try:
            numbers_strings = ['1' * k for k in numbers]
        except ValueError as e:
            raise ValueError('Numbers must be integers') from e

        return '0'.join(numbers_strings)

    @staticmethod
    def tape_to_numbers(tape: str) -> List[int]:
        '''
        Converts tape with strings of ones of lengths k1, ..., kn,
        separated by one zero each, to set of numbers k1, ..., kn
        '''

        if not set(tape).issubset({'0', '1'}):
            raise ValueError('Tape must contain only ones and zeros')

        splitted = tape.split('0')

        out = [len(s) for s in splitted if len(s) != 0]
        return out
