
from __future__ import print_function

import json
import getpass

from cmd2 import Cmd

from .katcp_tui import connect_katcp
from .plugin import connect_plugin


class KatCam(Cmd):
    """Simple command processor example."""

    def do_ps(self, line):
        """An kat tailored ps."""
        print(line)

    def do_plugins(self, line):
        """Show the available plugins and the rule interpretation for each."""
        connect_plugin(line)

    def do_katcp(self, line):
        """Connect with the katcp protocol."""
        connect_katcp(line)

    def do_node(self, line):
        """Print the node.conf contents, sorted by key.
        or by provided filters."""
        items = line.split()
        try:
            node_conf = json.loads(open('/var/kat/node.conf').read())
        except:
            node_conf = {}

        if not items:
            items = sorted(node_conf.keys())
            for key in items:
                print("{}: {}".format(key, node_conf.get(key)))
        else:
            for key in items:
                print("{}".format(node_conf.get(key)), end=" ")
            print()

    def do_shell(self, line):
        """Open a IPython CAM shell.
        the kat object will be there and ready.
        """
        cam = False
        controlled_clients = False
        for segment in [s.lower() for s in line.split()]:
            if segment == 'cam':
                cam = getpass.getpass("CAM Password or ENTER to continue:")
                # cam_pass=' '
                cam = cam.strip()
                if not cam:
                    cam = True
            elif segment == 'all':
                controlled_clients = 'all'

        import IPython
        from IPython import start_ipython
        try:
            # New IPython
            c = IPython.config.application.get_config()
        except AttributeError:
            # Old IPython
            c = IPython.config.loader.Config()
        # Set the configuration of the IPython session:
        # https://ipython.org/ipython-doc/dev/config/intro.html
        c.TerminalIPythonApp.display_banner = True
        c.InteractiveShellApp.exec_lines = ['import katuilib']
        if cam is False:
            c.InteractiveShellApp.exec_lines.append('configure()')
        elif cam is True:
            c.InteractiveShellApp.exec_lines.append('configure_cam()')
        else:
            cmd = 'configure_cam('
            cmd += 'cam_pass="{}"'.format(cam)
            if controlled_clients:
                cmd += ", controlled_clients='all'"
            cmd += ')'
            c.InteractiveShellApp.exec_lines.append(cmd)
        start_ipython(argv=[], config=c)

    def do_EOF(self, line):
        """Ctrl-D to exit."""
        return True
