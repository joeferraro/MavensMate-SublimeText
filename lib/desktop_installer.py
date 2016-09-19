import threading
import os
import sys
import MavensMate.config as config
import time
from MavensMate.lib.printer import PanelPrinter
from .threads import PanelThreadProgress
from .threads import ThreadTracker
import subprocess

debug = config.debug

try:
    from .threads import ThreadProgress
except ImportError as e:
    debug("[MAVENSMATE] import error: ", e)

try:
    import urllib
except ImportError:
    import urllib.request as urllib
import sublime

# explicitly executes DesktopInstaller (downloads and installs latest version of mm to the plugin root)
def execute(printer=None, **kwargs):
    if printer == None:
        printer = PanelPrinter.get(sublime.active_window().id())
    threads = []
    thread = DesktopInstaller(True, printer=printer, **kwargs)
    threads.append(thread)
    thread.start()

def handle_result(operation, process_id, printer, res, thread):
    debug('handling result of MavensMate Desktop update')
    thread.calculate_process_region()
    region = [thread.status_region.end(), thread.status_region.end()+10]
    thread.printer.panel.run_command('write_operation_status', {'text': thread.result, 'region': region })

class DesktopInstaller(threading.Thread):
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

        if self.printer == None:
            self.printer = PanelPrinter.get(self.window.id())

        threading.Thread.__init__(self)

    def calculate_process_region(self):
        process_region = self.printer.panel.find(self.process_id,0)
        self.status_region = self.printer.panel.find('   Result: ',process_region.begin())

    def run(self):
        try:
            debug('mm_installer -->')

            ThreadProgress(self, "Installing MavensMate Desktop. This could take a few minutes.", '')
            self.install()

            settings = sublime.load_settings('mavensmate.sublime-settings')
            settings.set('mm_desktop_installed', True)
            sublime.save_settings('mavensmate.sublime-settings')

            self.result = 'MavensMate Desktop successfully installed. Happy coding!!'
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
        if self.printer != None:
            self.printer.show()
            self.printer.writeln(' ')
            self.printer.writeln('                                                                          ')
            self.printer.writeln('Installing MavensMate Desktop. This could take a few minutes...')
            self.printer.writeln('Timestamp: '+self.process_id)
            self.printer.writeln('   Result:           ')
            self.calculate_process_region()
            PanelThreadProgress(self)

        if sys.platform == 'darwin':
            process = subprocess.Popen([os.path.join(sublime.packages_path(),"MavensMate","bin","install.sh")], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = process.communicate()
            if stderr != None:
                printer = PanelPrinter.get(sublime.active_window())
                printer.show()
                message = '[ERROR]: Could not install MavensMate Desktop. '+stderr.decode('utf-8')
                printer.write('\n'+message+'\n')
        elif sys.platform == 'win32':
            download_url = 'https://mavensmate-app-auto-updater.herokuapp.com/download/channel/beta/'+sys.platform
            download_path = os.path.join(sublime.packages_path(),"User","MavensMate","mavensmate.exe")
            debug('attempting to download: ',download_url)
            # download and write mavensmate.exe to disk
            with urllib.request.urlopen(download_url) as response, open(download_path, 'wb') as out_file:
                data = response.read() # a `bytes` object
                out_file.write(data)
            # call exe (to install it)
            process = subprocess.Popen([download_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = process.communicate()
            if stderr != None:
                printer = PanelPrinter.get(sublime.active_window())
                printer.show()
                message = '[ERROR]: Could not install MavensMate Desktop. '+stderr.decode('utf-8')
                printer.write('\n'+message+'\n')

        elif sys.platform == 'linux':
            pass #todo



