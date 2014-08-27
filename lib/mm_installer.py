import threading
import json
import os
import stat
import sys
import shutil

from zipfile import ZipFile
try:
    from .threads import ThreadProgress
except ImportError as e:
    print("[MAVENSMATE] import error: ", e)

try: 
    import urllib
except ImportError:
    import urllib.request as urllib
import sublime

def execute():
    threads = []
    thread = MmInstaller(True)
    threads.append(thread)        
    thread.start()

# iterates the list of mm releases, grabs the latest via the tag name (version number)
def get_latest_release(release_data):
    latest = None
    for r in release_data:
        if latest == None:
            latest = r
        else:
            latest_version = int(float(latest['tag_name'].replace("v","").replace(".", "")))
            r_version = int(float(r['tag_name'].replace("v","").replace(".", "")))
            if r_version > latest_version:
                latest = r
    return latest

# extracts mm.zip into a top-level subdirectory called 'mm'
def extract_mm_zip():
    file_location = os.path.join(sublime.packages_path(),"MavensMate","mm.zip")
    dest_dir = os.path.join(sublime.packages_path(),"MavensMate")
    
    with ZipFile(file_location) as zf:
        zf.extractall(dest_dir)

def ensure_executable_perms():
    mm_stat = os.stat(os.path.join(sublime.packages_path(),"MavensMate","mm","mm"))
    os.chmod(os.path.join(sublime.packages_path(),"MavensMate","mm","mm"), mm_stat.st_mode | stat.S_IEXEC)

    mavensmate_app_stat = os.stat(os.path.join(sublime.packages_path(),"MavensMate","mm","lib","bin","MavensMateWindowServer.app","Contents","MacOS","MavensMateWindowServer"))
    os.chmod(os.path.join(sublime.packages_path(),"MavensMate","mm","lib","bin","MavensMateWindowServer.app","Contents","MacOS","MavensMateWindowServer"), mavensmate_app_stat.st_mode | stat.S_IEXEC)

def get_mm_releases():
    # https://api.github.com/repos/joeferraro/mm/releases
    if 'linux' in sys.platform:
        # https://github.com/joeferraro/mm/releases/download/v0.1.9/mm-osx.zip
        releases = os.popen('curl https://api.github.com/repos/joeferraro/mm/releases').read()
    else:
        releases = urllib.request.urlopen('https://api.github.com/repos/joeferraro/mm/releases').read().decode('utf-8')    
    return json.loads(releases)

class MmInstaller(threading.Thread):
    def __init__(self, force=False, version=None):
        self.force = force
        self.version = version
        threading.Thread.__init__(self)

    def run(self):
        print('running MmInstaller!!!!')
        try:
            if os.path.isfile(os.path.join(sublime.packages_path(),"MavensMate","mm.zip")):
                os.remove(os.path.join(sublime.packages_path(),"MavensMate","mm.zip"))

            settings = sublime.load_settings('mavensmate.sublime-settings')
            mm_location = settings.get('mm_location', 'default')

            if self.force:
                if os.path.isdir(os.path.join(sublime.packages_path(),"MavensMate","mm")):
                    shutil.rmtree(os.path.join(sublime.packages_path(),"MavensMate","mm"))
                self.install()

            elif not os.path.isdir(os.path.join(sublime.packages_path(),"MavensMate","mm")) and mm_location == 'default':
                # need to download and install
                self.install()

            elif mm_location == 'default' and os.path.isdir(os.path.join(sublime.packages_path(),"MavensMate","mm")):
                # check version
                with open (os.path.join(sublime.packages_path(),"MavensMate","mm","version.txt"), "r") as version_file:
                    version_data=version_file.read().replace('\n', '')
                current_version_data = version_data.replace('v','')

                installed_version_int = int(float(current_version_data.replace(".", "")))

                release_data = get_mm_releases()

                latest_release = get_latest_release(release_data)
                latest_version = latest_release['tag_name'].replace('v','')

                server_version_int = int(float(latest_version.replace(".", "")))

                if server_version_int > installed_version_int:
                    if sublime.ok_cancel_dialog("A new version of the MavensMate API, mm, is available. Would you like to update (recommended)?"):
                        if os.path.isdir(os.path.join(sublime.packages_path(),"MavensMate","mm")):
                            shutil.rmtree(os.path.join(sublime.packages_path(),"MavensMate","mm"))

                        self.install()
                else:
                    print('mm is up to date!')
            

        except BaseException as e:
            import traceback
            import sys
            traceback.print_exc(file=sys.stdout)            
            print('[MAVENSMATE] could not update mm')
            print(e)

    def install(self):
        ThreadProgress(self, "Installing MavensMate API (mm). This could take a few minutes.", 'MavensMate API (mm) update complete.')

        # https://api.github.com/repos/joeferraro/mm/releases
        if 'linux' in sys.platform:
            # https://github.com/joeferraro/mm/releases/download/v0.1.9/mm-osx.zip
            releases = os.popen('curl https://api.github.com/repos/joeferraro/mm/releases').read()
        else:
            releases = urllib.request.urlopen('https://api.github.com/repos/joeferraro/mm/releases').read().decode('utf-8')
        release_data = json.loads(releases)

        latest_release = get_latest_release(release_data)
        print(latest_release)

        file_name_platform_flag = None
        if 'linux' in sys.platform:
            file_name_platform_flag = 'linux'
        elif 'darwin' in sys.platform:
            file_name_platform_flag = 'osx'
        else:
            file_name_platform_flag = 'win'

        latest_asset = None
        for a in latest_release['assets']:
            if file_name_platform_flag in a['name']:
                latest_asset = a
        print('latest asset ---->')
        print(latest_asset)

        with urllib.request.urlopen(latest_asset['browser_download_url']) as response, open(os.path.join(sublime.packages_path(),"MavensMate","mm.zip"), 'wb') as out_file:
            data = response.read() # a `bytes` object
            out_file.write(data)

        extract_mm_zip()
        f = open(os.path.join(sublime.packages_path(),"MavensMate","mm","version.txt"), 'wb')
        f.write(bytes(latest_release['tag_name'], 'UTF-8'))
        f.close()

        ensure_executable_perms()

        if os.path.isfile(os.path.join(sublime.packages_path(),"MavensMate","mm.zip")):
            os.remove(os.path.join(sublime.packages_path(),"MavensMate","mm.zip"))