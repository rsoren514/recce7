__author__ = 'jessenelson'

from threading import Thread


class BasePlugin(Thread):
    def __init__(self, socket, framework):
        Thread.__init__(self)
        self._skt = socket
        self._framework = framework
        self.run(self)

    def run(self):
        self.do_track()
        self._skt.close()
