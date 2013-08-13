import threading
import json
import plistlib
import sublime
import os
try:
    import MavensMate.config as config
except:
    import config
try: 
    import urllib
except ImportError:
    import urllib.request as urllib


class UsageReporter(threading.Thread):
    def __init__(self, action):
        self.action = action
        self.response = None
        threading.Thread.__init__(self)

    def run(self):
        try:
            settings = sublime.load_settings('mavensmate.sublime-settings')
            ip_address = ''
            try:
                #get ip address
                ip_address = urllib.request.urlopen('http://ip.42.pl/raw').read()
            except:
                ip_address = 'unknown'

            #get current version of mavensmate
            json_data = open(config.mm_dir+"/packages.json")
            data = json.load(json_data)
            json_data.close()
            current_version = data["packages"][0]["platforms"]["osx"][0]["version"]
            mm_version = None
            try:
                dic = plistlib.readPlist(os.path.join(settings.get('mm_app_location'), 'Contents', 'Info.plist'))
                if 'CFBundleVersion' in dic:
                    mm_version = dic['CFBundleVersion']
            except BaseException as e:
                print(e)
                pass

            #post to usage servlet
            headers = { "Content-Type":"application/x-www-form-urlencoded" }

            handler = urllib.request.HTTPSHandler(debuglevel=0)
            opener = urllib.request.build_opener(handler)

            b = 'version='+current_version+'&ip_address='+ip_address.decode('utf-8')+'&action='+self.action+'&mm_version='+mm_version
            b = b.encode('utf-8')
            req = urllib.request.Request("https://mavensmate.appspot.com/usage", data=b, headers=headers)
            self.response = opener.open(req).read()
        except Exception as e: 
            #traceback.print_exc(file=sys.stdout)
            print('[MAVENSMATE] failed to send usage statistic')
            print(e)
