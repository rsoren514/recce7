from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import json

#todo:  get json from database data
#todo:  set up method for each path
#todo:  decide what we want for path names (what the api will be)



fakejson = {"test": "something"}

class RESTRequestHandler (BaseHTTPRequestHandler):

    def do_GET(self) :

        if self.path == "/analytics" :
            #send response code:
            self.send_response(200)
            #send headers:
            self.send_header("Content-type:", "text/html")
            # send a blank line to end headers:
            self.wfile.write("\n")

            #send response:
            json.dump(fakejson, self.wfile)
