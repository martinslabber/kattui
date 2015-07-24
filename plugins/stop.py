KATTUI = True

import subprocess


def do(self, line):
    """Stop the CAM system, doing kat-stop.sh

    If the arrgument 'hard' is added eg. ::
        kat stop hard

    Then a kat kill will be done.
    """
    if line and line.lower() in ['hard', 'kill']:
        cmd = ['kat-kill.py']
    else:
        cmd = ['kat-stop.sh']
    subprocess.call(cmd)
