# -*- coding: utf-8 -*-
import subprocess
import sys


def run_shell_cmd(cmd,
                  cwd=None,
                  verbose=False):
    if verbose:
        print("Running command:")
        print("```")
        print(cmd)
        print("```")

    r = subprocess.Popen(["sh", "-c", cmd],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         cwd=cwd)
    out, err = r.communicate()
    if len(err.strip()) > 0:
        print(err)
    if r.returncode != 0:
        sys.exit(r.returncode)
    return out
