import unittest

from src.tape_mapper import TapeMapper

class TestTapeMapper(unittest.TestCase):
    def test_numbers_to_tape(self):
        self.assertEqual(TapeMapper.numbers_to_tape(3, 4), '11101111')
        self.assertEqual(TapeMapper.numbers_to_tape(1, 1, 1, 1, 1), '101010101')
        self.assertEqual(TapeMapper.numbers_to_tape(7), '1111111')
        self.assertEqual(TapeMapper.numbers_to_tape(1, 2, 3, 4), '1011011101111')

        with self.assertRaises(ValueError):
            TapeMapper.numbers_to_tape(9, 8, 'anime', None)

    def test_tape_to_numbers(self):
        with self.assertRaises(ValueError):
            TapeMapper.tape_to_numbers('11001101011234anime')

        self.assertEqual([3, 4], TapeMapper.tape_to_numbers('11101111'))
        self.assertEqual([1, 1, 1, 1, 1], TapeMapper.tape_to_numbers('101010101'))
        self.assertEqual([7], TapeMapper.tape_to_numbers('1111111'))
        self.assertEqual([1, 2, 3, 4], TapeMapper.tape_to_numbers('1011011101111'))
