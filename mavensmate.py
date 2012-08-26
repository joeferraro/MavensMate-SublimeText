# Written by Joe Ferraro (@joeferraro / www.joe-ferraro.com)
import sublime
import sublime_plugin
import os
import sys
import subprocess
import threading  
import time
import tempfile 
import ast
import copy
if os.name != 'nt':
    import unicodedata
 
mm_dir = os.getcwdu()
settings = sublime.load_settings('mavensmate.sublime-settings')
hide_panel = settings.get('mm_hide_panel_on_success', 1)
hide_time = settings.get('mm_hide_panel_time', 1)

def get_ruby():
    ruby = "ruby"    
    if settings.get('mm_ruby') != None: 
        ruby = settings.get('mm_ruby')
    return ruby

ruby = get_ruby()

def start_local_server():
    cmd = ruby+" -r '"+mm_dir+"/support/lib/local_server.rb' -e 'MavensMate::LocalServer.start'"
    os.system(cmd)

def stop_local_server():
    cmd_b = ruby+" -r '"+mm_dir+"/support/lib/local_server.rb' -e 'MavensMate::LocalServer.stop'"

def generate_ui(ruby_script, arg0):
    cmd = ruby+" '"+mm_dir+"/commands/"+ruby_script+".rb' '"+arg0+"'"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    if p.stdout is not None : 
        msg = p.stdout.readlines()
    temp = tempfile.NamedTemporaryFile(delete=False, prefix="mm")
    try:
        temp.write('\n'.join(msg))
    finally:
        temp.close()
    return temp.name

def launch_mavens_mate_window(temp_file_name):
    os.system("open '"+mm_dir+"/bin/MavensMate.app' --args -url '"+temp_file_name+"'")
    time.sleep(1) 
    os.remove(temp_file_name) #<= we may want to move this delete call to the binary

def kill_mavens_mate_window():
    os.system("killAll MavensMate")
    
def get_active_file():
    return sublime.active_window().active_view().file_name()

def is_mm_project():
    import json
    #return sublime.active_window().active_view().settings().get('mm_project_directory') != None #<= bug
    is_mm_project = None
    try:
        project_directory = sublime.active_window().folders()[0]
        json_data = open(project_directory+"/.sublime-project")
        data = json.load(json_data)
        pd = data["settings"]["mm_project_directory"]
        is_mm_project = True
    except:
        is_mm_project = False
    return is_mm_project

def mm_project_directory():
    #return sublime.active_window().active_view().settings().get('mm_project_directory') #<= bug
    return sublime.active_window().folders()[0]

def mm_workspace():
    workspace = ""
    if settings.get('mm_workspace') != None:
        workspace = settings.get('mm_workspace')
    else:
        workspace = sublime.active_window().active_view().settings().get('mm_workspace')
    return workspace

def mark_line_numbers(lines):
    icon = 'dot'
    points = [sublime.active_window().active_view().text_point(l - 1, 0) for l in lines]
    regions = [sublime.Region(p, p) for p in points]
    sublime.active_window().active_view().add_regions('deleted', regions, "operation.fail",
        icon, sublime.HIDDEN | sublime.DRAW_EMPTY)

def clear_marked_line_numbers():
    sublime.active_window().active_view().erase_regions('deleted')

class MarkLinesCommand(sublime_plugin.WindowCommand):
    def run (self):
        #mark_lines(self, None)
        clear_marked_lines()

#refreshes selected directory (or directories)
# if src is refreshed, project is "cleaned"
class RefreshDirectoryCommand(sublime_plugin.WindowCommand):
    def run (self, dirs):
        printer = PanelPrinter.get(self.window.id())
        printer.show()
        printer.write('\nRefreshing from server\n')
        dir_string = ','.join(dirs)
        printer.write(dir_string+'\n')
        temp = tempfile.NamedTemporaryFile(delete=False, prefix="mm")
        try:
            temp.write(dir_string)
        finally:
            temp.close()
        threads = []
        thread = MetadataAPICall("clean_directories", "'"+temp.name+"' '"+mm_project_directory()+"'")
        threads.append(thread)
        thread.start()
        handle_threads(threads, printer, handle_result, 0)  

class ExecuteAnonymousCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("execute_anonymous", mm_project_directory())
        launch_mavens_mate_window(temp_file_name)

#displays edit project dialog
class EditProjectCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("edit_project", mm_project_directory())
        launch_mavens_mate_window(temp_file_name)

#displays new project dialog
class NewProjectCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("new_project", mm_workspace())
        launch_mavens_mate_window(temp_file_name)

