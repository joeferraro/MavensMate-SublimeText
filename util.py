import sublime
import sublime_plugin
import sys
import os
import subprocess
import json
import threading 
import re
import time
import pipes
import shutil
# import string
# import random
# from datetime import datetime, date, time

try: 
    import urllib, urllib2
except ImportError:
    import urllib.request as urllib

try:
    import apex_extensions
except:
    import MavensMate.apex_extensions as apex_extensions

import traceback
from operator import itemgetter
from datetime import datetime
if os.name != 'nt':
    import unicodedata

#PLUGIN_DIRECTORY = os.getcwd().replace(os.path.normpath(os.path.join(os.getcwd(), '..', '..')) + os.path.sep, '').replace(os.path.sep, '/')
#for future reference (windows/linux support)
#sublime.packages_path()
 
try:
    mm_dir = os.getcwdu()
except:
    mm_dir = os.path.dirname(__file__)

settings = sublime.load_settings('mavensmate.sublime-settings')
hide_panel = settings.get('mm_hide_panel_on_success', 1)
hide_time = settings.get('mm_hide_panel_time', 1)
packages_path = sublime.packages_path()
sublime_version = int(float(sublime.version()))

def package_check():
    #ensure user settings are installed
    try:
        if not os.path.exists(packages_path+"/User/mavensmate.sublime-settings"):
            shutil.copyfile(mm_dir+"/mavensmate.sublime-settings", packages_path+"/User/mavensmate.sublime-settings")
    except:
        pass

def mm_call(operation, mm_debug_panel=True, **kwargs):
    settings = sublime.load_settings('mavensmate.sublime-settings')
    if operation != 'new_project' and operation != 'new_project_from_existing_directory' and is_project_legacy() == True:
        operation = 'upgrade_project'
    if not os.path.exists(settings.get('mm_location')):
        active_window_id = sublime.active_window().id()
        printer = PanelPrinter.get(active_window_id)
        printer.show()
        message = '[OPERATION FAILED]: Could not find MavensMate.app. Download MavensMate.app from http://www.joe-ferraro.com/mavensmate/MavensMate.app and place in /Applications. Also, please ensure mm_app_location and mm_location are set properly in Sublime Text (MavensMate --> Settings --> User)'
        printer.write('\n'+message+'\n')
        return

    printer = None
    context = kwargs.get('context', None)
    params  = kwargs.get('params', None)
    if mm_debug_panel:
        try:
            if isinstance(context, sublime.View):
                active_window_id = sublime.active_window().id()
            else:
                active_window_id = context.window.id()
        except:
            active_window_id = sublime.active_window().id()
        printer = PanelPrinter.get(active_window_id)
        printer.show()

    message = 'Handling requested operation...'
    if operation == 'new_metadata':
        message = 'Creating New '+params['metadata_type']+' => ' + params['metadata_name']
    elif operation == 'compile':
        if 'files' in params and len(params['files']) == 1:
            message = 'Compiling => ' + params['files'][0]
        else:
            message = 'Compiling Selected Metadata'
    elif operation == 'compile_project':
        message = 'Compiling Project' 
    elif operation == 'edit_project':
        message = 'Opening Edit Project dialog'  
    elif operation == 'unit_test':
        message = 'Opening Apex Test Runner'
    elif operation == 'clean_project':
        message = 'Cleaning Project'
    elif operation == 'deploy':
        message = 'Opening Deploy dialog'
    elif operation == 'execute_apex':
        message = 'Opening Execute Apex dialog'
    elif operation == 'upgrade_project':
        message = 'Your MavensMate project needs to be upgraded. Opening the upgrade UI.'    
    elif operation == 'index_apex_overlays':
        message = 'Indexing Apex Overlays'  
    elif operation == 'delete':
        if 'files' in params and len(params['files']) == 1:
            message = 'Deleting => ' + get_active_file()
        else:
            message = 'Deleting Selected Metadata'
    elif operation == 'refresh':
        if 'files' in params and len(params['files']) == 1:
            message = 'Refreshing => ' + get_active_file()
        else:
            message = 'Refreshing Selected Metadata'
    elif operation == 'open_sfdc_url':
        message = 'Opening Selected Metadata'
    elif operation == 'new_apex_overlay':
        message = 'Creating Apex Overlay' 
    elif operation == 'delete_apex_overlay':
        message = 'Deleting Apex Overlay'  
    elif operation == 'fetch_logs':
        message = 'Fetching Apex Logs'  
    elif operation == 'project_from_existing_directory':
        message = 'Opening New Project Dialog'   
        
    if mm_debug_panel:
        printer.write('\n'+message+'\n')

    threads = []
    thread = MavensMateTerminalCall(
        operation, 
        project_name=get_project_name(), 
        active_file=get_active_file(), 
        mm_location=settings.get('mm_location'),
        params=params
    )

    threads.append(thread)
    thread.start()
    if mm_debug_panel == False:
        ThreadProgress(thread, message, 'Operation complete')
    thread_progress_handler(operation, threads, printer, 0)

