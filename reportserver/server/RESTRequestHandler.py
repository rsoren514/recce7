import json
from http.server import BaseHTTPRequestHandler

from reportserver.manager import utilities
from reportserver.server.PortsServiceHandler import PortsServiceHandler

notFoundPayload = {}

badRequestPayload = {
    'error': 'invalid port number'}


#  Handles the service request, determines what was requested,
#  then returns back response.
#
class RestRequestHandler (BaseHTTPRequestHandler):

    def do_GET(self) :

        tokens = self.path.split('/')
        print(tokens)

        if self.path.startswith("/v1/analytics/ports"):
            port_handler = PortsServiceHandler()
            uom = None
            units = None
            if len(tokens) > 5:
                time_period = utilities.validateTimePeriod(tokens)
                uom = time_period[0]
                units = time_period[1]
            if len(tokens) >= 5:
                portNbr = utilities.validatePortNumber(tokens[4])
                print("requested: " + str(portNbr))
                if portNbr is not None and 0 < portNbr < 9000:
                    port_handler.getPortDataByTime(self, portNbr, uom, units)
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
        json_result = json.dumps(payload)
        self.send_response(responseCode)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(json_result))
        self.end_headers()
        self.flush_headers()

        self.wfile.write(bytes(json_result, "utf-8"))

        self.wfile.flush()

        return




