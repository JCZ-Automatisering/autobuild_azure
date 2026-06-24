import sys
import os
import subprocess


def fatal_error(msg, exit_code=1):
    print(f"FATAL ERROR: {msg}")
    sys.exit(exit_code)


def execute(cmd, verbose=False, no_fatal=False):
    if verbose:
        print(f"Executing: {cmd}")
    result = os.system(cmd)
    if result != 0:
        if not no_fatal:
            fatal_error(f"Command failed: {cmd}, return code {result}")
        return False

    return True


def execute_get_value(cmd):
    result = subprocess.run(
        cmd,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=None,
        text=True
    )
    return result.stdout


def get_current_user_id():
    value = execute_get_value("id -u")
    return int(value)

def get_current_group_id():
    value = execute_get_value("id -g")
    return int(value)

def config_section_has_all_keys(section_object, keys):
    for key in keys:
        if key not in section_object:
            return False

    return True
