__author__ = 'jessenelson'
import socket
from threading import Thread

HOST = ''
conn = None


class NetworkListener(Thread):
    def __init__(self, config, framework):
        Thread.__init__(self)
        self.config = config
        self.port = config['port']
        self.framework = framework
        self.session_socket = None

    # Override
    def run(self):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, self.port))
            s.listen(1)
            self.start_listening(s)
            s.close()

    def start_listening(self, local_socket):
        try:
            (new_socket, addr) = local_socket.accept()
            print("New connection from", addr, "on port", self.port)
            self.session_socket = new_socket
            self.framework.spawn(self.session_socket, self.config)

        except Exception as e:
            print("Error on connection: ", e)