def is_project_legacy():
    if os.path.exists(mm_project_directory()+"/config/settings.yaml"):
        return True
    else:
        return False

#monitors thread for activity, passes to the result handler when thread is complete
def thread_progress_handler(operation, threads, printer, i=0):
    result = None
    next_threads = []
    for thread in threads:
        if printer != None:
            printer.write('.')
        if thread.is_alive():
            next_threads.append(thread)
            continue
        if thread.result == None:
            continue
        result = thread.result

    threads = next_threads

    if len(threads):
        sublime.set_timeout(lambda: thread_progress_handler(operation, threads, printer, i), 200)
        return

    handle_result(operation, printer, result)

#handles the result of the mm script
def handle_result(operation, printer, result):
    try:
        result = json.loads(result)
        print_result_message(operation, result, printer) 
        if operation == 'new_metadata' and to_bool(result['success']) == True:
            if 'messages' in result:
                if type(result['messages']) is not list:
                    result['messages'] = [result['messages']]
                for m in result['messages']:
                    if 'package.xml' not in m['fileName']:
                        file_name = m['fileName']
                        location = mm_project_directory() + "/" + file_name.replace('unpackaged/', 'src/')
                        sublime.active_window().open_file(location)
                        break
        if to_bool(result['success']) == True:
            if printer != None:
                printer.hide()  
        if operation == 'refresh':            
            sublime.set_timeout(lambda: sublime.active_window().active_view().run_command('revert'), 200)
            clear_marked_line_numbers()
    except AttributeError:   
        if printer != None:
            printer.write('\n[OPERATION FAILED]: Whoops, unable to parse the response. Please report this issue at https://github.com/joeferraro/MavensMate-SublimeText')
            printer.write('\n[RESPONSE FROM MAVENSMATE]: '+result+'\n')
    except Exception:
        if printer != None:
            printer.write('\n[OPERATION FAILED]: Whoops, you found a bug. Please report this issue at https://github.com/joeferraro/MavensMate-SublimeText')
            printer.write('\n[RESPONSE FROM MAVENSMATE]: '+result+'\n')

#prints the result of the mm operation, can be a string or a dict
def print_result_message(operation, res, printer):
    #print 'result of operation ', res
    if to_bool(res['success']) == False and 'messages' in res:
        #here we're parsing a response from the metadata endpoint
        line_col = ""
        msg = None
        failures = None
        if type( res['messages'] ) == list:
            for m in res['messages']:
                if 'problem' in m:
                    msg = m
                    break
            if msg == None: #must not have been a compile error, must be a test run error
                if 'run_test_result' in res and 'failures' in res['run_test_result'] and type( res['run_test_result']['failures'] ) == list:
                    failures = res['run_test_result']['failures']
                elif 'failures' in res['run_test_result']:
                    failures = [res['run_test_result']['failures']]
            #print(failures)
        else:
            msg = res['messages']
        if msg != None:
            if 'lineNumber' in msg:
                line_col = ' (Line: '+msg['lineNumber']
                mark_line_numbers([int(float(msg['lineNumber']))], "bookmark")
            if 'columnNumber' in msg:
                line_col += ', Column: '+msg['columnNumber']
            if len(line_col) > 0:
                line_col += ')'
            printer.write('\n[DEPLOYMENT FAILED]: ' + msg['fileName'] + ': ' + msg['problem'] + line_col + '\n')
        elif failures != None:
            for f in failures: 
                printer.write('\n[DEPLOYMENT FAILED]: ' + f['name'] + ', ' + f['methodName'] + ': ' + f['message'] + '\n')
    elif 'success' in res and res["success"] == False and 'line' in res:
        #this is a response from the apex compile api
        line_col = ""
        if 'line' in res:
            line_col = ' (Line: '+res['line']
            mark_line_numbers([int(float(res['line']))], "bookmark")
        if 'column' in res:
            line_col += ', Column: '+res['column']
        if len(line_col) > 0:
            line_col += ')'
        printer.write('\n[COMPILE FAILED]: ' + res['problem'] + line_col + '\n')
    elif 'success' in res and to_bool(res['success']) == True:     
        printer.write('\n[Operation completed Successfully]' + '\n')
    elif to_bool(res['success']) == False and 'body' in res:
        printer.write('\n[OPERATION FAILED]:' + res['body'] + '\n')
    elif to_bool(res['success']) == False:
        printer.write('\n[OPERATION FAILED]' + '\n')
    else:
        printer.write('\n[Operation Completed Successfully]' + '\n')    

