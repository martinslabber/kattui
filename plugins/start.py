KATTUI = True
KATTUI_DENY = {'site': ['karoo', 'vkaroo']}
KATTUI_ALLOW = {'nodetype': ['head']}

import subprocess


def do(self, line):
    """Start the CAM system, doing kat-start.sh"""
    print("run kat-start.sh")
    subprocess.call('kat-start.sh')
