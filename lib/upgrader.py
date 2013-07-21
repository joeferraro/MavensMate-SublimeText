import threading
import MavensMate.config as config
import json
try: 
    import urllib, urllib2
except ImportError:
    import urllib.request as urllib
import sublime

class AutomaticUpgrader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            json_data = open(config.mm_dir+"/packages.json")
            data = json.load(json_data)
            json_data.close()
            current_version = data["packages"][0]["platforms"]["osx"][0]["version"]
            j = json.load(urllib.urlopen("https://raw.github.com/joeferraro/MavensMate-SublimeText/master/packages.json"))
            #TODO
            #j = json.load(urllib.urlopen("https://raw.github.com/joeferraro/MavensMate-SublimeText/2.0/packages.json"))
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
                #if sublime.ok_cancel_dialog("A new version of MavensMate ("+latest_version+") is available. "+release_notes+"Would you like to update?", "Update"):
                    #sublime.set_timeout(lambda: sublime.run_command("update_me"), 1)
                sublime.message_dialog("A new version of MavensMate for Sublime Text ("+latest_version+") is available. To update, select 'Plugins' from the MavensMate.app status bar menu.")
        
        except:
            print('[MAVENSMATE] skipping update check')