import os
import sys
import shutil
import sublime
import pipes
from MavensMate.lib.exceptions import *

windows_platforms = ["win32","win64","cygwin"]
linux_platforms = ["linux2"]
osx_platforms = ["darwin"]
user_platform = sys.platform

is_windows   = user_platform in windows_platforms
is_linux     = user_platform in linux_platforms
is_osx       = user_platform in osx_platforms

# removes directory including subdirectories
def rmtree(directory):
    if is_windows:
         os.system('rd /s /q "'+directory+'"')
    else:
        shutil.rmtree(directory)
        #shutil_force_rm_tree(directory)

def node_path():
    settings = sublime.load_settings('mavensmate.sublime-settings')
    if is_windows:
        platform_key = 'windows'
    elif is_linux:
        platform_key = 'linux'
    elif is_osx:
        platform_key = 'osx'
    if os.path.exists(settings.get('mm_node_path')[platform_key]):
        return settings.get('mm_node_path')[platform_key]
    elif shutil.which('node') != None:
        return shutil.which('node')
    else:
        raise MMException('Cannot find node. Please ensure nodejs is installed and either a) available on your path or b) the full path of node must be set in mm_node_path.')

def url_transfer_executable():
    if shutil.which('curl') != None:
        return pipes.quote(shutil.which('curl'))
    elif shutil.which('wget') != None:
        return pipes.quote(shutil.which('wget')) + ' -q -O -'
    else:
        raise MMException('Please install curl or wget and try your operation again')