#displays deploy dialog
class DeployToServerCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("deploy_to_server", mm_project_directory())
        launch_mavens_mate_window(temp_file_name)

#displays new project dialog
class CheckoutProjectCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("checkout_project", mm_workspace())
        launch_mavens_mate_window(temp_file_name)   

#displays unit test dialog
class RunApexUnitTestsCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("run_apex_tests", mm_project_directory())
        launch_mavens_mate_window(temp_file_name) 

#replaces local copy of metadata with latest server copies
class CleanProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.ok_cancel_dialog("Are you sure you want to clean this project? All local (non-server) files will be deleted and your project will be refreshed from the server", "Clean"):
            printer = PanelPrinter.get(self.window.id())
            printer.show()
            printer.write('\nCleaning Project\n')
            threads = []
            thread = MetadataAPICall("clean_project", "'"+mm_project_directory()+"' '"+mm_workspace()+"'")
            threads.append(thread)
            thread.start()
            handle_threads(threads, printer, handle_result, 0)  

#attempts to compile the entire project
class CompileProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.ok_cancel_dialog("Are you sure you want to compile the entire project?", "Compile Project"):
            printer = PanelPrinter.get(self.window.id())
            printer.show()
            printer.write('\nCompiling Project\n')
            threads = []
            thread = MetadataAPICall("compile_project", "'"+mm_project_directory()+"'")
            threads.append(thread)
            thread.start()
            handle_threads(threads, printer, handle_result, 0)

#deletes selected metadata
class DeleteMetadataCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        if sublime.ok_cancel_dialog("Are you sure you want to delete the selected files from Salesforce?", "Delete"):
            printer = PanelPrinter.get(self.window.id())
            printer.show()
            printer.write('\nDeleting Selected Metadata\n')
            file_string = ','.join(files)
            temp = tempfile.NamedTemporaryFile(delete=False, prefix="mm")
            try:
                temp.write(file_string)
            finally:
                temp.close()
            threads = []
            thread = MetadataAPICall("delete_metadata", "'"+temp.name+"' '"+mm_project_directory()+"'")
            threads.append(thread)
            thread.start()
            handle_threads(threads, printer, handle_result, 0)  

#displays new apex class dialog
class NewApexClassCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        sublime.active_window().show_input_panel("Apex Class Name, Template (base, test, batch, sched, email, empty)", "MyClass, base", self.on_input, None, None)
    
    def on_input(self, input): 
        printer = PanelPrinter.get(self.view.window().id())
        printer.show()
        api_name, class_type = parse_new_metadata_input(input)
        printer.write('\nCreating New Apex Class => ' + api_name + '\n')
        threads = []
        thread = MetadataAPICall("new_metadata", "'{:meta_type=>\"ApexClass\", :api_name=>\""+api_name+"\"}' '"+mm_project_directory()+"'")
        threads.append(thread)
        thread.start()
        handle_threads(threads, printer, handle_result, 0)  

#displays new apex trigger dialog
class NewApexTriggerCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        sublime.active_window().show_input_panel("Apex Trigger Name, SObject Name", "MyAccountTrigger, Account", self.on_input, None, None)
    
    def on_input(self, input): 
        printer = PanelPrinter.get(self.view.window().id())
        printer.show()
        api_name, sobject_name = parse_new_metadata_input(input)
        printer.write('\nCreating New Apex Trigger => ' + api_name + '\n')
        threads = []
        thread = MetadataAPICall("new_metadata", "'{:meta_type=>\"ApexTrigger\", :api_name=>\""+api_name+"\", :object_api_name=>\""+sobject_name+"\"}' '"+mm_project_directory()+"'")
        threads.append(thread)
        thread.start()
        handle_threads(threads, printer, handle_result, 0)  

#displays new apex page dialog
class NewApexPageCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        sublime.active_window().show_input_panel("Visualforce Page Name", "", self.on_input, None, None)
    
    def on_input(self, input): 
        printer = PanelPrinter.get(self.view.window().id())
        printer.show()
        api_name = parse_new_metadata_input(input)
        printer.write('\nCreating New Visualforce Page => ' + api_name + '\n')
        threads = []
        thread = MetadataAPICall("new_metadata", "'{:meta_type=>\"ApexPage\", :api_name=>\""+api_name+"\"}' '"+mm_project_directory()+"'")
        threads.append(thread)
        thread.start()
        handle_threads(threads, printer, handle_result, 0)  

