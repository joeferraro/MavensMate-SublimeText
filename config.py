import os
import sublime

try:
    mm_dir = os.getcwdu()
except:
    mm_dir = os.path.dirname(__file__)

sublime_version = int(float(sublime.version()))
settings = None
merge_settings = None