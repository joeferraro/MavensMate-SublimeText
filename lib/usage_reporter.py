import threading
import json
import MavensMate.config as config
try: 
    import urllib, urllib2
except ImportError:
    import urllib.request as urllib


class UsageReporter(threading.Thread):
    def __init__(self, action):
        self.action = action
        self.response = None
        threading.Thread.__init__(self)

    def run(self):
        try:
            ip_address = ''
            try:
                #get ip address
                ip_address = urllib2.urlopen('http://ip.42.pl/raw').read()
            except:
                ip_address = 'unknown'

            #get current version of mavensmate
            json_data = open(config.mm_dir+"/packages.json")
            data = json.load(json_data)
            json_data.close()
            current_version = data["packages"][0]["platforms"]["osx"][0]["version"]

            #post to usage servlet
            headers = { "Content-Type":"application/x-www-form-urlencoded" }

            handler = urllib2.HTTPSHandler(debuglevel=0)
            opener = urllib2.build_opener(handler)

            req = urllib2.Request("https://mavensmate.appspot.com/usage", data='version='+current_version+'&ip_address='+ip_address+'&action='+self.action+'', headers=headers)
            self.response = opener.open(req).read()
        except: 
            #traceback.print_exc(file=sys.stdout)
            print('[MAVENSMATE] failed to send usage statistic')
