import threading
import json
import os
import sys
import subprocess
try:
    import MavensMate.config as config
except:
    import config
try: 
    import urllib
except ImportError:
    import urllib.request as urllib
import sublime

class AutomaticUpgrader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            json_data = open(os.path.join(config.mm_dir,"packages.json"))
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
                    sublime.message_dialog("A new version of MavensMate for Sublime Text ("+latest_version+") is available."+release_notes+"To update, download the package from https://github.com/joeferraro/MavensMate-SublimeText and place in the Sublime Text packages directory.")
                elif 'darwin' in sys.platform:
                    sublime.message_dialog("A new version of MavensMate for Sublime Text ("+latest_version+") is available."+release_notes+"To update, select 'Plugins' from the MavensMate.app status bar menu, then \"Update Plugin\".\n\nYou will need to restart Sublime Text after updating.")
                else: #windows
                    if sublime.ok_cancel_dialog("A new version of MavensMate for Sublime Text ("+latest_version+") is available."+release_notes+"Would you like to update?"):
                        updater_path = os.path.join(os.environ["ProgramFiles"],"MavensMate","MavensMate-SublimeText.exe")
                        #os.system('"{0}"'.format(updater_path))
                        startupinfo = subprocess.STARTUPINFO()
                        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                        subprocess.Popen('"{0}"'.format(updater_path), startupinfo=startupinfo)

        except BaseException as e:
            # import traceback
            # import sys
            # traceback.print_exc(file=sys.stdout)            
            print('[MAVENSMATE] skipping update check')
            print(e)