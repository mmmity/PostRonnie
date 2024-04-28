# PostRonnie
Post-Turing machine interpreter
![coverage](coverage.svg)

For now, example programs are stored in the folder "examples"

## Usage
```
usage: python postronnie.py [-h] [--program_file PROGRAM_FILE] [--output_file OUTPUT_FILE] {run,debug,tape-to-numbers,numbers-to-tape} input_file

Post-Turing machine interpreter

positional arguments:
  {run,debug,tape-to-numbers,numbers-to-tape}
                        run - runs program and stores its output in output-file;
                        debug - runs program in debug mode, showing every iteration of it, prints all logs to stdout;
                        tape-to-numbers - converts data from tape to human-readable numbers;
                        numbers-to-tape - converts human-readable numbers to input tape for machine
                        
  input_file            path to input for program or for mapping

options:
  -h, --help            show this help message and exit
  --program_file PROGRAM_FILE
                        path to program if you chose run or debug
  --output_file OUTPUT_FILE
                        path to output for program or mapping. If unspecified, uses stdout
```

### Example uses
Say, you have numbers `12` and `5`, and you want to compute `12 mod 5` using PostRonnie. Here is how you achieve that:
- Create a file `input_numbers`, which contains just `12` and `5`, divided by whitespace
- `python postronnie.py numbers-to-tape input_numbers --output_file input` - creates input, readable for Post machine from those numbers, and stores it in `input`.
- `python postronnie.py run input --program_file examples/mod.post --output_file output` - runs your program on input, creates `output`, also in Post machine format.
- `python postronnie.py tape-to-numbers output --output_file output_numbers` - converts output to human-readable numbers, stored in `output_numbers`.

If you want to see how program works stepwise, you should use `debug` option instead of `run`. It will print state of tape after each step in your terminal.

## Syntax
`# comment` - a one-line comment \
`''' multiline\n comment'''` - a multi-line comment

Commands:
- `BEGIN` - indicates that next line is the beginning of the program
- `> N` - moves carriage right and jumps to line number N
- `< N` - moves carriage left and jumps to line number N
- `1 N` - puts character '1' into current position of carriage and jumps to line number N
- `0 N` - puts character '0' into current position of carriage and jumps to line number N
- `? N M` - if carriage points to '1', jumps to line number N, otherwise jumps to line number M
- `END` - end of program

## Tests
### Unit tests
Unit tests are stored in `tests` folder. To run them, use `python -m unittest discover -v` in project root directory.
