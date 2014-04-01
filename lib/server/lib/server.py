import sys
import os
import BaseHTTPServer
import handler
import config
import lib.config as gc

server = None

def run(context_path='', port=9000):
    gc.debug('>>> starting local MavensMate server!')
    # set current working dir on python path
    base_dir = os.path.normpath(os.path.abspath(os.path.curdir))
    sys.path.insert(0, base_dir)
    handler.Handler.mappings = config.mappings
    server = BaseHTTPServer.HTTPServer((context_path, port), handler.Handler)
    server.serve_forever()

def stop():
    print('[MAVENSMATE] shutting down local MavensMate server')
    server.shutdown()