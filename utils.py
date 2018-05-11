# -*- coding: utf-8 -*-
import os
import subprocess
import sys


def run_shell_cmd(cmd, silent_stdout=True, silend_stderr=False, dry_run=False):
    if dry_run:
        print("Running command:")
        print("```")
        print(cmd)
        print("```")
        return

    with open(os.devnull, 'w') as devnull:
        ret_code = subprocess.call(["sh", "-c", cmd],
                                   stdout=devnull if silent_stdout else None,
                                   stderr=devnull if silend_stderr else None)
        if ret_code != 0:
            sys.exit(ret_code)
