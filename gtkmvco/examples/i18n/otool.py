"""
Alternative to http://packages.python.org/macholib/
"""

import os.path
import subprocess

OTOOL = "/usr/bin/otool"  # Comes with Xcode

def exists():
    return os.path.exists(OTOOL)

def _call(*options):
    command = [OTOOL]
    command.extend(options)
    ipc = subprocess.Popen(command,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = ipc.communicate()
    if ipc.returncode != 0:
        raise EnvironmentError(' '.join(command))
    return out, err

def libraries(path):
    out, _ = _call("-L", path)
    return [line.split()[0] for line in out.splitlines()
        if line.startswith("\t")]
