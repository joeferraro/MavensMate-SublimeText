import os
import sys
import shutil
import stat
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

def url_transfer_executable():
    if shutil.which('curl') != None:
        return pipes.quote(shutil.which('curl'))
    elif shutil.which('wget') != None:
        return pipes.quote(shutil.which('wget')) + ' -q -O -'
    else:
        raise MMException('Please install curl or wget and try your operation again')

# def shutil_force_rm_tree(path, *args, **kwargs):
#     os.chmod(path, stat.S_IRWXU)
#     for (dirpath, dirnames, filenames) in os.walk(path):
#         os.chmod(dirpath, stat.S_IRWXU)
#         for filename in filenames:
#             os.chmod(os.path.join(dirpath, filename),
#                         stat.S_IRWXU)
#     shutil.rmtree(path, *args, **kwargs)
