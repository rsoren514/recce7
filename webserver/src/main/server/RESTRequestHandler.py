from http.server import BaseHTTPRequestHandler
from server.Utilities import Utilities
import json

notFoundPayload = {}

badRequestPayload = {
    'error': 'invalid port number'}


class RestRequestHandler (BaseHTTPRequestHandler):

    def do_GET(self) :

        tokens = self.path.split('/')
        print(tokens)

        utils = Utilities()
        if self.path.startswith("/v1/analytics/ports"):
            if len(tokens) >= 5:
                portNbr = utils.getIntValue(tokens[4])
                print("requested: " + str(portNbr))
                if portNbr is not None and 0 < portNbr < 9000:
                    self.getPortData(portNbr)
                else:
                    self.badRequest(portNbr)
            else:
                self.badRequest('')
        else:
            self.notFound()

    def notFound(self):
        # send response code:
        self.sendJsonResponse(notFoundPayload,404)

    def badRequest(self, portNbr):
        # send response code:
        self.sendJsonResponse(badRequestPayload,400)

    def sendJsonResponse(self, payload, responseCode):

        # Note:  responseCode must be set before headers in python3!!
        # see this post:
        # http://stackoverflow.com/questions/23321887/python-3-http-server-sends-headers-as-output/35634827#35634827
        self.send_response(responseCode)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(payload))
        self.end_headers()
        self.flush_headers()

        self.wfile.write(bytes(payload, "utf-8"))

        self.wfile.flush()

        return




