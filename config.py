import os
import sublime
import logging
from logging.handlers import RotatingFileHandler
import tempfile

mm_dir = os.path.dirname(__file__)
sublime_version = int(float(sublime.version()))
settings = None
merge_settings = None

logger = None

def setup_logging():
    try:
        settings = sublime.load_settings('mavensmate.sublime-settings')

        logging.raiseExceptions = False
        logging.basicConfig(level=logging.DEBUG)

        log_location = settings.get('mm_plugin_logs_location', tempfile.gettempdir())
        logging_handler = RotatingFileHandler(os.path.join(log_location, "mmst.log"), maxBytes=1*1024*1024, backupCount=5)

        #mm log setup
        global logger
        logger = logging.getLogger('mmst')
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        logger.addHandler(logging_handler)
    except:
        pass #TODO: need to handle this permission denied error (https://github.com/joeferraro/MavensMate-SublimeText/issues/293)

def debug(msg, obj=None):
    try:
        if obj != None and type(msg) is str:
            logger.debug(msg + ' ', obj)
            print('[MAVENSMATE]: ' + msg + ' ', obj)
        elif obj == None and type(msg) is str:
            logger.debug(msg)
            print('[MAVENSMATE]:',msg)
        else:
            logger.debug(msg)
            print('[MAVENSMATE]:',msg)
    except:
        if obj != None and type(msg) is str:
            print('[MAVENSMATE]: ' + msg + ' ', obj)
        elif obj == None and type(msg) is str:
            print('[MAVENSMATE]:',msg)
        else:
            print('[MAVENSMATE]:',msg)

