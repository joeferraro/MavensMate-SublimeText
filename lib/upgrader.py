import threading
import json
import os
import sys
import subprocess

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
    PanelThreadProgress(thread)
    ThreadTracker(thread)

def handle_result(operation, process_id, printer, result, thread):
    process_region = printer.panel.find(process_id,0)
    status_region = printer.panel.find('Result:',process_region.begin())
    printer.panel.run_command('write_operation_status', {'text': result, 'region': [status_region.end(), status_region.end()+10] })
    printer.scroll_to_bottom()

class ManualUpgrader(threading.Thread):
    def __init__(self, printer):
        self.printer        = printer
        self.operation      = "upgrade"
        self.process_id     = "upgrade"
        self.result         = None
        self.callback       = handle_result
        threading.Thread.__init__(self)

    def run(self):
        process = None
        if 'linux' in sys.platform:
            updater_path = os.path.join(sublime.packages_path(),"MavensMate","install-dev.py")
            settings = sublime.load_settings('mavensmate.sublime-settings')
            python_location = settings.get("mm_python_location")
            #subprocess.Popen('"{0}" "{1}"'.format(python_location, updater_path), startupinfo=startupinfo)
            process = subprocess.Popen('"{0}" "{1}"'.format(python_location, updater_path), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        elif 'darwin' in sys.platform:
            sublime.message_dialog("A new version of MavensMate for Sublime Text ("+latest_version+") is available."+release_notes+"To update, select 'Plugins' from the MavensMate.app status bar menu, then \"Update Plugin\".\n\nYou will need to restart Sublime Text after updating.")
        else: #windows
            updater_path = os.path.join(os.environ["ProgramFiles"],"MavensMate","MavensMate-SublimeText.exe")
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen('"{0}"'.format(updater_path), startupinfo=startupinfo)

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
                    #sublime.message_dialog("A new version of MavensMate for Sublime Text ("+latest_version+") is available."+release_notes+"To update, download the package from https://github.com/joeferraro/MavensMate-SublimeText and place in the Sublime Text packages directory.")
                    if sublime.ok_cancel_dialog("A new version of MavensMate for Sublime Text ("+latest_version+") is available."+release_notes+"Would you like to update?"):
                        updater_path = os.path.join(sublime.packages_path(),"MavensMate","install-dev.py")
                        settings = sublime.load_settings('mavensmate.sublime-settings')
                        python_location = settings.get("mm_python_location")
                        startupinfo = subprocess.STARTUPINFO()
                        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                        #subprocess.Popen('"{0}" "{1}"'.format(python_location, updater_path), startupinfo=startupinfo)
                        subprocess.Popen('"{0}" "{1}"'.format(python_location, updater_path), startupinfo=startupinfo)
                elif 'darwin' in sys.platform:
                    sublime.message_dialog("A new version of MavensMate for Sublime Text ("+latest_version+") is available."+release_notes+"To update, select 'Plugins' from the MavensMate.app status bar menu, then \"Update Plugin\".\n\nYou will need to restart Sublime Text after updating.")
                else: #windows
                    if sublime.ok_cancel_dialog("A new version of MavensMate for Sublime Text ("+latest_version+") is available."+release_notes+"Would you like to update?"):
                        updater_path = os.path.join(os.environ["ProgramFiles"],"MavensMate","MavensMate-SublimeText.exe")
                        startupinfo = subprocess.STARTUPINFO()
                        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                        subprocess.Popen('"{0}"'.format(updater_path), startupinfo=startupinfo)

        except BaseException as e:
            # import traceback
            # import sys
            # traceback.print_exc(file=sys.stdout)            
            print('[MAVENSMATE] skipping update check')
            print(e)