def parse_json_from_file(location):
    try:
        json_data = open(location)
        data = json.load(json_data)
        json_data.close()
        return data
    except:
        return {}

def get_number_of_lines_in_file(file_path):
    f = open(file_path)
    lines = f.readlines()
    f.close()
    return len(lines) + 1

def get_execution_overlays(file_path):
    try:
        response = []
        fileName, ext = os.path.splitext(file_path)
        if ext == ".cls" or ext == ".trigger":
            api_name = fileName.split("/")[-1] 
            overlays = parse_json_from_file(mm_project_directory()+"/config/.overlays")
            for o in overlays:
                if o['API_Name'] == api_name:
                    response.append(o)
        return response
    except:
        return []

#creates resource-bundles for the static resource(s) selected        
def create_resource_bundle(self, files):
    for file in files:
        fileName, fileExtension = os.path.splitext(file)
        if fileExtension != '.resource':
            sublime.message_dialog("You can only create resource bundles for static resources")
            return
    printer = PanelPrinter.get(self.window.id())
    printer.show()
    printer.write('\nCreating Resource Bundle(s)\n')

    if not os.path.exists(mm_project_directory()+'/resource-bundles'):
        os.makedirs(mm_project_directory()+'/resource-bundles')

    for file in files:
        fileName, fileExtension = os.path.splitext(file)
        baseFileName = fileName.split("/")[-1]
        if os.path.exists(mm_project_directory()+'/resource-bundles/'+baseFileName+fileExtension):
            printer.write('[OPERATION FAILED]: The resource bundle already exists\n')
            return
        cmd = 'unzip \''+file+'\' -d \''+mm_project_directory()+'/resource-bundles/'+baseFileName+fileExtension+'\''
        res = os.system(cmd)

    printer.write('[Resource bundle creation complete]\n')
    printer.hide()
    send_usage_statistics('Create Resource Bundle') 

def get_active_file():
    try:
        return sublime.active_window().active_view().file_name()
    except Exception as e:
        return ''

def get_project_name():
    try:
        return os.path.basename(sublime.active_window().folders()[0])
    except:
        return None

def check_for_workspace():
    settings = sublime.load_settings('mavensmate.sublime-settings')
    if not os.path.exists(settings.get('mm_workspace')):
        #os.makedirs(settings.get('mm_workspace')) we're not creating the directory here bc there's some sort of weird race condition going on
        msg = 'Your mm_workspace directory does not exist. Please create the directory then try your operation again. Thx!'
        sublime.message_dialog(msg)  
        raise BaseException

def sublime_project_file_path():
    project_directory = sublime.active_window().folders()[0]
    if os.path.isfile(project_directory+"/.sublime-project"):
        return project_directory+"/.sublime-project"
    elif os.path.isfile(project_directory+"/"+get_project_name()+".sublime-project"):
        return project_directory+"/"+get_project_name()+".sublime-project"
    else:
        return None 

# check for mavensmate .settings file
def is_mm_project():
    try:
        json_data = open(sublime_project_file_path())
        data = json.load(json_data)
        pd = data["folders"][0]["path"]
        return os.path.isfile(pd+"/config/.settings")
    except:
        return False

def get_file_extension():
    try :
        active_file = get_active_file()
        if not active_file: return None
        return active_file.split(".")[-1]
    except:
        pass
    return None

def is_mm_file():
    try :
        if not is_mm_project(): return False
        return os.path.isfile(get_active_file()+"-meta.xml")
    except:
        return False

