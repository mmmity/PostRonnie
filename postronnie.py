import argparse
import textwrap
import time

from src.interpreter import Interpreter, EndOfProgram
from src.tape_mapper import TapeMapper

def main():
    parser = argparse.ArgumentParser(
        prog='PostRonnie',
        description='Post-Turing machine interpreter',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('command',
                        choices=['run', 'debug', 'tape-to-numbers', 'numbers-to-tape'],
                        help=textwrap.dedent('''
                            run - runs program and stores its output in output-file;
                            debug - runs program in debug mode, showing every iteration of it, prints all logs to stdout;
                            tape-to-numbers - converts data from tape to human-readable numbers;
                            numbers-to-tape - converts human-readable numbers to input tape for machine\n\n'''.lstrip('\n')
                        ))
    parser.add_argument('--program_file', help='path to program if you chose run or debug')
    parser.add_argument('input_file', help='path to input for program or for mapping')
    parser.add_argument('--output_file', help='path to output for program or mapping. If unspecified, uses stdout')

    args = parser.parse_args()

    with open(args.input_file, 'r') as input_file:
        input_str = input_file.read().strip()


    match args.command:
        case 'run':
            if args.program_file is None:
                print('Program file must be specified')
                return
            try:
                interpreter = Interpreter.load_from_files(args.input_file, args.program_file)
            except FileNotFoundError:
                print('No such file or directory')
                return

            step_count = 0
            while True:
                try:
                    interpreter.interpret_current_line()
                    step_count += 1
                    if step_count >= 1000:
                        results = 'undefined'
                        break
                except EndOfProgram:
                    results = interpreter.get_results()
                    break

            if args.output_file is None:
                print(results)
            else:
                with open(args.output_file, 'w') as output_file:
                    output_file.write(results)

        case 'debug':
            if args.program_file is None:
                print('Program file must be specified')
                return
            try:
                interpreter = Interpreter.load_from_files(args.input_file, args.program_file)
            except FileNotFoundError:
                print('No such file or directory')
                return

            while True:
                try:
                    print(interpreter.debug())
                    interpreter.interpret_current_line()
                    time.sleep(0.3)
                    step_count += 1
                    if step_count >= 1000:
                        results = 'undefined'
                        break
                except EndOfProgram:
                    results = interpreter.get_results()
                    break
            
            print(results)

        case 'tape-to-numbers':
            results = TapeMapper.tape_to_numbers(input_str)

            if args.output_file is None:
                print(results)
            else:
                with open(args.output_file, 'w') as output_file:
                    output_file.write(' '.join(map(str, results)))

        case 'numbers-to-tape':
            try:
                numbers = list(map(int, input_str.split()))
            except ValueError:
                print('Must provide numbers')

            results = TapeMapper.numbers_to_tape(*numbers)

            if args.output_file is None:
                print(results)
            else:
                with open(args.output_file, 'w') as output_file:
                    output_file.write(results)


if __name__ == '__main__':
    main()
