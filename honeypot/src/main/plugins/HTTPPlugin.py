__author__ = 'jessenelson'
__author__ = 'zkuhns'

from plugins.BasePlugin import BasePlugin

from socket import SocketIO
from http.server import BaseHTTPRequestHandler

PAGE_LOGIN = """<html>
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

'''

'''
class HTTPPluginHandler(BaseHTTPRequestHandler):
    def __init__(self, socket):
        self.rfile = SocketIO(socket, "r")
        self.wfile = SocketIO(socket, "w")
        self.body = ''

    def setup(self):
        pass

    def address_string(self):
        return "honey_potter"

    def get_body(self):
        content_length = int(self.headers.get('content-length', 0))
        if (content_length == 0):
            return

        self.body = self.rfile.read(content_length)
        self.body = str(self.body)[2:len(self.body)+2]

    def do_GET(self):
        # front page
        if (self.path == '/'):
            self.send_response(200, 'OK')
            self.end_headers()
            self.wfile.write(PAGE_LOGIN.encode('UTF-8'))

            return

        # anything else recieves a 404
        self.send_error(404)
        self.end_headers()

    def do_POST(self):
        #login post
        if (self.path == '/login'):
            # grab the login information send a 500
            self.send_error(500)
            self.end_headers()

            return

        # Anything else recieves a 404
        self.send_error(404)
        self.end_headers()

    def do_HEAD(self):
        pass

    def do_PUT(self):
        pass

'''

'''
class HTTPPlugin(BasePlugin):
    def do_track(self):
        handler = HTTPPluginHandler(self.SOCKET)
        handler.handle_one_request()
        handler.get_body()
        self.create_entry(handler)
        handler.finish()

    def create_entry(self, handler):
        entry = {'HTTP' : {'METHOD' : handler.command,
                           'PATH' : handler.path,
                           'HEADERS' : handler.headers.as_string(),
                           'BODY' : handler.body}}

        self.do_save(entry)