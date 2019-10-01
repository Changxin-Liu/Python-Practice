"""
Installs dependencies for Ninedraft
CSSE1001 Assignment 3, Semester 1, 2019

If running this file produces an error, try:
    1. running IDLE as an administrator
    2. opening this file in IDLE
    3. run this file

If that doesn't resolve the issue, please post to Piazza
"""

import sys
import subprocess

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

for path in execute([sys.executable, "-m", "pip", "install", "pymunk"]):
    print(path, end="")
