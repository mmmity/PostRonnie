'''
A script for running integral tests for all available programs.
It is used as integral tests in CI
'''
import os
from pathlib import Path
import subprocess
import json

argument_mapping = json.load(open('argument_mapping.json', 'r'))

for filename in os.listdir('examples'):
    if not filename.endswith('.post'):
        continue
    no_extension = Path(filename).stem

    proc = subprocess.run(['python3', 'stress_tests.py', no_extension, str(argument_mapping[no_extension]), '30'], capture_output=True)
    # Runs 30 random tests on chosen program using stress_tests.py

    if proc.returncode != 0:
        print(f'failed tests for {no_extension}')
        print('stdout:')
        print(proc.stdout.decode('utf-8'))
        exit(1)

print('All integral tests completed successfully')
