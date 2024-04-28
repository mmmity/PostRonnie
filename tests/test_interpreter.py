import unittest
import random
import os

from src.interpreter import EndOfProgram, Interpreter, UndefinedError
from src.dllist import DLList, nxt

class TestInterpreter(unittest.TestCase):
    def test_init(self):
        int1 = Interpreter('100', ['BEGIN'])
        self.assertEqual(int1.data, DLList([True, False, False]))
        self.assertEqual(int1.current_index, 1)

        with self.assertRaises(ValueError):
            Interpreter('anime', ['BEGIN', '> 1'])

        with self.assertRaises(SyntaxError):
            Interpreter('100', ['> 1'])

    def test_interpret_current_line_end(self):
        int1 = Interpreter('1', ['BEGIN', 'END'])
        with self.assertRaises(EndOfProgram):
            int1.interpret_current_line()

    def test_interpret_current_line_undefined(self):
        int1 = Interpreter('1', ['BEGIN', '> 3', '1 2'])
        with self.assertRaises(UndefinedError):
            for _ in range(Interpreter.MAX_STEP_COUNT + 2):
                int1.interpret_current_line()

    def test_interpret_current_line_nonexistent_line(self):
        int1 = Interpreter('1', ['BEGIN', '> 100500'])
        int1.interpret_current_line()
        with self.assertRaises(SyntaxError):
            int1.interpret_current_line()

    def test_interpret_current_line_normal(self):
        int1 = Interpreter('1', ['BEGIN', '> 3', '< 4', '< 5', 'END'])
        self.assertEqual(int1.data, DLList([True]))
        self.assertEqual(int1.current_index, 1)
        self.assertEqual(int1.carriage, int1.data.begin())

        int1.interpret_current_line()
        self.assertEqual(int1.data, DLList([True, False]))
        self.assertEqual(int1.current_index, 2)
        self.assertEqual(int1.carriage, nxt(int1.data.begin()))

        int1.interpret_current_line()
        self.assertEqual(int1.data, DLList([True, False]))
        self.assertEqual(int1.current_index, 3)
        self.assertEqual(int1.carriage, int1.data.begin())

        int1.interpret_current_line()
        self.assertEqual(int1.data, DLList([False, True, False]))
        self.assertEqual(int1.current_index, 4)
        self.assertEqual(int1.carriage, int1.data.begin())

    def test_get_results(self):
        int1 = Interpreter('11', ['BEGIN', '> 3', '> 4', '< 5', '< 6', '< 7', 'END'])
        for _ in range(5):
            int1.interpret_current_line()

        res = int1.get_results()
        self.assertEqual(res, '0110')

    def test_debug(self):
        int1 = Interpreter('11', ['BEGIN', '> 3', '> 4', '< 5', '< 6', '< 7', 'END'])
        self.assertEqual(int1.debug(), '\033[94m\033[1m1\033[0m1 on line 2')

        int1.interpret_current_line()
        self.assertEqual(int1.debug(), '1\033[94m\033[1m1\033[0m on line 3')

        int1.interpret_current_line()
        self.assertEqual(int1.debug(), '11\033[94m\033[1m0\033[0m on line 4')

        int1.interpret_current_line()
        self.assertEqual(int1.debug(), '1\033[94m\033[1m1\033[0m0 on line 5')

        int1.interpret_current_line()
        self.assertEqual(int1.debug(), '\033[94m\033[1m1\033[0m10 on line 6')

    def test_load_from_files(self):
        input_filename = 'input_' + random.randbytes(6).hex()
        program_filename = 'program_' + random.randbytes(7).hex()
        with open(input_filename, 'w') as input_file:
            input_file.write('100')

        with open(program_filename, 'w') as program_file:
            program_file.write('BEGIN')

        int1 = Interpreter.load_from_files(input_filename, program_filename)

        self.assertEqual(int1.data, DLList([True, False, False]))
        self.assertEqual(int1.current_index, 1)
        self.assertEqual(int1.program, ['BEGIN'])

        os.remove(input_filename)
        os.remove(program_filename)
