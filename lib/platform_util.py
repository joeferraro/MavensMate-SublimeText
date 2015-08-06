import sys
import shutil
import pipes
from MavensMate.lib.exceptions import *

windows_platforms = ["win32","win64","cygwin"]
linux_platforms = ["linux2"]
osx_platforms = ["darwin"]
user_platform = sys.platform

is_windows   = user_platform in windows_platforms
is_linux     = user_platform in linux_platforms
is_osx       = user_platform in osx_platforms

def url_transfer_executable():
    if shutil.which('curl') != None:
        return pipes.quote(shutil.which('curl'))
    elif shutil.which('wget') != None:
        return pipes.quote(shutil.which('wget')) + ' -q -O -'
    else:
        raise MMException('Please install curl or wget and try your operation again')