def mm_project_directory():
    #return sublime.active_window().active_view().settings().get('mm_project_directory') #<= bug
    return sublime.active_window().folders()[0]

def mm_workspace():
    settings = sublime.load_settings('mavensmate.sublime-settings')
    workspace = ""
    if settings.get('mm_workspace') != None:
        workspace = settings.get('mm_workspace')
    else:
        workspace = sublime.active_window().active_view().settings().get('mm_workspace')
    return workspace

def mark_overlays(lines):
    mark_line_numbers(lines, "dot", "overlay")

def write_overlays(overlay_result):
    #print 'writing overlays >>>'
    #print(overlay_result)
    result = json.loads(overlay_result)
    if result["totalSize"] > 0:
        for r in result["records"]:
            sublime.set_timeout(lambda: mark_line_numbers([int(r["Line"])], "dot", "overlay"), 100)

def mark_line_numbers(lines, icon="dot", mark_type="compile_issue"):
    points = [sublime.active_window().active_view().text_point(l - 1, 0) for l in lines]
    regions = [sublime.Region(p, p) for p in points]
    sublime.active_window().active_view().add_regions(mark_type, regions, "operation.fail",
        icon, sublime.HIDDEN | sublime.DRAW_EMPTY)

def clear_marked_line_numbers(mark_type="compile_issue"):
    try:
        sublime.set_timeout(lambda: sublime.active_window().active_view().erase_regions(mark_type), 100)
    except Exception as e:
        print(e.message)
        print('no regions to clean up')

def compile_callback(result):
    try:
        result = json.loads(result)
        if result['success'] == True:
            clear_marked_line_numbers()
    except:
        print('[MAVENSMATE] Issue handling compile result')

def print_debug_panel_message(message):
    printer = PanelPrinter.get(sublime.active_window().id())
    printer.show()
    printer.write(message)

#parses the input from sublime text
def parse_new_metadata_input(input):
    input = input.replace(" ", "")
    if "," in input:
        params = input.split(",")
        api_name = params[0]
        class_type_or_sobject_name = params[1]
        return api_name, class_type_or_sobject_name
    else:
        return input

def to_bool(value):
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if str(value).lower() in ("yes", "y", "true",  "t", "1"): return True
    if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))

def get_tab_file_names():
    tabs = []
    win = sublime.active_window()
    for vw in win.views():
        if vw.file_name() is not None:
            try:
                extension = os.path.splitext(vw.file_name())[1]
                extension = extension.replace(".","")
                if extension in apex_extensions.valid_extensions:
                    tabs.append(vw.file_name())
            except:
                pass
        else:
            pass      # leave new/untitled files (for the moment)
    return tabs 

def send_usage_statistics(action):
    settings = sublime.load_settings('mavensmate.sublime-settings')
    if settings.get('mm_send_usage_statistics') == True:
        sublime.set_timeout(lambda: UsageReporter(action).start(), 3000)

def refresh_active_view():
    sublime.set_timeout(sublime.active_window().active_view().run_command('revert'), 100)

def check_for_updates():
    settings = sublime.load_settings('mavensmate.sublime-settings')
    if settings.get('mm_check_for_updates') == True:
        sublime.set_timeout(lambda: AutomaticUpgrader().start(), 5000)

def index_overlays():
    mm_call('index_apex_overlays', False)
    send_usage_statistics('Index Apex Overlays')  

#preps code completion object for search in doxygen documentation
def prep_for_search(name): 
    #s1 = re.sub('(.)([A-Z]+)', r'\1_\2', name).strip()
    #return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    #return re.sub('([A-Z])', r'\1_', name)
    return name.replace('_', '')

