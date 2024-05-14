import sys
from typing import List
import random
import subprocess
import os

from src.tape_mapper import TapeMapper

def generate_test_case(length: int) -> List[int]:
    '''
    Generates test case made of length integers. Returns it
    '''
    return [random.randint(1, 10) for i in range(length)]

def convert_test_case(args: List[int]) -> str:
    '''
    Creates a test case in a random input file
    Name of input file is always "input_{suffix}"
    Also creates machine-readable tape in "input_tape_{suffix}
    Returns the suffix of input file name.
    '''
    suffix = random.randbytes(7).hex()

    with open('input_' + suffix, 'w') as numeric_input:
        numeric_input.write(' '.join(map(str, args)))

    with open('input_tape_' + suffix, 'w') as tape_input:
        tape_input.write(TapeMapper.numbers_to_tape(*args))

    return suffix

def run_test_case(suffix: str, program_name: str):
    '''
    Runs test case on program_name.post and program_name.py
    Stores their outputs in py_output_{suffix} and post_output_{suffix}
    '''
    with open('input_' + suffix) as numeric_input, open('output_' + suffix, 'w') as numeric_output:
        py_proc = subprocess.run(
            ["python", f"examples/{program_name}.py"],
            stdin=numeric_input,
            stdout=numeric_output
        )
        if py_proc.returncode != 0:
            raise ValueError("Malformed input, happens")

    with open('output_tape_' + suffix, 'w') as tape_output:
        post_proc = subprocess.run(
            ["python", "postronnie.py", "--program_file", f"examples/{program_name}.post", "run", f"input_tape_{suffix}"],
            stdout=tape_output
        )
        post_proc.check_returncode()

def compare_test_case(suffix: str) -> bool:
    '''
    Returns True if outputs from post and py script are the same, False otherwise
    '''
    with open('output_' + suffix) as numeric_output, open('output_tape_' + suffix) as tape_output:
        return list(map(int, numeric_output.read().split())) == TapeMapper.tape_to_numbers(tape_output.read().strip())

def clean_up(suffix: str):
    '''
    Removes all temporary files in test case
    '''
    if os.path.exists('input_' + suffix):
        os.remove('input_' + suffix)

    if os.path.exists('input_tape_' + suffix):
        os.remove('input_tape_' + suffix)

    if os.path.exists('output_' + suffix):
        os.remove('output_' + suffix)

    if os.path.exists('output_tape_' + suffix):
        os.remove('output_tape_' + suffix)

def main():
    # print(os.listdir('.'))
    name = sys.argv[1]
    arg_count = int(sys.argv[2])
    count = int(sys.argv[3])

    for _ in range(count):
        test_case = generate_test_case(arg_count)
        suffix = convert_test_case(test_case)

        try:
            run_test_case(suffix, name)
        except FileNotFoundError:
            print('No such program. Aborting')
            clean_up(suffix)
            exit(1)
        except ValueError:
            clean_up(suffix)
            continue
        except subprocess.CalledProcessError:
            print('Error in post machine. Aborting')
            print('Test case is: ' + ' '.join(map(str, test_case)))
            clean_up(suffix)
            exit(1)

        try:
            if not compare_test_case(suffix):
                print('Outputs do not match')
                print('Test case is: ' + ' '.join(map(str, test_case)))
                clean_up(suffix)
                exit(1)
        except Exception as e:
            clean_up(suffix)
            print('Got exception:', e)

        clean_up(suffix)

    print(f'{count} tests successfully run')

if __name__ == '__main__':
    main()
