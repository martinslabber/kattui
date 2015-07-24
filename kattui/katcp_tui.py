import katcp


def connect_katcp(line):
    sections = line.split()
    if sections:
        address = sections[0]
        command = sections[1:]
    else:
        address = ''
        command = []

    if ":" in address:
        if not command:
            command = ['help']
        host, port = address.split(':', 1)
        if not host:
            host = '127.0.0.1'

        try:
            port = int(port)
        except ValueError:
            port = None
    else:
        print("No address given address format is host:port")
        return

    print("Input line is: '{}' address '{}:{}' command '{}'".
          format(line, host, port, command))
    if host and port:
        this_katcp = KatCPTui(host, port)
        this_katcp.run(command)


class KatCPTui(object):

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.client = katcp.BlockingClient(host, port)
        self.raw = False

    def run(self, command):
        print("Run command on Katcp: ", command)

        self.client.handle_inform = self._katcp_line
        self.client.handle_reply = self._katcp_line

        request = command[0]
        params = command[1:]

        message = katcp.Message(katcp.Message.REQUEST, request, params)
        self.client.start()
        self.client.until_running()
        import time
        time.sleep(3)  # WHY????
        self.client.blocking_request(message)
        self.client.stop()
        self.client.ioloop.instance().stop()

    def _katcp_line(self, msg):
        if self.raw:
            print(msg)
        else:
            print(self._print_message(msg))

    def _print_message(self, msg):
        """Return Message serialized for humans.
        Returns
        -------
        msg : str
            The message encoded as a ASCII string.
        """
        if msg.arguments:
            arg_str = " " + " ".join(msg.arguments)
        else:
            arg_str = ""

        if msg.mid is not None:
            mid_str = "[%s]" % msg.mid
        else:
            mid_str = ""

        return "%s%s%s%s" % (msg.TYPE_SYMBOLS[msg.mtype], msg.name,
                             mid_str, arg_str)
