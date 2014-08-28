import sys
import os
import MavensMate.lib.server.lib.handler as handler
import MavensMate.lib.server.lib.endpoints as endpoints
import MavensMate.lib.server.lib.config as gc
import threading
import socketserver
from http.server import HTTPServer
#from BaseHTTPServer import HTTPServer
server = None

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def run(context_path='', port=9000):
    gc.debug('starting local MavensMate UI server')
    base_dir = os.path.normpath(os.path.abspath(os.path.curdir))
    sys.path.insert(0, base_dir)
    handler.Handler.mappings = endpoints.mappings
    server = ThreadedHTTPServer((context_path, port), handler.Handler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    #server.serve_forever()

def stop():
    print('[MAVENSMATE] shutting down local MavensMate server')
    server.shutdown()
    #os.system("kill -9 `fuser -n tcp 9000`")