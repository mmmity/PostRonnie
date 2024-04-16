# PostRonnie
Post-Turing machine interpreter

For now, example programs are stored in the folder "examples"

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