def start_mavensmate_app():
    p = subprocess.Popen("pgrep -fl MavensMate", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    msg = None
    if p.stdout is not None: 
        msg = p.stdout.readlines()
    elif p.stderr is not None:
        msg = p.stdout.readlines() 
    if msg == '' or len(msg) == 0:
        os.system("open '"+settings.get('mm_app_location')+"'")

class UsageReporter(threading.Thread):
    def __init__(self, action):
        self.action = action
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
            json_data = open(mm_dir+"/packages.json")
            data = json.load(json_data)
            json_data.close()
            current_version = data["packages"][0]["platforms"]["osx"][0]["version"]

            #post to usage servlet
            url = "https://mavensmate.appspot.com/usage"
            headers = { "Content-Type":"application/x-www-form-urlencoded" }

            handler = urllib2.HTTPSHandler(debuglevel=0)
            opener = urllib2.build_opener(handler)

            req = urllib2.Request("https://mavensmate.appspot.com/usage", data='version='+current_version+'&ip_address='+ip_address+'&action='+self.action+'', headers=headers)
            response = opener.open(req).read()
            #print response
        except: 
            #traceback.print_exc(file=sys.stdout)
            print('[MAVENSMATE] failed to send usage statistic')

class ThreadProgress():
    """
    Animates an indicator, [=   ], in the status area while a thread runs

    :param thread:
        The thread to track for activity

    :param message:
        The message to display next to the activity indicator

    :param success_message:
        The message to display once the thread is complete
    """

    def __init__(self, thread, message, success_message, callback=None):
        self.thread = thread
        self.message = message
        self.success_message = success_message
        self.addend = 1
        self.size = 8
        self.callback = None
        sublime.set_timeout(lambda: self.run(0), 100)

    def run(self, i):
        if not self.thread.is_alive():
            if hasattr(self.thread, 'result') and not self.thread.result:
                sublime.status_message('')
                return
            sublime.status_message(self.success_message)
            if self.callback != None:
                self.callback()
            return

        before = i % self.size
        after = (self.size - 1) - before

        sublime.status_message('%s [%s=%s]' % \
            (self.message, ' ' * before, ' ' * after))

        if not after:
            self.addend = -1
        if not before:
            self.addend = 1
        i += self.addend

        sublime.set_timeout(lambda: self.run(i), 100)

def finish_update():
    sublime.message_dialog("MavensMate has been updated successfully!")
    printer = PanelPrinter.get(sublime.active_window().id())
    printer.hide()    

def get_version_number():
    try:
        json_data = open(mm_dir+"/packages.json")
        data = json.load(json_data)
        json_data.close()
        version = data["packages"][0]["platforms"]["osx"][0]["version"]
        return version
    except:
        return ''

class AutomaticUpgrader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            json_data = open(mm_dir+"/packages.json")
            data = json.load(json_data)
            json_data.close()
            current_version = data["packages"][0]["platforms"]["osx"][0]["version"]
            #j = json.load(urllib.urlopen("https://raw.github.com/joeferraro/MavensMate-SublimeText/master/packages.json"))
            j = json.load(urllib.urlopen("https://raw.github.com/joeferraro/MavensMate-SublimeText/2.0/packages.json"))
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

#calls out to the ruby scripts that interact with the metadata api
#pushes them to background threads and reads the piped response
class MavensMateTerminalCall(threading.Thread):
    def __init__(self, operation, **kwargs):
        self.operation      = operation
        self.project_name   = kwargs.get('project_name', None)
        self.active_file    = kwargs.get('active_file', None)
        self.mm_location    = kwargs.get('mm_location', None)
        self.params         = kwargs.get('params', None)
        self.process        = None
        self.result         = None
        self.callback       = None
        if self.params != None:
            self.callback   = self.params.get('callback', None)
        threading.Thread.__init__(self)

    def get_arguments(self, ui=False, html=False):
        args = {
            '-o'        : self.operation,
            '--html'    : html
        }
        if sublime_version >= 3000:
            args['-c'] = 'SUBLIME_TEXT_3'
        else:
            args['-c'] = 'SUBLIME_TEXT_2'
        ui_operations = ['edit_project', 'new_project', 'unit_test', 'deploy', 'execute_apex', 'upgrade_project', 'new_project_from_existing_directory']
        if self.operation in ui_operations:
            args['--ui'] = True

        arg_string = []
        for x in args.keys():
            if args[x] != None and args[x] != True and args[x] != False:
                arg_string.append(x + ' ' + args[x] + ' ')
            elif args[x] == True or args[x] == None:
                arg_string.append(x + ' ')
        stripped_string = ''.join(arg_string).strip()
        return stripped_string

    def submit_payload(self):
        payload = ''
        if self.operation == 'edit_project':
            payload = {
                'project_name' : self.project_name
            }
        elif self.operation == 'upgrade_project':
            payload = {
                'project_name' : self.project_name
            }
        elif self.operation == 'unit_test' or self.operation == 'execute_apex' or self.operation == 'compile_project':
            payload = {
                'project_name' : self.project_name
            }    
        elif self.operation == 'compile':
            payload = {
                'project_name'  : self.project_name,
                'files'         : self.params.get('files', [])
            }
        elif self.operation == 'index_apex_overlays':
            payload = {
                'project_name'  : self.project_name
            }
        elif self.operation == 'new_metadata':
            payload = {
                'project_name'                  : self.project_name,
                'api_name'                      : self.params.get('metadata_name', None),
                'metadata_type'                 : self.params.get('metadata_type', None),
                'apex_trigger_object_api_name'  : self.params.get('object_api_name', None),
                'apex_class_type'               : self.params.get('apex_class_type', None)
            }
        elif self.operation == 'clean_project':
            payload = {
                'project_name'  : self.project_name
            }
        elif self.operation == 'deploy':
            payload = {
                'project_name'  : self.project_name
            }
        elif self.operation == 'refresh':
            if 'files' in self.params:
                payload = {
                    'project_name'  : self.project_name,
                    'files'         : self.params.get('files', []),
                }
            elif 'directories' in self.params:
                payload = {
                    'project_name'  : self.project_name,
                    'directories'   : self.params.get('directories', [])
                }
            else:
                payload = {
                    'project_name'  : self.project_name,
                    'directories'   : self.params.get('directories', []),
                    'files'         : self.params.get('files', [])
                }
        elif self.operation == 'open_sfdc_url':
                payload = {
                    'project_name'  : self.project_name,
                    'files'         : self.params.get('files', []),
                    'type'          : self.params.get('type', "edit")
                }
        elif self.operation == 'delete':
            payload = {
                'project_name'  : self.project_name,
                'files'         : self.params.get('files', [])
            }
        elif self.operation == 'fetch_logs':
            payload = {
                'project_name'  : self.project_name
            }
        elif self.operation == 'new_apex_overlay':
            payload = self.params
            payload['project_name'] = self.project_name
        elif self.operation == 'delete_apex_overlay':
            payload = self.params
            payload['project_name'] = self.project_name
        elif self.operation == 'new_project_from_existing_directory':
            payload = self.params

        if type(payload) is dict:
            payload = json.dumps(payload)  
        print(payload)  
        try:
            self.process.stdin.write(payload)
        except:
            self.process.stdin.write(payload.encode('utf-8'))
        self.process.stdin.close()

    def run(self):
        print('[MAVENSMATE] executing mm terminal call')
        print("{0} {1}".format(pipes.quote(self.mm_location), self.get_arguments()))
        self.process = subprocess.Popen("{0} {1}".format(pipes.quote(self.mm_location), self.get_arguments()), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        self.submit_payload()
        if self.process.stdout is not None: 
            mm_response = self.process.stdout.readlines()
        elif self.process.stderr is not None:
            mm_response = self.process.stderr.readlines()
        try:
            response_body = '\n'.join(mm_response)
        except:
            strs = []
            for line in mm_response:
                strs.append(line.decode('utf-8'))   
            response_body = '\n'.join(strs)

        print('[MAVENSMATE] response from mm: ' + response_body)
        self.result = response_body
        if self.operation == 'compile':
            compile_callback(response_body)
        if self.operation == 'new_apex_overlay' or self.operation == 'delete_apex_overlay':
            sublime.set_timeout(lambda : index_overlays(), 100)
        if self.callback != None:
            print(self.callback)
            self.callback(response_body)


#class representing the MavensMate activity/debug panel in Sublime Text
class PanelPrinter(object):
    printers = {}

    def __init__(self):
        self.name = 'MavensMate-OutputPanel'
        self.visible = False
        self.hide_time = hide_time
        self.queue = []
        self.strings = {}
        self.just_error = False
        self.capture = False
        self.input = None
        self.input_start = None
        self.on_input_complete = None
        self.original_view = None

    @classmethod
    def get(cls, window_id):
        printer = cls.printers.get(window_id)
        if not printer:
            printer = PanelPrinter()
            printer.window_id = window_id
            printer.init()
            cls.printers[window_id] = printer
            printer.write('==============================================\n')
            printer.write('<---- MavensMate for Sublime Text v'+get_version_number()+' ---->\n')
            printer.write('==============================================\n')
        return printer

    def error(self, string):
        callback = lambda : self.error_callback(string)
        sublime.set_timeout(callback, 1)

    def error_callback(self, string):
        string = str(string)
        self.reset_hide()
        self.just_error = True
        sublime.error_message('MavensMate: ' + string)

    def hide(self, thread = None):
        settings = sublime.load_settings('mavensmate.sublime-settings')
        hide = settings.get('mm_hide_panel_on_success', True)
        if hide == True:
            hide_time = time.time() + float(hide)
            self.hide_time = hide_time
            sublime.set_timeout(lambda : self.hide_callback(hide_time, thread), int(hide * 300))

    def hide_callback(self, hide_time, thread):
        if thread:
            last_added = ThreadTracker.get_last_added(self.window_id)
            if thread != last_added:
                return
        if self.visible and self.hide_time and hide_time == self.hide_time:
            if not self.just_error:
                self.window.run_command('hide_panel')
            self.just_error = False

    def init(self):
        if not hasattr(self, 'panel'):
            self.window = sublime.active_window()
            self.panel = self.window.get_output_panel(self.name)
            self.panel.set_read_only(True)
            self.panel.settings().set('syntax', 'Packages/MavensMate/themes/MavensMate.hidden-tmLanguage')
            self.panel.settings().set('color_scheme', 'Packages/MavensMate/themes/MavensMate.hidden-tmTheme')
            self.panel.settings().set('word_wrap', True)
            self.panel.settings().set('gutter', True)
            self.panel.settings().set('line_numbers', True)

    def reset_hide(self):
        self.hide_time = None

    def show(self, force = False):
        self.init()
        settings = sublime.load_settings('mavensmate.sublime-settings')
        hide = settings.get('hide_output_panel', 1)
        if force or hide != True or not isinstance(hide, bool):
            self.visible = True
            self.window.run_command('show_panel', {'panel': 'output.' + self.name})

    def write(self, string, key = 'sublime_mm', finish = False):
        if not len(string) and not finish:
            return
        if key not in self.strings:
            self.strings[key] = []
            self.queue.append(key)
        if len(string):
            try:
                if not isinstance(string, unicode):
                    string = unicode(string, 'UTF-8', errors='strict')
            except:
                if type(string) is not str:
                    string = str(string, 'utf-8')
            if os.name != 'nt':
                string = unicodedata.normalize('NFC', string)
            self.strings[key].append(string)
        if finish:
            self.strings[key].append(None)
        sublime.set_timeout(self.write_callback, 0)
        return key

    def write_callback(self):
        if sublime_version >= 3000:
            found = False
            for key in self.strings.keys():
                if len(self.strings[key]):
                    found = True
            if not found:
                return
            string = self.strings[key].pop(0)
            self.panel.run_command('mavens_mate_output_text', {'text': string})
            
            size = self.panel.size()
            sublime.set_timeout(lambda : self.panel.show(size, True), 2)

            return
        else:
            found = False
            for key in self.strings.keys():
                if len(self.strings[key]):
                    found = True
            if not found:
                return
            read_only = self.panel.is_read_only()
            if read_only:
                self.panel.set_read_only(False)
            edit = self.panel.begin_edit()
            keys_to_erase = []
            for key in list(self.queue):
                while len(self.strings[key]):
                    string = self.strings[key].pop(0)
                    if string == None:
                        self.panel.erase_regions(key)
                        keys_to_erase.append(key)
                        continue
                    if key == 'sublime_mm':
                        point = self.panel.size()
                    else:
                        regions = self.panel.get_regions(key)
                        if not len(regions):
                            point = self.panel.size()
                        else:
                            region = regions[0]
                            point = region.b + 1
                    if point == 0 and string[0] == '\n':
                        string = string[1:]
                    self.panel.insert(edit, point, string)
                    if key != 'sublime_mm':
                        point = point + len(string) - 1
                        region = sublime.Region(point, point)
                        self.panel.add_regions(key, [region], '')
        
            for key in keys_to_erase:
                if key in self.strings:
                    del self.strings[key]
                try:
                    self.queue.remove(key)
                except ValueError:
                    pass
            
            self.panel.end_edit(edit)
            if read_only:
                self.panel.set_read_only(True)
            size = self.panel.size()
            sublime.set_timeout(lambda : self.panel.show(size, True), 2)

