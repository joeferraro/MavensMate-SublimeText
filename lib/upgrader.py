import threading
import json
import os
import sys
import subprocess
import time
try:
    import plistlib
except:
    pass


try:
    from .threads import ThreadTracker
    from .threads import ThreadProgress
    from .threads import PanelThreadProgress
except ImportError as e:
    print("[MAVENSMATE] import error: ", e)

try: 
    import urllib
except ImportError:
    import urllib.request as urllib
import sublime

def execute(printer):
    threads = []
    thread = ManualUpgrader(printer)
    threads.append(thread)        
    thread.start()

def handle_result(operation, process_id, printer, result, thread):
    process_region = printer.panel.find(process_id,0)
    status_region = printer.panel.find('Result:',process_region.begin())
    printer.panel.run_command('write_operation_status', {'text': result, 'region': [status_region.end(), status_region.end()+10] })
    printer.scroll_to_bottom()

class ManualUpgrader(threading.Thread):
    def __init__(self, printer):
        self.printer        = printer
        self.operation      = "upgrade"
        self.process_id     = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        self.result         = None
        self.callback       = handle_result
        self.alt_callback   = None
        self.status_region  = None

        self.printer.show()
        self.printer.writeln(' ')
        self.printer.writeln('==============================================')
        self.printer.writeln("Reloading MavensMate for Sublime Text Plugin. You will need to restart Sublime Text when update is complete. If you have any issues updating, open a terminal and run the python installer script located here: https://raw.github.com/joeferraro/MavensMate-SublimeText/master/install.py. Example (from the terminal): $ python install.py")
        self.printer.writeln('Timestamp: '+self.process_id)

        threading.Thread.__init__(self)

    def run(self):
        if 'linux' in sys.platform or 'darwin' in sys.platform:
            ThreadProgress(self, "Updating MavensMate for Sublime Text", 'MavensMate update complete. Please restart Sublime Text.')
            process = None
            
            updater_path = os.path.join(sublime.packages_path(),"MavensMate","install.py")
            settings = sublime.load_settings('mavensmate.sublime-settings')
            python_location = settings.get("mm_python_location")
            process = subprocess.Popen('"{0}" "{1}"'.format(python_location, updater_path), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        
            mm_response = ""
            if process != None:
                if process.stdout is not None: 
                    mm_response = process.stdout.readlines()
                elif process.stderr is not None:
                    mm_response = process.stderr.readlines()
                try:
                    response_body = '\n'.join(mm_response)
                except:
                    strs = []
                    for line in mm_response:
                        strs.append(line.decode('utf-8'))   
                    response_body = '\n'.join(strs)

            print('[MAVENSMATE] response from upgrader: ' + response_body)
            self.result = response_body

class AutomaticUpgrader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            json_data = open(os.path.join(sublime.packages_path(),"MavensMate","packages.json"))
            data = json.load(json_data)
            json_data.close()
            current_version = data["packages"][0]["platforms"]["osx"][0]["version"]
            if 'linux' in sys.platform:
                response = os.popen('curl https://raw.github.com/joeferraro/MavensMate-SublimeText/master/packages.json').read()
            else:
                response = urllib.request.urlopen('https://raw.github.com/joeferraro/MavensMate-SublimeText/master/packages.json').read().decode('utf-8')
            j = json.loads(response)
            latest_version = j["packages"][0]["platforms"]["osx"][0]["version"]
            release_notes = "\n\nRelease Notes: "
            try:
                release_notes += j["packages"][0]["platforms"]["osx"][0]["release_notes"] + "\n\n"
            except:
                release_notes = ""

            installed_version_int = int(float(current_version.replace(".", "")))
            server_version_int = int(float(latest_version.replace(".", "")))

            needs_update = False
            if server_version_int > installed_version_int:
                needs_update = True
            
            if needs_update == True:
                if 'linux' in sys.platform:
                    sublime.message_dialog("A new version of MavensMate for Sublime Text ("+latest_version+") is available."+release_notes+"To update, select MavensMate > Update MavensMate from the Sublime Text menu.")
                elif 'darwin' in sys.platform:
                    sublime.message_dialog("A new version of MavensMate for Sublime Text ("+latest_version+") is available."+release_notes+"To update, select MavensMate > Update MavensMate from the Sublime Text menu.")
                else: #windows
                    if sublime.ok_cancel_dialog("A new version of MavensMate for Sublime Text ("+latest_version+") is available."+release_notes+"Would you like to update?"):
                        updater_path = os.path.join(os.environ["ProgramFiles"],"MavensMate","MavensMate-SublimeText.exe")
                        if not os.path.isfile(updater_path):
                            updater_path = updater_path.replace("Program Files", "Program Files (x86)")
                        startupinfo = subprocess.STARTUPINFO()
                        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                        subprocess.Popen('"{0}"'.format(updater_path), startupinfo=startupinfo)
            else:
                if 'darwin' in sys.platform:
                    settings = sublime.load_settings('mavensmate.sublime-settings')
                    mm_app_location = settings.get("mm_app_location")
                    plist_path = mm_app_location+"/Contents/Info.plist"

                    plist = plistlib.readPlist(plist_path)
                    version_number = plist['CFBundleVersion']
                    installed_version_int = int(float(version_number.replace(".", "")))
                    if installed_version_int <= 383:
                        sublime.message_dialog("A new version of MavensMate.app is available and we strongly encourage you to update. If you are running 0.38.0, you likely need to manually download and re-install from mavensmate.com.")

        except BaseException as e:
            # import traceback
            # import sys
            # traceback.print_exc(file=sys.stdout)            
            print('[MAVENSMATE] skipping update check')
            print(e)