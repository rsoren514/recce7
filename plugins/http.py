"""

"""

from plugins.base import BasePlugin
from socket import SocketIO
from socket import timeout
from http.server import BaseHTTPRequestHandler

import uuid

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

MAX_MESSAGE_LENGTH = 65536


class HTTPPlugin(BasePlugin, BaseHTTPRequestHandler):
    def __init__(self, socket, config, framework):
        BasePlugin.__init__(self, socket, config, framework)

        self.rfile = SocketIO(socket, "r")
        self.wfile = SocketIO(socket, "w")

        self.command = None
        self.path = None
        self.headers = None
        self.body = None
        self.session = None

        socket.settimeout(60)

    def do_track(self):
        self.handle_one_request()
        self.format_data()

        #self._skt = None

    def get_body(self):
        too_long = False

        if self.headers is None:
            self.body = ''
            return
        else:

            try:
                body_length = int(self.headers.get('content-length', 0))
                if body_length > 65536:
                    body_length = 65536
                    too_long = True
            except TypeError:
                self.body = ''
                return

            try:
                self.body = self.rfile.read(body_length)
                self.body = str(self.body, 'utf-8')
                if too_long:
                    self.body += '*'
            except timeout:
                self.body = ''

    def get_session(self):
        cookie = self.headers.get('cookie', None)
        if cookie is None:
            cookie = 'SESSION=' + str(uuid.uuid4())
        self.send_header('Set-Cookie', cookie)

    def format_data(self):
        if self.command is None:
            self.command = ''
        if self.path is None:
            self.path = ''
        if self.headers is None:
            self.headers = ''
        else:
            self.headers = self.headers.as_string()
        if self.body is None:
            self.body = ''

    def address_string(self):
        return self.get_client_address()

    def end_headers(self):
        self.get_session()
        if self.request_version != 'HTTP/0.9':
            self._headers_buffer.append(b"\r\n")
            self.flush_headers()

    def do_GET(self):
        self.do_HEAD()
        if self.path == '/':
            self.wfile.write(PAGE_LOGIN)

    def do_HEAD(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', str(len(PAGE_LOGIN)))
            self.end_headers()
        elif self.path == '/login':
            self.send_error(403)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path =='/':
            self.do_GET()
        if self.path == '/login':
            self.send_error(500)
            self.get_body()
        else:
            self.send_error(404)
            self.get_body()

    def do_PUT(self):
        self.send_error(501)

    def do_OPTIONS(self):
        self.send_error(501)

    def do_DELETE(self):
        self.send_error(501)

    def do_TRACE(self):
        self.send_error(501)

    def do_CONNECT(self):
        self.send_error(501)