#displays new apex component dialog
class NewApexComponentCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        sublime.active_window().show_input_panel("Visualforce Component Name", "", self.on_input, None, None)
    
    def on_input(self, input): 
        printer = PanelPrinter.get(self.view.window().id())
        printer.show()
        api_name = parse_new_metadata_input(input)
        printer.write('\nCreating New Visualforce Component => ' + api_name + '\n')
        threads = []
        thread = MetadataAPICall("new_metadata", "'{:meta_type=>\"ApexComponent\", :api_name=>\""+api_name+"\"}' '"+mm_project_directory()+"'")
        threads.append(thread)
        thread.start()
        handle_threads(threads, printer, handle_result, 0)  

#deploys the currently active file
class CompileActiveFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        printer = PanelPrinter.get(self.window.id())
        printer.show()
        active_file = get_active_file()
        printer.write('\nCompiling => ' + active_file + '\n')        
        threads = []
        thread = MetadataAPICall("compile_file", "'"+active_file+"'")
        threads.append(thread)
        thread.start()
        handle_threads(threads, printer, handle_result, 0)

#deploys the currently active file
class RefreshActiveFile(sublime_plugin.WindowCommand):
    def run(self):
        printer = PanelPrinter.get(self.window.id())
        printer.show()
        active_file = get_active_file()
        printer.write('\nRefreshing From Server => ' + active_file + '\n')        
        threads = []
        thread = MetadataAPICall("refresh_from_server", "'"+active_file+"'")
        threads.append(thread)
        thread.start()
        handle_threads(threads, printer, handle_result, 0)

#handles compiling to server on save
class RemoteEdit(sublime_plugin.EventListener):
    def on_post_save(self, view):
        active_file = get_active_file()
        fileName, ext = os.path.splitext(active_file)
        valid_file_extensions = ['.page', '.component', '.cls', '.object', '.page', '.trigger', '.tab', '.layout', '.resource', '.remoteSite']
        if settings.get('mm_compile_on_save') == True and is_mm_project() == True and ext in valid_file_extensions:
            printer = PanelPrinter.get(view.window().id())
            printer.show() 
            printer.write('\nCompiling => ' + active_file + '\n')        
            threads = []
            thread = MetadataAPICall("compile_file", "'"+active_file+"'")
            threads.append(thread)
            thread.start()
            handle_threads(threads, printer, handle_result, 0)            

#displays mavensmate panel
class ShowDebugPanelCommand(sublime_plugin.WindowCommand):
    def run(self): 
        if is_mm_project() == True:
            PanelPrinter.get(self.window.id()).show(True)

#hides mavensmate panel
class HideDebugPanelCommand(sublime_plugin.WindowCommand):
    def run(self):
        if is_mm_project() == True:
            PanelPrinter.get(self.window.id()).show(False)

