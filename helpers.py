import sys
import os


def fatal_error(msg, exit_code=1):
    print(f"FATAL ERROR: {msg}")
    sys.exit(exit_code)


def execute(cmd, verbose=False):
    if verbose:
        print(f"Executing: {cmd}")
    result = os.system(cmd)
    if result != 0:
        fatal_error(f"Command failed: {cmd}, return code {result}")
