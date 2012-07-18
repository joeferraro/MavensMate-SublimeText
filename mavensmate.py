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

mm_dir = os.getcwdu()

def start_local_server():
    cmd = "ruby -r '"+mm_dir+"/support/lib/local_server.rb' -e 'MavensMate::LocalServer.start'"
    os.system(cmd)

def stop_local_server():
    cmd_b = "ruby -r '"+mm_dir+"/support/lib/local_server.rb' -e 'MavensMate::LocalServer.stop'"

def generate_ui(ruby_script, arg0):
    cmd = "ruby '"+mm_dir+"/commands/"+ruby_script+".rb' '"+arg0+"'"
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
    return sublime.active_window().active_view().settings().get('mm_project_directory') != None

def mm_project_directory():
    #return sublime.active_window().active_view().settings().get('mm_project_directory') #<= bug
    return sublime.active_window().folders()[0]

def mm_workspace():
    return sublime.active_window().active_view().settings().get('mm_workspace')

#displays new project dialog
class NewProjectCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("new_project", mm_workspace())
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

#deletes selected metadata
class CleanProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.ok_cancel_dialog("Are you sure you want to clean this project? All local (non-server) files will be deleted and your project will be refreshed from the server", "Clean"):
            self.status_panel = show_mm_panel(self)
            write_to_panel(self.status_panel, 'Cleaning Project\n')
            print "------CLEANING PROJECT------"
            threads = []
            thread = MetadataAPICall("clean_project", "'"+mm_project_directory()+"' '"+mm_workspace()+"'")
            threads.append(thread)
            thread.start()
            handle_threads(threads, self.status_panel, handle_result, 0)  

#deletes selected metadata
class DeleteMetadataCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        if sublime.ok_cancel_dialog("Are you sure you want to delete the selected files from Salesforce?", "Delete"):
            self.status_panel = show_mm_panel(self)
            write_to_panel(self.status_panel, 'Deleting Selected Metadata\n')
            #print files
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
            handle_threads(threads, self.status_panel, handle_result, 0)  

#displays new apex class dialog
class NewApexClassCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        sublime.active_window().show_input_panel("Apex Class Name, Template (base, test, batch, sched, email, empty)", "MyClass, base", self.on_input, None, None)
    
    def on_input(self, input): 
        self.status_panel = show_mm_panel(self)
        api_name, class_type = parse_new_metadata_input(input)
        write_to_panel(self.status_panel, 'Creating New Apex Class => ' + api_name + '\n')
        threads = []
        thread = MetadataAPICall("new_metadata", "'{:meta_type=>\"ApexClass\", :api_name=>\""+api_name+"\"}' '"+mm_project_directory()+"'")
        threads.append(thread)
        thread.start()
        handle_threads(threads, self.status_panel, handle_result, 0)  

#displays new apex trigger dialog
class NewApexTriggerCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        sublime.active_window().show_input_panel("Apex Trigger Name, SObject Name", "MyAccountTrigger, Account", self.on_input, None, None)
    
    def on_input(self, input): 
        self.status_panel = show_mm_panel(self)
        api_name, sobject_name = parse_new_metadata_input(input)
        write_to_panel(self.status_panel, 'Creating New Apex Trigger => ' + api_name + '\n')
        threads = []
        thread = MetadataAPICall("new_metadata", "'{:meta_type=>\"ApexTrigger\", :api_name=>\""+api_name+"\", :object_api_name=>\""+sobject_name+"\"}' '"+mm_project_directory()+"'")
        threads.append(thread)
        thread.start()
        handle_threads(threads, self.status_panel, handle_result, 0)  

#displays new apex page dialog
class NewApexPageCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        sublime.active_window().show_input_panel("Visualforce Page Name", "", self.on_input, None, None)
    
    def on_input(self, input): 
        self.status_panel = show_mm_panel(self)
        api_name = parse_new_metadata_input(input)
        write_to_panel(self.status_panel, 'Creating New Visualforce Page => ' + api_name + '\n')
        threads = []
        thread = MetadataAPICall("new_metadata", "'{:meta_type=>\"ApexPage\", :api_name=>\""+api_name+"\"}' '"+mm_project_directory()+"'")
        threads.append(thread)
        thread.start()
        handle_threads(threads, self.status_panel, handle_result, 0)  

