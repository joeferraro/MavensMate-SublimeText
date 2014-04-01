import logging
import os.path
import sys
import tempfile 
import sublime
from logging.handlers import RotatingFileHandler

logger = None

def __get_base_path():
    if hasattr(sys, 'frozen'):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(__file__))

def __get_is_frozen():
    if hasattr(sys, 'frozen'):
        return True
    else:
        return False

def setup_logging():
    try:
        settings = sublime.load_settings('mavensmate.sublime-settings')

        logging.raiseExceptions = False
        logging.basicConfig(level=logging.DEBUG)

        log_location = settings.get('mm_log_location', tempfile.gettempdir())
        logging_handler = RotatingFileHandler(os.path.join(log_location, "mmui.log"), maxBytes=1*1024*1024, backupCount=5)

        #mm log setup
        global logger
        logger = logging.getLogger('mmui')
        logger.setLevel(logging.DEBUG)
        logger.propagate = False 
        logger.addHandler(logging_handler)
    except:
        pass #todo: https://github.com/joeferraro/MavensMate-SublimeText/issues/293

def debug(msg, obj=None):
    try:
        if obj != None and type(msg) is str:
            logger.debug(msg + ' ', obj)
            print('[MAVENSMATE UI]: ' + msg + ' ', obj)
        elif obj == None and type(msg) is str:
            logger.debug(msg)
            print('[MAVENSMATE UI]:',msg)
        else:
            logger.debug(msg)
            print('[MAVENSMATE UI]:',msg) 
    except:
        if obj != None and type(msg) is str:
            print('[MAVENSMATE UI]: ' + msg + ' ', obj)
        elif obj == None and type(msg) is str:
            print('[MAVENSMATE UI]:',msg)
        else:
            print('[MAVENSMATE UI]:',msg) 
       
mm_path = None
frozen = __get_is_frozen()
base_path = __get_base_path()