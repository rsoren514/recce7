__author__ = 'jessenelson'
__author__ = 'zkuhns'

from plugins.base import BasePlugin

import time
import urllib.parse
import socket

PAGE_LOGIN = b"""<html>
    <head>
        <style>
            form {
                text-align: center;
            }
        </style>

        <section class="loginform cf">
        <form action="login" method="post">
            Username<br>
            <input type="text" name="username" required><br>
            Password<br>
            <input type="password" name="password" required><br>
            <input type="submit" value="Login">
        </form>
        </section>
    </head>
</html>"""

PAGE_ERROR = """<html>
    <head>
        %(error)s
    </head>
</html>"""


METHODS = {
    'GET',
    'HEAD',
    'POST',
    'PUT',
    'DELETE',
    'TRACE',
    'CONNECT'
}

HEADERS = {
    'accept',
    'accept-charset',
    'accept-encoding',
    'accept-language',
    'accept-datetime',
    'authorization',
    'cache-control',
    'connection',
    'cookie',
    'content-length',
    'content-md5',
    'content-type',
    'date',
    'expect',
    'forwarded',
    'from',
    'host',
    'if-match',
    'if-modified-since',
    'if-none-match',
    'if-range',
    'if-unmodified-since',
    'max-forwards',
    'origin',
    'pragma',
    'proxy-authorization',
    'range',
    'referer',
    'te',
    'user-agent',
    'upgrade',
    'via',
    'warning',
}

DAYS = [
    'Mon',
    'Tue',
    'Wed',
    'Thu',
    'Fri',
    'Sat',
    'Sun',
]

MONTHS = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
]

SERVER_NAME = "honey_potter"

REPLIES = {
    200 : '200 OK',
    400 : '400 Bad Request',
    404 : '404 Not Found',
    414 : '414 URI Too Long',
    500 : '500 Internal Server Error',
    501 : '501 Not Implemented',
}

'''

'''
class HTTPPlugin(BasePlugin):
    def __init__(self, socket, framework):
        BasePlugin.__init__(self, socket, framework)

        self.message = ""

        self.method = ""
        self.path = ""
        self.version = ""
        self.headers = {}
        self.body = ""

    def do_track(self):
        self.rfile = socket.SocketIO(self._skt, "r")
        self.wfile = socket.SocketIO(self._skt, "w")

        if not self.read_message():
            self._skt = None
            return False

        if not self.handle_message():
            self._skt = None
            return False

        self._skt = None

    def read_message(self):
        if (not self.read_request()):
            return False

        if (not self.read_headers()):
            return False

        if (not self.read_body()):
            return False

        return True

    def read_request(self):
        request_line = self.rfile.readline(2049)

        if (len(request_line) > 2048):
            # too long exception 414 error
            return False

        request_line = request_line.split()

        self.method = str(request_line[0], 'utf-8')

        if self.method not in METHODS:
            # method is not an http method 400 error
            return False

        self.path = str(request_line[1], 'utf-8')
        self.path = urllib.parse.unquote(self.path)
        self.path = self.path.lower()

        if self.path[0] != '/':
            # path is not a path 400 error
            return False

        if (len(request_line) == 3):
            self.version = str(request_line[2], 'utf-8')

        return True

    def read_headers(self):
        while (True):
            line = self.rfile.readline()

            if line in (b'\r\n', b'\n', b''):
                break

            line = str(line, 'utf-8')

            line = line.split(': ', 1)

            if (len(line) < 2):
                # bad header 400 error
                return False

            line[1] = line[1].rstrip('\n')
            line[1] = line[1].rstrip('\r\n')
            self.headers[line[0].lower()] = line[1]

        return True

    def read_body(self):
        if 'content-length' in self.headers:
            size = self.headers['content-length']
            print(size)

        return True

    def handle_message(self):
        if not getattr(self, 'do_' + self.method)():
            return False

        return True

    def do_GET(self):
        if (self.path == '/'):
            self.reply(200, PAGE_LOGIN)
        else:
            self.reply(404)

        return True

    def do_HEAD(self):
        if (self.path == '/'):
            self.reply(200, PAGE_LOGIN)
        else:
            self.reply(404)

        return True

    def do_POST(self):
        if (self.path == '/login'):
            self.reply(500)
        else:
            self.reply(404)

        return True

    def do_PUT(self):
        self.reply(501)

        return True

    def do_DELETE(self):
        self.reply(501)

        return True

    def do_TRACE(self):
        self.reply(501)

        return True

    def do_CONNECT(self):
        self.reply(501)

        return True

    def reply(self, code, body=None):
        self.wfile.write(b'HTTP/1.1 ')
        self.wfile.write(bytes(REPLIES[code], 'utf-8'))
        self.wfile.write(b'\r\n')
        self.wfile.write(b'Date: ' + bytes(self.date_string(), 'utf-8'))
        self.wfile.write(b'\r\n')
        self.wfile.write(b'Content-Type: text/html; charset=UTF-8')
        self.wfile.write(b'\r\n')

        if body == None:
            body = "<html><head><h1>" + REPLIES[code] + "</h1></head></html>"
            body = bytes(body, 'utf-8')

        self.wfile.write(b'Content-Length: ')
        self.wfile.write(bytes(str(len(body)), 'utf-8'))
        self.wfile.write(b'\r\n')
        self.wfile.write(b'\r\n')
        self.wfile.write(body)

    def date_string(self):
        year, mon, mday, hour, min, sec, wday, yday, isdst = time.gmtime(time.time())
        return "%s, %02d %3s %4d %02d:%02d:%02d GMT" \
            % (DAYS[wday], mday, MONTHS[mon-1], year, hour, min, sec)