__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>'

import socket
from threading import Thread, Lock

HOST = ''


class NetworkListener(Thread):
    def __init__(self, config, framework):
        super().__init__()
        self.config = config
        self.port = config['port']
        self.framework = framework
        self.session_socket = None
        self.lock = Lock()
        self.running = False
        self.connection_count = 0

    @property
    def connection_count(self):
        with self.lock:
            return self.__connection_count

    @connection_count.setter
    def connection_count(self, val):
        with self.lock:
            self.__connection_count = val

    # Override
    def run(self):
        self.running = True
        while self.running:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, self.port))
            s.listen(1)
            self.start_listening(s)
            s.close()
            self.connection_count += 1

    def start_listening(self, local_socket):
        try:
            (new_socket, addr) = local_socket.accept()
            print("New connection from", addr, "on port", self.port)
            self.session_socket = new_socket
            self.framework.spawn(self.session_socket, self.config)

        except Exception as e:
            print("Error on connection: ", e)

    def stop(self):
        self.running = False
        self.join()
