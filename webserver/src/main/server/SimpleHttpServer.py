import BaseHTTPServer

from RESTRequestHandler import *


class SimpleHttpServer():
    def setupAndStart(self):
        # configure these params somewhere else
        server_addr = ('localhost', 8000)
        #request_handler = SimpleHTTPServer.SimpleHTTPRequestHandler

        request_handler = RESTRequestHandler

        # instantiate a server object
        httpd = BaseHTTPServer.HTTPServer (server_addr, request_handler)

        # start serving pages
        httpd.serve_forever ()

