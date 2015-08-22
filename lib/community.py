import threading
import json
import sublime
import os
import sys
import traceback
import MavensMate.util as util
import MavensMate.lib.platform_util as platform_util
try:
    import MavensMate.config as config
except:
    import config
try:
    import urllib
except ImportError:
    import urllib.request as urllib
try:
    from uuid import getnode as get_mac
except:
    pass

def sync_activity(action):
    settings = sublime.load_settings('mavensmate.sublime-settings')
    if settings.get('mm_send_usage_statistics') == True or settings.get('mm_community_api_token', '') != '':
        sublime.set_timeout(lambda: ActivityHandler(action).start(), 3000)

class ActivityHandler(threading.Thread):
    def __init__(self, action):
        self.action = action or ''
        self.project = util.get_project_name() or ''
        self.response = None
        threading.Thread.__init__(self)

    def run(self):
        try:
            settings = sublime.load_settings('mavensmate.sublime-settings')
            ip_address = ''
            try:
                #get ip address
                if 'linux' in sys.platform:
                    url_exe = platform_util.url_transfer_executable()
                    ip_address = os.popen(url_exe+" http://ip.42.pl/raw").read()
                else:
                    ip_address = urllib.request.urlopen('http://ip.42.pl/raw').read()
            except:
                ip_address = 'unknown'

            #get current version of mavensmate
            #print(os.path.join(config.mm_dir,"packages.json"))
            json_data = open(os.path.join(config.mm_dir,"packages.json"))
            data = json.load(json_data)
            json_data.close()
            current_version = data["packages"][0]["platforms"]["osx"][0]["version"]

            mm_version = ''
            mm_path = settings.get('mm_path', 'default')
            if mm_path == 'default' and os.path.isdir(os.path.join(sublime.packages_path(),"MavensMate","mm")):
                try:
                    with open (os.path.join(sublime.packages_path(),"MavensMate","mm","version.txt"), "r") as version_file:
                        version_data=version_file.read().replace('\n', '')
                    mm_version = version_data.replace('v','')
                except:
                    pass


            if ip_address == None:
                ip_address = 'unknown'
            try:
                mac = str(get_mac())
            except:
                mac = 'unknown'

            community_api_token = settings.get('mm_community_api_token', None)
            if community_api_token != None and community_api_token != '':
                try:
                    api_access_token = settings.get('mm_community_api_token')
                    if 'linux' in sys.platform:
                        b = 'foo=bar&project='+self.project+'&ip_address='+ip_address+'&action='+self.action+'&mm_version='+mm_version+'&platform='+sys.platform+'&plugin_version='+current_version+'&mac_address='+mac
                        url_exe = platform_util.url_transfer_executable()
                        req = os.popen(url_exe+" https://mavensmate.herokuapp.com/api/actions?api_access_token="+api_access_token+" -d='"+b+"'").read()
                        self.response = req
                    else:
                        b = 'mac_address='+mac+'&project='+self.project+'&plugin_version='+current_version+'&ip_address='+ip_address.decode('utf-8')+'&action='+self.action+'&mm_version='+mm_version+'&platform='+sys.platform
                        b = b.encode('utf-8')
                        headers = { "Content-Type":"application/x-www-form-urlencoded" }
                        handler = urllib.request.HTTPSHandler(debuglevel=0)
                        opener = urllib.request.build_opener(handler)
                        req = urllib.request.Request("https://mavensmate.herokuapp.com/api/actions?api_access_token="+api_access_token, data=b, headers=headers)
                        self.response = opener.open(req).read()
                except Exception as e:
                    print('[MAVENSMATE] failed to send community activity, check the value of mm_community_api_token')
                    # traceback.print_exc()
                    print(e)
            else:
                if 'linux' in sys.platform:
                    b = 'foo=bar&ip_address='+ip_address+'&action='+self.action+'&mm_version='+mm_version+'&platform='+sys.platform+'&version='+current_version+'&mac_address='+mac
                    url_exe = platform_util.url_transfer_executable()
                    req = os.popen(url_exe+" https://mavensmate.appspot.com/usage -d='"+b+"'").read()
                    self.response = req
                else:
                    b = 'mac_address='+mac+'&version='+current_version+'&ip_address='+ip_address.decode('utf-8')+'&action='+self.action+'&mm_version='+mm_version+'&platform='+sys.platform
                    b = b.encode('utf-8')
                    #post to usage servlet
                    headers = { "Content-Type":"application/x-www-form-urlencoded" }
                    handler = urllib.request.HTTPSHandler(debuglevel=0)
                    opener = urllib.request.build_opener(handler)
                    req = urllib.request.Request("https://mavensmate.appspot.com/usage", data=b, headers=headers)
                    self.response = opener.open(req).read()
        except Exception as e:
            print('[MAVENSMATE] skipped community activity')
            # print(e)
