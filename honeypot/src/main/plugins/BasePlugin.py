__author__ = 'jessenelson'

from threading import Thread


class BasePlugin(Thread):
    def __init__(self, socket):
        Thread.__init__(self)
        self._skt = socket
        pass

    def run(self):
        self.do_track()
        self._skt.close()
