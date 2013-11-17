import os
import sublime
import logging
import tempfile

mm_dir = os.path.dirname(__file__)
sublime_version = int(float(sublime.version()))
settings = None
merge_settings = None

logging.raiseExceptions = False
logging.basicConfig(level=logging.INFO)

logging_handler = logging.FileHandler(os.path.join(tempfile.gettempdir(),"mmst.log"))

#mm log setup
logger = logging.getLogger('mmst')
logger.setLevel(logging.DEBUG)
logger.propagate = False 
logger.addHandler(logging_handler)