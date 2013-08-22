import os
import sublime

mm_dir = os.path.dirname(__file__)
sublime_version = int(float(sublime.version()))
settings = None
merge_settings = None