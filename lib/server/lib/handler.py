#import BaseHTTPServer
from http.server import BaseHTTPRequestHandler
import MavensMate.lib.server.lib.config as config

class Handler(BaseHTTPRequestHandler):
  # set mappings - dict of dicts - ex: {'/' : {'GET' : test}}
  # meaning, path / with GET request will map to test handler
    mappings = {}

    def main_handler(self, method='GET'):
        # get request url (without url params) and remove trailing /
        config.logger.debug('>>> handling request')
        config.logger.debug(self.path)

        request_url = self.path.split('?')[0]
        if request_url is not '/':
            request_url = request_url.rstrip('/')

        handler = None
        try:
            handler = self.mappings[request_url][method]
            #config.logger.debug(handler)
        except KeyError:
            # no mapping found for the request
            self.send_response(404)
            self.end_headers()
            return

        try:
            handler(self)
        except KeyError:
            # method not found
            self.send_response(501)
            self.end_headers()
            return

    def do_GET(self):
        self.main_handler('GET')
        return

    def do_POST(self):
        print(self)
        self.main_handler('POST')
        return

    def log_message(self, format, *args):
        return