#calls out to the ruby scripts that interact with the metadata api
#pushes them to background threads and reads the piped response
class MetadataAPICall(threading.Thread):
    def __init__(self, command_name, params):
        self.result = None
        self.command_name = command_name
        self.params = params
        threading.Thread.__init__(self)

    def run(self):
        p = subprocess.Popen(ruby+" '"+mm_dir+"/commands/"+self.command_name+".rb' "+self.params+"", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        if p.stdout is not None : 
           msg = p.stdout.readlines()
        msg_string  = '\n'.join(msg)
        msg_string = msg_string.replace(":true", ":True")
        msg_string = msg_string.replace(":false", ":False")
        msg_string = msg_string.replace(":null", "None")
        msg_string = msg_string.replace("namespace\"None", "namespace\":None")
        msg_string = msg_string.replace("\\n", "\\\n")
        msg_string = msg_string.replace("problem\"None", "problem\":None")
        msg_string = msg_string.replace("id\"None", "id\":None")
        print "result is: " + msg_string
        res = None
        try:
            res = ast.literal_eval(msg_string)
        except:
            try:
                res = eval(msg_string)
            except:
                res = msg_string
        self.result = res

#handles spawned threads and prints the "loading indicator" to the mm_panel
def handle_threads(threads, printer, handle_result, i=0):
    compile_result = ""
    next_threads = []
    for thread in threads:
        printer.write('.')
        if thread.is_alive():
            next_threads.append(thread)
            continue
        if thread.result == False:
            continue
        compile_result = thread.result

    threads = next_threads

    if len(threads):
        sublime.set_timeout(lambda: handle_threads(threads, printer, handle_result, i), 600)
        return

    handle_result(printer, compile_result)

#prints the result of the ruby script, can be a string or a dict
def print_result_message(res, printer):
    if isinstance(res, str):
        clear_marked_line_numbers()
        printer.write('\n[OPERATION FAILED]:' + res + '\n')
    elif 'check_deploy_status_response' in res and res['check_deploy_status_response']['result']['success'] == False and 'messages' in res['check_deploy_status_response']['result']:
        #here we're parsing a response from the metadata endpoint
        res = res['check_deploy_status_response']['result']
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
            print failures
        else:
            msg = res['messages']
        if msg != None:
            if 'line_number' in msg:
                line_col = ' (Line: '+msg['line_number']
                mark_line_numbers([int(float(msg['line_number']))])
            if 'column_number' in msg:
                line_col += ', Column: '+msg['column_number']
            if len(line_col) > 0:
                line_col += ')'
            printer.write('\n[DEPLOYMENT FAILED]: ' + msg['file_name'] + ': ' + msg['problem'] + line_col + '\n')
        elif failures != None:
            for f in failures: 
                printer.write('\n[DEPLOYMENT FAILED]: ' + f['name'] + ', ' + f['method_name'] + ': ' + f['message'] + '\n')
    elif 'check_deploy_status_response' in res and res['check_deploy_status_response']['result']['success'] == False and 'messages' not in res['check_deploy_status_response']['result']:
        #here we're parsing a response from the apex endpoint
        res = res['check_deploy_status_response']['result']
        line_col = ""
        if 'line' in res:
            line_col = ' (Line: '+res['line']
            mark_line_numbers([int(float(res['line']))])
        if 'column' in res:
            line_col += ', Column: '+res['column']
        if len(line_col) > 0:
            line_col += ')'
        printer.write('\n[COMPILE FAILED]: ' + res['problem'] + line_col + '\n')
    elif 'check_deploy_status_response' in res and res['check_deploy_status_response']['result']['success'] == True:     
        clear_marked_line_numbers()
        printer.write('\n[Deployed Successfully]' + '\n')
    elif res['success'] == False and 'message' in res:
        clear_marked_line_numbers()
        printer.write('\n[OPERATION FAILED]:' + res['message'] + '\n')
    elif res['success'] == False:
        clear_marked_line_numbers()
        printer.write('\n[OPERATION FAILED]' + '\n')
    else:
        clear_marked_line_numbers()
        printer.write('\n[Operation Completed Successfully]' + '\n')    

#handles the result of the ruby script
def handle_result(printer, result):
    print_result_message(result, printer) 
    if 'check_deploy_status_response' in result: 
        res = result['check_deploy_status_response']['result']
        if res['success'] == True and 'location' in res :
            sublime.active_window().open_file(res['location'])
        if res['success'] == True and hide_panel == True:
            printer.hide()             
    elif 'success' in result:
        if result['success'] == True and hide_panel == True:
            printer.hide() 

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


# future functionality

#TODO: deploys the currently open tabs
# class CompileTabsCommand(sublime_plugin.WindowCommand):
#     def run(self):
#         #printer = PanelPrinter.get(self.window.id())
#         files = get_tab_file_names()
#         files_list = ', '.join(files)
#         print files_list
#         # printer.write('Compiling Active Tabs\n')        
#         # threads = []
#         # thread = MetadataAPICall("compile_file", "'"+active_file+"'")
#         # threads.append(thread)
#         # thread.start()
#         # handle_threads(threads, printer, handle_result, 0)
#         foo = 'bar'

# def get_tab_file_names():
#     from os import path
#     from operator import itemgetter
#     from datetime import datetime
#     tabs = []
#     win = sublime.active_window()
#     for vw in win.views():
#        if vw.file_name() is not None:
#           #_, tail = path.split(vw.file_name())
#           #modified = path.getmtime(vw.file_name())
#           #tabs.append((tail, vw, modified))
#           tabs.append('"'+vw.file_name()+'"')
#        else:
#           pass      # leave new/untitled files (for the moment)
#     return tabs 

# class GetTabsCommand(sublime_plugin.WindowCommand):
#     def run(self):
#         from os import path
#         from operator import itemgetter
#         from datetime import datetime
#         tabs = []
#         win = sublime.active_window()
#         for vw in win.views():
#            if vw.file_name() is not None:
#               _, tail = path.split(vw.file_name())
#               modified = path.getmtime(vw.file_name())
#               #tabs.append((tail, vw, modified))
#               tabs.append((tail, vw.file_name()))
#            else:
#               pass      # leave new/untitled files (for the moment)
#         print tabs

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
            if not isinstance(string, unicode):
                string = unicode(string, 'UTF-8', errors='strict')
            if os.name != 'nt':
                string = unicodedata.normalize('NFC', string)
            self.strings[key].append(string)
        if finish:
            self.strings[key].append(None)
        sublime.set_timeout(self.write_callback, 0)
        return key

    def write_callback(self):
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
