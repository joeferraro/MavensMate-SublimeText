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

# returns a list of releases for the current platform
def get_platform_releases(release_data):
    platform_releases = []
    platform_flag = get_platform_flag()
    for r in release_data:
        for asset in r['assets']:
            if platform_flag in asset['name']:
                platform_releases.append(r)
    return platform_releases

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

# returns a list of releases from the joeferraro/mm repository
def get_mm_releases():
    if 'linux' in sys.platform:
        url_exe = platform_util.url_transfer_executable()
        releases = os.popen(url_exe+" https://api.github.com/repos/joeferraro/mm/releases").read()
    else:
        releases = urllib.request.urlopen('https://api.github.com/repos/joeferraro/mm/releases').read().decode('utf-8')    
    return json.loads(releases)

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
        self.beta_user      = self.settings.get('mm_beta_user', False)
        self.release        = kwargs.get('release', None)
        self.platform_flag  = get_platform_flag()
        self.release_data   = get_mm_releases()
        self.latest_release = self.get_latest_release()

        if self.printer == None:
            self.printer = PanelPrinter.get(self.window.id())

        threading.Thread.__init__(self)

    def calculate_process_region(self):
        process_region = self.printer.panel.find(self.process_id,0)
        self.status_region = self.printer.panel.find('   Result: ',process_region.begin())

    def release_has_platform_asset(self, release):
        if not self.beta_user and release['prerelease']:
            return False
        for asset in release['assets']:
           if self.platform_flag in asset['name']:
               return True
        return False

    # iterates the list of mm releases, grabs the latest via the tag name (version number) and platform
    def get_latest_release(self):
        latest = None
        for r in self.release_data:
            if self.beta_user == False and r['prerelease'] == True:
                continue

            if latest == None:
                if self.beta_user and r['prerelease']:
                    if self.release_has_platform_asset(r):
                        latest = r
                        continue
                if self.release_has_platform_asset(r):
                    latest = r
            else:
                if self.beta_user and r['prerelease']:
                    if self.release_has_platform_asset(r):
                        latest_version = int(float(latest['tag_name'].replace("v","").replace(".", "")))
                        r_version = int(float(r['tag_name'].replace("v","").replace(".", "")))
                        if r_version > latest_version:
                            if self.release_has_platform_asset(r):
                                latest = r
                                continue    
                           
                latest_version = int(float(latest['tag_name'].replace("v","").replace(".", "")))
                r_version = int(float(r['tag_name'].replace("v","").replace(".", "")))
                if r_version > latest_version:
                    if self.release_has_platform_asset(r):
                        latest = r
                        continue
        return latest

    def run(self):
        try:
            debug('mm_installer -->')

            if self.release != None:
                ThreadProgress(self, "Installing MavensMate API (mm) "+self.release['tag_name']+". This could take a few minutes.", '')
            else:
                ThreadProgress(self, "Ensuring MavensMate API (mm) is up to date. This could take a few minutes.", '')

            mm_path = self.settings.get('mm_path', 'default')

            if self.force:
                debug('forcing mm installation')
                self.install()

            elif not os.path.isdir(os.path.join(sublime.packages_path(),"User","MavensMate","mm")) and mm_path == 'default':
                # need to download and install
                debug('user mm_path value is default, but mm not installed, forcing install')
                self.install()

            elif mm_path == 'default' and os.path.isdir(os.path.join(sublime.packages_path(),"User","MavensMate","mm")):
                # check version
                debug('checking for updated mm version')
                
                # here we check for version.txt in the User/mm directory
                try:
                    with open (os.path.join(sublime.packages_path(),"User","MavensMate","mm","version.txt"), "r") as version_file:
                        version_data=version_file.read().replace('\n', '')
                    current_version_data = version_data.replace('v','')

                    installed_version_int = int(float(current_version_data.replace(".", "")))
                except:
                    self.install()
                    self.result = 'Success. Please restart Sublime Text -- Happy coding!!'
                    if self.printer != None:
                        self.calculate_process_region()
                        ThreadTracker.remove(self)
                    return

                # compare local version to server (github release) version
                latest_version = self.latest_release['tag_name'].replace('v','')

                server_version_int = int(float(latest_version.replace(".", "")))

                if server_version_int > installed_version_int:
                    debug('mm is out of date, prompting for an update')
                    #if sublime.ok_cancel_dialog("A new version ("+self.latest_release['tag_name']+") of the MavensMate API (mm) is available, you are running "+version_data+". Would you like to update (recommended)? \n\nIf you no longer wish to see these notifications, toggle mm_check_for_updates to false.\n\nIf you would like MavensMate to automatically install updates to mm, set mm_auto_install_mm_updates to true."):
                    if sublime.ok_cancel_dialog("A new version ("+self.latest_release['tag_name']+") of the MavensMate API (mm) is available, you are running "+version_data+". Would you like to update (recommended)? \n\nIf you no longer wish to see these notifications, toggle mm_check_for_updates to false."):
                        if os.path.isdir(os.path.join(sublime.packages_path(),"User","MavensMate","mm")):
                            platform_util.rmtree(os.path.join(sublime.packages_path(),"User","MavensMate","mm"))

                        self.install()
                else:
                    debug('mm is up to date ('+latest_version+'), no further action needed')
            
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

        if os.path.isfile(os.path.join(sublime.packages_path(),"User","MavensMate","mm.zip")):
            os.remove(os.path.join(sublime.packages_path(),"User","MavensMate","mm.zip"))

        if self.release == None:
            release_to_install = self.latest_release
        else:
            # installing a specific release
            release_to_install = self.release

        debug(release_to_install)

        file_name_platform_flag = get_platform_flag()
        
        latest_asset = None
        for a in release_to_install['assets']:
            if file_name_platform_flag in a['name']:
                latest_asset = a
        debug('latest asset ---->')
        debug(latest_asset)
        download_url = latest_asset['browser_download_url']
        debug('attempting to download: ',latest_asset['browser_download_url'])

        if 'linux' in sys.platform:
            import subprocess
            zip_name = 'mm.tar.gz'
            command = "wget -O '"+os.path.join(sublime.packages_path(),"User","MavensMate",zip_name)+"' '"+download_url+"'"
            process = subprocess.Popen(command, shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            download_result = ''
            response_body = ''
            if process.stdout is not None: 
                download_result = process.stdout.readlines()
            elif process.stderr is not None:
                download_result = process.stderr.readlines()
            try:
                response_body = '\n'.join(download_result)
            except:
                strs = []
                for line in download_result:
                    strs.append(line.decode('utf-8'))   
                response_body = '\n'.join(strs)

            debug('result of wget download::: ')
            debug(response_body)
        else:
            zip_name = 'mm.zip'
            with urllib.request.urlopen(download_url) as response, open(os.path.join(sublime.packages_path(),"User","MavensMate",zip_name), 'wb') as out_file:
                data = response.read() # a `bytes` object
                out_file.write(data)

        extract_mm_zip()
        f = open(os.path.join(sublime.packages_path(),"User","MavensMate","mm","version.txt"), 'wb')
        f.write(bytes(release_to_install['tag_name'], 'UTF-8'))
        f.close()

        ensure_executable_perms()

        if os.path.isfile(os.path.join(sublime.packages_path(),"User","MavensMate",zip_name)):
            os.remove(os.path.join(sublime.packages_path(),"User","MavensMate",zip_name))