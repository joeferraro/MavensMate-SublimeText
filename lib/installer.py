import threading
import json
import os
import stat
import sys
import MavensMate.config as config
import MavensMate.lib.platform_util as platform_util
import time
from MavensMate.lib.printer import PanelPrinter
from .threads import PanelThreadProgress
from .threads import ThreadTracker
import shutil

debug = config.debug

from zipfile import ZipFile
try:
    from .threads import ThreadProgress
except ImportError as e:
    debug("[MAVENSMATE] import error: ", e)

try:
    import urllib
except ImportError:
    import urllib.request as urllib
import sublime

def get_platform_flag():
    if 'linux' in sys.platform:
        file_name_platform_flag = 'linux'
    elif 'darwin' in sys.platform:
        file_name_platform_flag = 'osx'
    else:
        file_name_platform_flag = 'win'
    return file_name_platform_flag

# explicitly executes MmInstaller (downloads and installs latest version of mm to the plugin root)
def execute(printer=None, **kwargs):
    if printer == None:
        printer = PanelPrinter.get(sublime.active_window().id())
    threads = []
    thread = MmInstaller(True, printer=printer, **kwargs)
    threads.append(thread)
    thread.start()

# extracts mm.zip into a top-level subdirectory called 'mm'
def extract_mm_zip():
    zip_name = 'mm.zip'
    if 'linux' in sys.platform:
        zip_name = 'mm.tar.gz'

    file_location = os.path.join(sublime.packages_path(),"User","MavensMate",zip_name)
    dest_dir = os.path.join(sublime.packages_path(),"User","MavensMate")

    if 'linux' in sys.platform:
        import tarfile
        with tarfile.open(file_location) as tarf:
            tarf.extractall(dest_dir)
    else:
        with ZipFile(file_location) as zf:
            zf.extractall(dest_dir)

# chmod +x any platform-specific executables
def ensure_executable_perms():
    if 'linux' in sys.platform:
        mm_stat = os.stat(os.path.join(sublime.packages_path(),"User","MavensMate","mm","mm"))
        os.chmod(os.path.join(sublime.packages_path(),"User","MavensMate","mm","mm"), mm_stat.st_mode | stat.S_IEXEC)
    elif 'darwin' in sys.platform:
        mm_stat = os.stat(os.path.join(sublime.packages_path(),"User","MavensMate","mm","mm"))
        os.chmod(os.path.join(sublime.packages_path(),"User","MavensMate","mm","mm"), mm_stat.st_mode | stat.S_IEXEC)

        mavensmate_app_stat = os.stat(os.path.join(sublime.packages_path(),"User","MavensMate","mm","lib","bin","MavensMateWindowServer.app","Contents","MacOS","MavensMateWindowServer"))
        os.chmod(os.path.join(sublime.packages_path(),"User","MavensMate","mm","lib","bin","MavensMateWindowServer.app","Contents","MacOS","MavensMateWindowServer"), mavensmate_app_stat.st_mode | stat.S_IEXEC)
    else:
        mm_stat = os.stat(os.path.join(sublime.packages_path(),"User","MavensMate","mm","mm.exe"))
        os.chmod(os.path.join(sublime.packages_path(),"User","MavensMate","mm","mm.exe"), mm_stat.st_mode | stat.S_IEXEC)

def handle_result(operation, process_id, printer, res, thread):
    debug('handling result of mm update!!!')
    thread.calculate_process_region()
    region = [thread.status_region.end(), thread.status_region.end()+10]
    thread.printer.panel.run_command('write_operation_status', {'text': thread.result, 'region': region })

class MmInstaller(threading.Thread):
    def __init__(self, force=False, version=None, **kwargs):
        self.force          = force
        self.version        = version
        self.printer        = kwargs.get('printer', None)
        self.process_id     = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        self.status_region  = None
        self.callback       = handle_result
        self.window         = sublime.active_window()
        self.view           = self.window.active_view()
        self.result         = None
        self.operation      = 'install_mm'
        self.alt_callback   = None
        self.settings       = sublime.load_settings('mavensmate.sublime-settings')
        self.release        = kwargs.get('release', None)
        self.platform_flag  = get_platform_flag()

        if self.printer == None:
            self.printer = PanelPrinter.get(self.window.id())

        threading.Thread.__init__(self)

    def calculate_process_region(self):
        process_region = self.printer.panel.find(self.process_id,0)
        self.status_region = self.printer.panel.find('   Result: ',process_region.begin())

    def run(self):
        try:
            debug('mavensmate package installer -->')

            self.install()

            self.result = 'Success. Please restart Sublime Text -- Happy coding!!'
            if self.printer != None:
                self.calculate_process_region()
                ThreadTracker.remove(self)

        except BaseException as e:
            import traceback
            import sys
            traceback.print_exc(file=sys.stdout)
            debug('[MAVENSMATE] could not install mm')
            debug(e)
            self.result = '[OPERATION FAILED]: could not install mm, please generate/check logs and report GitHub issue'
            if self.printer != None:
                self.calculate_process_region()
                ThreadTracker.remove(self)

    def install(self):
        if not os.path.isdir(os.path.join(sublime.packages_path(),"User","MavensMate")):
            os.makedirs(os.path.join(sublime.packages_path(),"User","MavensMate"))

        if os.path.isdir(os.path.join(sublime.packages_path(),"User","MavensMate","mm")):
            platform_util.rmtree(os.path.join(sublime.packages_path(),"User","MavensMate","mm"))

        if self.printer != None:
            self.printer.show()
            self.printer.writeln(' ')
            self.printer.writeln('                                                                          ')
            if self.release != None:
                self.printer.writeln('Installing MavensMate API (mm) '+self.release['tag_name']+' to the User plugin directory.')
            else:
                self.printer.writeln('Installing the MavensMate API (mm) to the User plugin directory.')
            self.printer.writeln('Timestamp: '+self.process_id)
            self.printer.writeln('   Result:           ')

            self.calculate_process_region()
            PanelThreadProgress(self)

        if 'linux' in sys.platform or 'darwin' in sys.platform:
            import subprocess
            command = [ 'sudo', shutil.which('npm'), 'install', '--prefix', os.path.join(sublime.packages_path(),'User','MavensMate'), 'mavensmate' ]
            debug(command)
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
            install_command_result = ''
            install_command_body = ''
            if process.stdout is not None:
                install_command_result = process.stdout.readlines()
            elif process.stderr is not None:
                install_command_result = process.stderr.readlines()
            try:
                install_command_body = '\n'.join(install_command_result)
            except:
                strs = []
                for line in install_command_result:
                    strs.append(line.decode('utf-8'))
                install_command_body = '\n'.join(strs)

            debug('result of npm install::: ')
            debug(install_command_body)
        else:
            pass

        # ensure_executable_perms()
