import socket
from threading import Thread

'''

'''
class BasePlugin(Thread):
    def __init__(self, socket, framework):
        Thread.__init__(self)
        self.SOCKET = socket
        self.FRAMEWORK = framework
        self._localAddress = socket.getsockname()[0]
        self._peerAddress = socket.getpeername()[0]
        self.run()

    '''

    '''
    def run(self):
        self.configure()

        try:
            self.do_track()
        except ConnectionResetError as cre:
            error_number = cre.errno
            if error_number == 54:  # ERRNO 54 is 'connection reset by peer'
                # Log that it is possible we are being scanned, would want to write this to the db
                print("Maybe we are being scanned")
                pass

        # Need this in try statement in case socket has already been closed by client
        try:
            # Blocks any more reading from socket once we are done, unable to write data at this point anyway
            self.SOCKET.shutdown(socket.SHUT_RD)
            self.SOCKET.close()
        except OSError:
            # Log this as user force closed from their end
            print("Socket already closed.")

    def do_save(self, data):
        data['HTTP']['PEER'] = self._peerAddress
        data['HTTP']['LOCAL'] = self._localAddress
        data['HTTP']['TIME'] = 'time'

        print(data)

        self.FRAMEWORK.insert_data(data)
    '''

    '''
    def configure(self):
        pass

    '''

    '''
    def track(self):
        pass