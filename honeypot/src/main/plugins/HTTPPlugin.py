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

PAGE_404 = """\
<!DOCTYPE HTML>
<html>
    <head>
        <h1>404 Not Found</h1>
    </head>
</html>
    """

PAGE_500 = """\
<!DOCTYPE HTML>
<html>
    <head>
        <h1>500 Internal Server Error</h1>
    </head>
</html>
    """

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

    def parse_body(self):
        print("BODY")
        self.body = []

        while(True):
            print("LOOP")
            line = self.rfile.readline()
            print("LINE")
            if line in (b'\r\n', b'\n', b''):
                break
            self.body.append(line)

    def do_GET(self):
        # front page
        if (self.path == '/'):
            self.send_response(200, 'OK')
            self.end_headers()
            self.wfile.write(PAGE_LOGIN.encode('UTF-8'))

            return

        # anything else recieves a 404
        self.send_response(404, 'Not Found')
        self.end_headers()
        self.wfile.write(PAGE_404.encode('UTF-8'))

    def do_POST(self):
        #login post
        if (self.path == '/login'):
            # grab the login information send a 500
            self.send_response(500, 'Internal Server Error')
            self.end_headers()
            self.wfile.write(PAGE_500.encode('UTF-8'))

            content_length = int(self.headers.get('content-length', 0))
            if (content_length == 0):
                return

            self.body = self.rfile.read(content_length)

            return

        # Anything else recieves a 404
        self.send_response(404, 'Not Found')
        self.end_headers()
        self.wfile.write(PAGE_404.encode('UTF-8'))

'''

'''
class HTTPPlugin(BasePlugin):
    def do_track(self):
        handler = HTTPPluginHandler(self.SOCKET)
        handler.handle_one_request()
        #TODO Split the headers and body

        entry = {"HTTP" :
                     {'REQUEST' : str(handler.raw_requestline)[2:len(handler.raw_requestline)],
                      'HEADERS' : handler.headers.as_string(),
                      'BODY' : str(handler.body)}}

        self.do_save(entry)

        handler.finish()