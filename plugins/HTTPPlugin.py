__author__ = 'jessenelson'

from plugins.BasePlugin import BasePlugin


class HTTPPlugin(BasePlugin):
    def __init__(self, socket, framework):
        BasePlugin.__init__(self, socket, framework)
        print('Spawned team!')

    def do_track(self):
        while True:
            data = self._skt.recv(1024)
            if not data:
                break
            self._skt.sendall(data)