#displays new apex component dialog
class NewApexComponentCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        sublime.active_window().show_input_panel("Visualforce Component Name", "", self.on_input, None, None)
    
    def on_input(self, input): 
        self.status_panel = show_mm_panel(self)
        api_name = parse_new_metadata_input(input)
        write_to_panel(self.status_panel, 'Creating New Visualforce Component => ' + api_name + '\n')
        threads = []
        thread = MetadataAPICall("new_metadata", "'{:meta_type=>\"ApexComponent\", :api_name=>\""+api_name+"\"}' '"+mm_project_directory()+"'")
        threads.append(thread)
        thread.start()
        handle_threads(threads, self.status_panel, handle_result, 0)  

#deploys the currently active file
class CompileActiveFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.status_panel = show_mm_panel(self)
        active_file = get_active_file()
        write_to_panel(self.status_panel, 'Compiling => ' + active_file + '\n')        
        threads = []
        thread = MetadataAPICall("compile_file", "'"+active_file+"'")
        threads.append(thread)
        thread.start()
        handle_threads(threads, self.status_panel, handle_result, 0)

class MetadataAPICall(threading.Thread):
    def __init__(self, command_name, params):
        self.result = None
        self.command_name = command_name
        self.params = params
        threading.Thread.__init__(self)

    def run(self):
        p = subprocess.Popen("ruby '"+mm_dir+"/commands/"+self.command_name+".rb' "+self.params+"", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        if p.stdout is not None : 
           msg = p.stdout.readlines()
        msg_string  = '\n'.join(msg)
        msg_string = msg_string.replace(":true", ":True")
        msg_string = msg_string.replace(":false", ":False")
        print "result is: " + msg_string
        res = ast.literal_eval(msg_string)
        self.result = res

def handle_threads(threads, p, handle_result, i=0):
    compile_result = ""
    next_threads = []
    for thread in threads:
        write_to_panel(p, '>')
        if thread.is_alive():
            next_threads.append(thread)
            continue
        if thread.result == False:
            continue
        compile_result = thread.result

    threads = next_threads

    if len(threads):
        sublime.set_timeout(lambda: handle_threads(threads, p, handle_result, i), 600)
        return

    handle_result(p, compile_result)

def show_mm_panel(el):
    panel_name = 'MavensMate-OutputPanel'
    custom_syntax = 'Packages/MavensMate/MavensMate.tmLanguage'    
    if not hasattr(el, 'panel'):
        el.panel = sublime.active_window().get_output_panel(panel_name)
    el.panel.set_syntax_file(custom_syntax)
    sublime.active_window().run_command("show_panel", {"panel": "output." + panel_name})
    el.panel.set_viewport_position((0,el.panel.size()))
    return el.panel

def write_to_panel(panel, message):
    edit = panel.begin_edit() 
    panel.insert(edit, panel.size(), message)
    panel.end_edit(edit)
    panel.set_viewport_position((0,panel.size()))

def print_result_message(res, panel):
    if 'check_deploy_status_response' in res and res['check_deploy_status_response']['result']['success'] == False:
        res = res['check_deploy_status_response']['result']
        line_col = ""
        msg = []
        if type( res['messages'] ) == list:
            msg = res['messages'][0]
        else:
            msg = res['messages']
        if 'line_number' in msg:
            line_col = ' (Line: '+msg['line_number']
        if 'column_number' in msg:
            line_col += ', Column: '+msg['column_number']
        if len(line_col) > 0:
            line_col += ')'
        write_to_panel(panel, '\n[DEPLOYMENT FAILED]: ' + msg['problem'] + line_col + '\n')
    elif 'check_deploy_status_response' in res and res['check_deploy_status_response']['result']['success'] == True:     
        write_to_panel(panel, '\n[Deployed Successfully]' + '\n')
    elif res['success'] == False and 'message' in res:
        write_to_panel(panel, '\n[OPERATION FAILED]:' + res['message'] + '\n')
    elif res['success'] == False:
        write_to_panel(panel, '\n[OPERATION FAILED]' + '\n')
    else:
        write_to_panel(panel, '\n[Operation Completed Successfully]' + '\n')    

def handle_result(panel, result):
    print_result_message(result, panel) 
    if 'check_deploy_status_response' in result: 
        res = result['check_deploy_status_response']['result']
        if res['success'] == True and 'location' in res :
            sublime.active_window().open_file(res['location'])

def parse_new_metadata_input(input):
    input = input.replace(" ", "")
    if "," in input:
        params = input.split(",")
        api_name = params[0]
        class_type_or_sobject_name = params[1]
        return api_name, class_type_or_sobject_name
    else:
        return input




