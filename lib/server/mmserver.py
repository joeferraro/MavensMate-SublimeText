# -*- coding: utf-8 -*-
import argparse
import MavensMate.lib.server.lib.server_threaded as server_threaded
import MavensMate.lib.server.lib.config as config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mmpath') 
    args = parser.parse_args()
    config.mm_path = args.mmpath
    try:
        server_threaded.run()
    except:
        config.debug("Server at port 9000 already running")

if __name__ == '__main__':
    main() 