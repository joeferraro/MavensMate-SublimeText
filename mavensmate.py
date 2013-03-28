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
import unicodedata, re
import urllib, urllib2
from xml.dom.minidom import parse, parseString
import json
import apex_reserved 
import command_helper 
import traceback

mm_dir = os.getcwdu()
#PLUGIN_DIRECTORY = os.getcwd().replace(os.path.normpath(os.path.join(os.getcwd(), '..', '..')) + os.path.sep, '').replace(os.path.sep, '/')
#for future reference (windows/linux support)
#sublime.packages_path()
settings = sublime.load_settings('mavensmate.sublime-settings')
hide_panel = settings.get('mm_hide_panel_on_success', 1)
hide_time = settings.get('mm_hide_panel_time', 1)

def check_for_workspace():
    if not os.path.exists(settings.get('mm_workspace')):
        #os.makedirs(settings.get('mm_workspace')) we're not creating the directory here bc there's some sort of weird race condition going on
        msg = 'Your mm_workspace directory does not exist. Please create the directory then try your operation again. Thx!'
        sublime.message_dialog(msg)  
        raise BaseException

def get_ruby():
    ruby = "ruby"    
    if settings.get('mm_ruby') != None: 
        ruby = settings.get('mm_ruby')
    return ruby

ruby = get_ruby()

def start_local_server():
    check_for_workspace()
    cmd = ruby+" -r '"+mm_dir+"/support/lib/local_server_thin.rb' -e 'MavensMate::LocalServerThin.start'"
    result = os.system(cmd)
    if result != 0:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        msg = 'The local MavensMate server has failed to launch: \n\n'
        pout = ''
        if p.stdout is not None : 
            pout = p.stdout.readlines()
        pout = '\n'.join(pout)
        sublime.message_dialog(msg + pout)
        raise BaseException

def stop_local_server():
    cmd = ruby+" -r '"+mm_dir+"/support/lib/local_server_thin.rb' -e 'MavensMate::LocalServerThin.stop'"
    os.system(cmd)

def generate_ui(ruby_script, args):
    p = subprocess.Popen(ruby+" '"+mm_dir+"/commands/"+ruby_script+".rb' "+args+"", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
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

def get_project_name():
    return os.path.basename(sublime.active_window().folders()[0])

def sublime_project_file_path():
    project_directory = sublime.active_window().folders()[0]
    if os.path.isfile(project_directory+"/.sublime-project"):
        return project_directory+"/.sublime-project"
    elif os.path.isfile(project_directory+"/"+get_project_name()+".sublime-project"):
        return project_directory+"/"+get_project_name()+".sublime-project"
    else:
        return None

def is_mm_project():
    #return sublime.active_window().active_view().settings().get('mm_project_directory') != None #<= bug
    is_mm_project = None
    try:
        json_data = open(sublime_project_file_path())
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

def mark_line_numbers(lines, icon="dot"):
    points = [sublime.active_window().active_view().text_point(l - 1, 0) for l in lines]
    regions = [sublime.Region(p, p) for p in points]
    sublime.active_window().active_view().add_regions('deleted', regions, "operation.fail",
        icon, sublime.HIDDEN | sublime.DRAW_EMPTY)

def clear_marked_line_numbers():
    try:
        sublime.active_window().active_view().erase_regions('deleted')
    except:
        print 'no regions to clean up'

class MarkLinesCommand(sublime_plugin.WindowCommand):
    def run (self):
        #mark_lines(self, None)
        clear_marked_lines()

class OpenProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        open_projects = []
        try:
            for w in sublime.windows():
                if len(w.folders()) == 0:
                    continue;
                root = w.folders()[0]
                if mm_workspace() not in root:
                    continue
                project_name = root.split("/")[-1]
                open_projects.append(project_name)
        except:
            print 'ok'

        import os
        self.dir_map = {}
        dirs = []
        for dirname in os.listdir(mm_workspace()):
            if dirname == '.DS_Store' or dirname == '.' or dirname == '..' or dirname == '.logs' : continue
            if dirname in open_projects : continue
            sublime_project_file = dirname+'.sublime-project'
            for project_content in os.listdir(mm_workspace()+"/"+dirname):
                if '.' not in project_content: continue
                if project_content == '.sublime-project':
                    sublime_project_file = '.sublime-project'
                    continue
            dirs.append(dirname)
            self.dir_map[dirname] = [dirname, sublime_project_file]
        self.results = dirs
        self.window.show_quick_panel(dirs, self.panel_done,
            sublime.MONOSPACE_FONT)

    def panel_done(self, picked):
        if 0 > picked < len(self.results):
            return
        self.picked_project = self.results[picked]
        print 'opening project: ' + self.picked_project
        project_file = self.dir_map[self.picked_project][1]
        if os.path.isfile(mm_workspace()+"/"+self.picked_project+"/"+project_file):
            p = subprocess.Popen("'/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl' --project '"+mm_workspace()+"/"+self.picked_project+"/"+project_file+"'", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        else:
            sublime.message_dialog("Cannot find: "+mm_workspace()+"/"+self.picked_project+"/"+project_file)

#launches the org connections UI
class OrgConnectionsCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("deployment_connections", "'"+mm_project_directory()+"'")
        launch_mavens_mate_window(temp_file_name)
        send_usage_statistics('Org Connections')

class UpdateMeCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        from functools import partial
        printer = PanelPrinter.get(sublime.active_window().id())
        printer.show()
        printer.write('\nUpdating MavensMate, please wait...\n')
        import shutil
        tmp_dir = tempfile.gettempdir()
        shutil.copyfile(mm_dir+"/install.rb", tmp_dir+"/install.rb")
        thread = threading.Thread(target=self.updatePackage)
        thread.start()       
        ThreadProgress(thread, 'Updating MavensMate', 'MavensMate has been updated successfully')
    def updatePackage(self):       
        tmp_dir = tempfile.gettempdir()
        os.chdir(tmp_dir)
        time.sleep(3)
        os.system(ruby+" install.rb")    
        #sublime.set_timeout(partial(self.notify), 1)

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

#creates a MavensMate project from an existing directory
class CreateMavensMateProject(sublime_plugin.WindowCommand):
    def run (self, dirs):
        directory = dirs[0]

        if directory.endswith("/src"):
            printer = PanelPrinter.get(self.window.id())
            printer.show()
            printer.write('\n[OPERATION FAILED] You must run this command from the project folder, not the "src" folder\n')
            return            

        dir_entries = os.listdir(directory)
        has_source_directory = False
        for entry in dir_entries:
            if entry == "src":
                has_source_directory = True
                break

        if has_source_directory == False:
            printer = PanelPrinter.get(self.window.id())
            printer.show()
            printer.write('\n[OPERATION FAILED] Unable to locate "src" folder\n')
            return
        
        dir_entries = os.listdir(directory+"/src")
        has_package = False
        for entry in dir_entries:
            if entry == "package.xml":
                has_package = True
                break

        if has_package == False:
            printer = PanelPrinter.get(self.window.id())
            printer.show()
            printer.write('\n[OPERATION FAILED] Unable to locate package.xml in src folder \n')
            return        

        start_local_server()
        temp_file_name = generate_ui("new_project_from_directory", "'"+directory+"' '"+mm_workspace()+"'")
        launch_mavens_mate_window(temp_file_name)

#launches the execute anonymous UI
class ExecuteAnonymousCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("execute_anonymous", "'"+mm_project_directory()+"'")
        launch_mavens_mate_window(temp_file_name)
        send_usage_statistics('Execute Anonymous')

#displays edit project dialog
class EditProjectCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("edit_project", "'"+mm_project_directory()+"'")
        launch_mavens_mate_window(temp_file_name)
        send_usage_statistics('Edit Project')

#displays new project dialog
class NewProjectCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("new_project", "'"+mm_workspace()+"'")
        launch_mavens_mate_window(temp_file_name)
        send_usage_statistics('New Project')

#displays deploy dialog
class DeployToServerCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("deploy_to_server", "'"+mm_project_directory()+"'")
        launch_mavens_mate_window(temp_file_name)
        send_usage_statistics('Deploy to Server')

#displays new project dialog
class CheckoutProjectCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("checkout_project", "'"+mm_workspace()+"'")
        launch_mavens_mate_window(temp_file_name)  
        send_usage_statistics('Checkout Project') 

#displays unit test dialog
class RunApexUnitTestsCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        start_local_server()
        temp_file_name = generate_ui("run_apex_tests", "'"+mm_project_directory()+"'")
        launch_mavens_mate_window(temp_file_name) 
        send_usage_statistics('Apex Unit Testing')

class ShowVersionCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        json_data = open(mm_dir+"/packages.json")
        data = json.load(json_data)
        json_data.close()
        version = data["packages"][0]["platforms"]["osx"][0]["version"]
        sublime.message_dialog("MavensMate v"+version+"\n\nMavensMate is an open source Sublime Text package for Force.com\n\nmavens.io/mm")

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
            send_usage_statistics('Clean Project')  

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
            send_usage_statistics('Compile Project')

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
            send_usage_statistics('Delete Metadata')

#opens the MavensMate shell
class NewShellCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        send_usage_statistics('New Shell Command')
        sublime.active_window().show_input_panel("MavensMate Command", "", self.on_input, None, None)
    
    def on_input(self, input): 
        try:
            ps = input.split(" ")
            if ps[0] == 'new':
                metadata_type, metadata_name, object_name = '', '', ''
                metadata_type   = ps[1]
                proper_type     = command_helper.dict[metadata_type][0]
                metadata_name   = ps[2]
                if len(ps) > 3:
                    object_name = ps[3]
                options = {
                    'metadata_type'     : proper_type,
                    'metadata_name'     : metadata_name,
                    'object_api_name'   : object_name,
                    'apex_class_type'   : 'Base'
                }
                new_metadata(self, options)
            elif ps[0] == 'bundle' or ps[0] == 'b':
                deploy_resource_bundle(ps[1])
            else:
                print_debug_panel_message('Unrecognized command: ' + input + '\n')
        except:
            print_debug_panel_message('Unrecognized command: ' + input + '\n')

def new_metadata(self, opts={}):
    printer = PanelPrinter.get(self.view.window().id())
    printer.show()
    printer.write('\nCreating New '+opts['metadata_type']+' => ' + opts['metadata_name'] + '\n')
    param1 = ''
    if opts['metadata_type'] == 'ApexClass':
        param1 = "{:meta_type=>\""+opts['metadata_type']+"\", :api_name=>\""+opts['metadata_name']+"\", :apex_class_type=>\""+opts['apex_class_type']+"\"}"
    elif opts['metadata_type'] == 'ApexTrigger':
        param1 = "{:meta_type=>\""+opts['metadata_type']+"\", :api_name=>\""+opts['metadata_name']+"\", :object_api_name=>\""+opts['object_api_name']+"\"}"
    else:
        param1 = "{:meta_type=>\""+opts['metadata_type']+"\", :api_name=>\""+opts['metadata_name']+"\"}"
    threads = []
    thread = MetadataAPICall("new_metadata", "'"+param1+"' '"+mm_project_directory()+"'")
    threads.append(thread)
    thread.start()
    handle_threads(threads, printer, handle_result, 0)

#displays new apex class dialog
class NewApexClassCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        send_usage_statistics('New Apex Class')
        sublime.active_window().show_input_panel("Apex Class Name, Template (base, test, batch, sched, email, exception, empty)", "MyClass, base", self.on_input, None, None)
    
    def on_input(self, input): 
        api_name, class_type = parse_new_metadata_input(input)
        options = {
            'metadata_type'     : 'ApexClass',
            'metadata_name'     : api_name,
            'apex_class_type'   : class_type
        }
        new_metadata(self, options)  

#displays new apex trigger dialog
class NewApexTriggerCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        send_usage_statistics('New Apex Trigger')
        sublime.active_window().show_input_panel("Apex Trigger Name, SObject Name", "MyAccountTrigger, Account", self.on_input, None, None)
    
    def on_input(self, input): 
        api_name, sobject_name = parse_new_metadata_input(input)
        options = {
            'metadata_type'     : 'ApexTrigger',
            'metadata_name'     : api_name,
            'object_api_name'   : sobject_name
        }
        new_metadata(self, options)   

#displays new apex page dialog
class NewApexPageCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        send_usage_statistics('New Visualforce Page')
        sublime.active_window().show_input_panel("Visualforce Page Name", "", self.on_input, None, None)
    
    def on_input(self, input): 
        api_name = parse_new_metadata_input(input)
        options = {
            'metadata_type'     : 'ApexPage',
            'metadata_name'     : api_name
        }
        new_metadata(self, options)     

#displays new apex component dialog
class NewApexComponentCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        send_usage_statistics('New Visualforce Component')
        sublime.active_window().show_input_panel("Visualforce Component Name", "", self.on_input, None, None)
    def on_input(self, input): 
        api_name = parse_new_metadata_input(input)
        options = {
            'metadata_type'     : 'ApexComponent',
            'metadata_name'     : api_name
        }
        new_metadata(self, options)   

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

#refreshes the currently active file from the server
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
        handle_threads(threads, printer, handle_refresh_result, 0)

#completions for force.com-specific use cases
class MavensMateCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        settings = sublime.load_settings('mavensmate.sublime-settings')
        if settings.get('mm_autocomplete') == False or is_mm_project() == False:
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if not ch == '.': return []

        word = view.substr(view.word(pt))
        print '------'
        print "trying to find instantiation of: " + word
        fn, ext = os.path.splitext(view.file_name())
        if (ext == '.cls' or ext == '.trigger') and word != None and word != '':
            _completions = []
            lower_prefix = word.lower()
            if os.path.isfile(mm_dir+"/support/lib/apex/"+lower_prefix+".json"): #=> apex static methods
                prefix = prefix.lower()
                json_data = open(mm_dir+"/support/lib/apex/"+lower_prefix+".json")
                data = json.load(json_data)
                json_data.close()
                pd = data["static_methods"]
                for method in pd:
                    _completions.append((method, method))
                return sorted(_completions)
            elif os.path.isfile(mm_project_directory()+"/src/classes/"+word+".cls"): #=> custom apex class static methods
                search_name = prep_for_search(word)
                print search_name
                print 'looking for class def in: ' + mm_project_directory()+"/config/.class_docs/xml/class_"+search_name+".xml"
                if os.path.isfile(mm_project_directory()+"/config/.class_docs/xml/"+search_name+".xml"):
                    object_dom = parse(mm_project_directory()+"/config/.class_docs/xml/"+search_name+".xml")
                    for node in object_dom.getElementsByTagName('memberdef'):
                        #print node.getAttribute("static")
                        if node.getAttribute("static") == "No": continue
                        member_type = ''
                        member_name = ''
                        member_args = ''
                        for child in node.childNodes:                            
                            if child.nodeName != 'name' and child.nodeName != 'type' and child.nodeName != 'argsstring': continue
                            if child.nodeName == 'name':
                                if child.firstChild != None: member_name = child.firstChild.nodeValue
                            elif child.nodeName == 'type':
                                if child.firstChild != None: member_type = child.firstChild.nodeValue
                            elif child.nodeName == 'argsstring':
                                if child.firstChild != None: member_args = child.firstChild.nodeValue   
                            print member_args 
                            if member_name != '' and member_name != 'set' and member_name != 'get':
                                _completions.append((member_name+member_args+" \t"+member_type, member_name + member_args))
                    return sorted(_completions)            
            else: 
                current_line = view.rowcol(pt)
                current_line_index = current_line[0]
                current_object = None
                region_from_top_to_current_word = sublime.Region(0, pt + 1)
                lines = view.lines(region_from_top_to_current_word)
                object_name_lower = ''
                for line in reversed(lines):
                    line_contents = view.substr(line)
                    line_contents = line_contents.replace("\t", "").strip()
                    
                    #print 'examaning line: ' + line_contents

                    if line_contents.find(word) == -1: continue #skip the line if our word isn't in the line
                    if line_contents.strip().startswith('/*') and line_contents.strip().endswith('*/'): continue #skip the line if it's a comment
                    if line_contents.startswith('//'): continue #skip line line if it's a comment
                    if line_contents.startswith(word+"."): continue #skip line if the variable starts it with assignment

                    import re
                    pattern = "'(.* "+word+" .*)'"
                    m = re.search(pattern, line_contents)
                    if m != None: 
                        print 'skipping because word found inside string'
                        continue #skip if we match our word inside of an Apex string

                    pattern = "'("+word+")'"
                    m = re.search(pattern, line_contents)
                    if m != None: 
                        print 'skipping because word found inside exact string'
                        continue #skip if we match our word, in an exact Apex string

                    pattern = re.compile("(system.debug.*\(.*"+word+")", re.IGNORECASE)
                    m = re.search(pattern, line_contents)
                    if m != None: 
                        print 'skipping because word found inside system.debug'
                        continue #skip if we match our word inside system.debug

                    #STILL NEED TO WORK ON THIS
                    #String bat;
                    #foo.bar(foo, bar, bat)
                    #bat. #=> this will be found in the parens above
                    #for (Opportunity o : opps)
                    pattern = re.compile("\(%s\)" % word, re.IGNORECASE)
                    m = re.search(pattern, line_contents)
                    if m != None: 
                        print 'skipping because word found inside parens'
                        continue #skip if we match our word inside parens                

                    #TODO: figure out a way to use word boundaries here to handle
                    #for (Opportunity o: opps) {
                    #
                    #}
                    #word boundary seemingly is only required on the left side
                    # pattern = re.compile("\(%s\)" % word, re.IGNORECASE)
                    # m = re.search(pattern, line_contents)
                    # if m != None: continue #skip if we match our word inside parens TODO?

                    #pattern = "(.*:.*"+word+")"
                    pattern = "(\[.*:.*"+word+".*\])"
                    m = re.search(pattern, line_contents)
                    if m != None:
                        print 'skipping because word found inside query'
                        continue #skip if being bound in a query

                    print "contents of line before strip: " + line_contents

                    object_name = None
                    #object_name = line_contents[0:line_contents.find(word)]
                    try:
                        #object_name = line_contents[0:re.search(r"\b%s\b" % word, line_contents).start()]
                        object_name = line_contents[0:re.search(r"\b%s(\:)?\b" % word, line_contents).start()]
                    except: continue
                    object_name = object_name.strip()

                    print "contents of line after strip: " + object_name

                    pattern = re.compile("^map\s*<", re.IGNORECASE)
                    m = re.search(pattern, line_contents)
                    if m != None:
                        object_name_lower = "map"
                        object_name = "Map"
                        print "our object: " + object_name
                        break

                    pattern = re.compile("^list\s*<", re.IGNORECASE)
                    m = re.search(pattern, line_contents)
                    if m != None:
                        object_name_lower = "list"
                        object_name = "List"
                        print "our object: " + object_name
                        break

                    pattern = re.compile("^set\s*<", re.IGNORECASE)
                    m = re.search(pattern, line_contents)
                    if m != None:
                        object_name_lower = "set"
                        object_name = "Set"
                        print "our object: " + object_name
                        break                        

                    if object_name.endswith(","): continue #=> we're guessing the word is method argument
                    if object_name.endswith("("): continue #=> we're guessing the word is method argument
                    if len(object_name) == 0: continue

                    object_name_lower = object_name.lower()
                    object_name_lower = object_name_lower.strip()
                    object_name_lower = object_name_lower[::-1] #=> reverses line
                    parts = object_name_lower.split(" ")
                    object_name_lower = parts[0]
                    object_name_lower = object_name_lower[::-1] #=> reverses line
                    if "this." in object_name_lower: continue
                    object_name_lower = re.sub(r'\W+', '', object_name_lower) #remove non alphanumeric chars

                    print "our object: " + object_name_lower

                    if object_name_lower in apex_reserved.keywords: continue

                    object_name = object_name.strip()
                    object_name = object_name[::-1] #=> reverses line
                    parts = object_name.split(" ")
                    object_name = parts[0]
                    object_name = object_name[::-1] #=> reverses line
                    object_name = re.sub(r'\W+', '', object_name) #remove non alphanumeric chars
                    print "our object capped: " + object_name

                    if object_name_lower != None and object_name_lower != "": break
                    #need to handle with word is found within a multiline comment
                if os.path.isfile(mm_dir+"/support/lib/apex/"+object_name_lower+".json"): #=> apex instance methods
                    json_data = open(mm_dir+"/support/lib/apex/"+object_name_lower+".json")
                    data = json.load(json_data)
                    json_data.close()
                    pd = data["instance_methods"]
                    for method in pd:
                        _completions.append((method, method))
                    return sorted(_completions)
                elif os.path.isfile(mm_project_directory()+"/config/objects/"+object_name_lower+".object"): #=> object fields
                    object_dom = parse(mm_project_directory()+"/config/objects/"+object_name_lower+".object")
                    for node in object_dom.getElementsByTagName('fields'):
                        field_name = ''
                        field_type = ''
                        for child in node.childNodes:                            
                            if child.nodeName != 'fullName' and child.nodeName != 'type': continue
                            if child.nodeName == 'fullName':
                                field_name = child.firstChild.nodeValue
                            elif child.nodeName == 'type':
                                field_type = child.firstChild.nodeValue
                        _completions.append((field_name+" \t"+field_type, field_name))
                    return sorted(_completions)
                elif os.path.isfile(mm_project_directory()+"/src/objects/"+object_name_lower+".object"): #=> object fields
                    object_dom = parse(mm_project_directory()+"/src/objects/"+object_name_lower+".object")
                    for node in object_dom.getElementsByTagName('fields'):
                        field_name = ''
                        field_type = ''
                        for child in node.childNodes:                            
                            if child.nodeName != 'fullName' and child.nodeName != 'type': continue
                            if child.nodeName == 'fullName':
                                field_name = child.firstChild.nodeValue
                            elif child.nodeName == 'type':
                                field_type = child.firstChild.nodeValue
                        _completions.append((field_name+" \t"+field_type, field_name))
                    return sorted(_completions)
                elif os.path.isfile(mm_project_directory()+"/src/classes/"+object_name_lower+".cls"): #=> apex classes
                    search_name = prep_for_search(object_name)
                    print search_name
                    print 'looking for class def in: ' + mm_project_directory()+"/config/.class_docs/xml/class_"+search_name+".xml"
                    if os.path.isfile(mm_project_directory()+"/config/.class_docs/xml/"+search_name+".xml"):
                        object_dom = parse(mm_project_directory()+"/config/.class_docs/xml/"+search_name+".xml")
                        for node in object_dom.getElementsByTagName('memberdef'):
                            if node.getAttribute("static") == "Yes": continue
                            member_type = ''
                            member_name = ''
                            member_args = ''
                            for child in node.childNodes:                            
                                if child.nodeName != 'name' and child.nodeName != 'type' and child.nodeName != 'argsstring': continue
                                if child.nodeName == 'name':
                                    if child.firstChild != None: member_name = child.firstChild.nodeValue
                                elif child.nodeName == 'type':
                                    if child.firstChild != None: member_type = child.firstChild.nodeValue
                                elif child.nodeName == 'argsstring':
                                    if child.firstChild != None: member_args = child.firstChild.nodeValue   
                                print member_args 
                                if member_name != '' and member_name != 'set' and member_name != 'get':
                                    _completions.append((member_name+member_args+" \t"+member_type, member_name + member_args))
                        return sorted(_completions)

#uses doxygen to generate xml-based documentation which assists in code completion/suggest functionality in MavensMate
class GenerateApexClassDocs(sublime_plugin.WindowCommand):
    def run(self):
        dinput = mm_project_directory() + "/src/classes"
        doutput = mm_project_directory() + "/config/.class_docs"
        if os.path.exists(mm_project_directory() + "/config/.class_docs/xml"):
            import shutil
            shutil.rmtree(mm_project_directory() + "/config/.class_docs/xml")
        if not os.path.exists(mm_project_directory() + "/config/.class_docs"):
            os.makedirs(mm_project_directory() + "/config/.class_docs")

        printer = PanelPrinter.get(self.window.id())  
        printer.show() 
        printer.write('\nIndexing Apex class definitions...\n')
        threads = []
        thread = ExecuteDoxygen(dinput, doutput)
        threads.append(thread)
        thread.start()
        handle_doxygen_threads(threads, printer) 

#handles compiling to server on save
class RemoteEdit(sublime_plugin.EventListener):
    def on_post_save(self, view):
        settings = sublime.load_settings('mavensmate.sublime-settings')
        active_file = get_active_file()
        fileName, ext = os.path.splitext(active_file)
        valid_file_extensions = ['.page', '.component', '.cls', '.object', '.page', '.trigger', '.tab', '.layout', '.resource', '.remoteSite', '.labels', '.app', '.dashboard']
        if settings.get('mm_compile_on_save') == True and is_mm_project() == True and ext in valid_file_extensions:
            printer = PanelPrinter.get(view.window().id())
            printer.show() 
            printer.write('\nCompiling => ' + active_file + '\n')        
            threads = []
            thread = MetadataAPICall("compile_file", "'"+active_file+"'")
            threads.append(thread)
            thread.start()
            handle_threads(threads, printer, handle_result, 0)            

# Future functionality
# class ExecutionOverlayLoader(sublime_plugin.EventListener):
#     def on_load(self, view):
#         print view.file_name()
#         fileName, ext = os.path.splitext(view.file_name())
#         if ext == ".cls" or ext == ".trigger":
#             threads = []
#             thread = MetadataAPICall("get_apex_overlays", "'"+view.file_name()+"'")
#             threads.append(thread)
#             thread.start()
#             generic_handle_threads(threads, write_overlays)            

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

#right click context menu support for resource bundle creation
class NewResourceBundleCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        if sublime.ok_cancel_dialog("Are you sure you want to create resource bundle(s) for the selected static resource(s)", "Create Resource Bundle(s)"):
            create_resource_bundle(self, files) 

#prompts users to select a static resource to create a resource bundle
class CreateResourceBundleCommand(sublime_plugin.WindowCommand):
    def run(self):
        srs = []
        for dirname in os.listdir(mm_project_directory()+"/src/staticresources"):
            if dirname == '.DS_Store' or dirname == '.' or dirname == '..' or '-meta.xml' in dirname : continue
            srs.append(dirname)
        self.results = srs
        self.window.show_quick_panel(srs, self.panel_done,
            sublime.MONOSPACE_FONT)

    def panel_done(self, picked):
        if 0 > picked < len(self.results):
            return
        ps = []
        ps.append(mm_project_directory()+"/src/staticresources/"+self.results[picked])
        create_resource_bundle(self, ps)
        
#deploys selected resource bundle to the server
class DeployResourceBundleCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.rbs_map = {}
        rbs = []
        for dirname in os.listdir(mm_project_directory()+"/resource-bundles"):
            if dirname == '.DS_Store' or dirname == '.' or dirname == '..' : continue
            rbs.append(dirname)
        self.results = rbs
        self.window.show_quick_panel(rbs, self.panel_done,
            sublime.MONOSPACE_FONT)

    def panel_done(self, picked):
        if 0 > picked < len(self.results):
            return
        deploy_resource_bundle(self.results[picked])

def deploy_resource_bundle(bundle_name):
    if '.resource' not in bundle_name:
        bundle_name = bundle_name + '.resource'
    printer = PanelPrinter.get(sublime.active_window().id())
    printer.show()
    printer.write('\nBundling and deploying to server => ' + bundle_name + '\n') 
    # delete existing sr
    if os.path.exists(mm_project_directory()+"/src/staticresources/"+bundle_name):
        os.remove(mm_project_directory()+"/src/staticresources/"+bundle_name)
    # zip bundle to static resource dir 
    os.chdir(mm_project_directory()+"/resource-bundles/"+bundle_name)
    cmd = "zip -r -X '"+mm_project_directory()+"/src/staticresources/"+bundle_name+"' *"      
    os.system(cmd)
    #compile
    file_path = mm_project_directory()+"/src/staticresources/"+bundle_name
    threads = []
    thread = MetadataAPICall("compile_file", "'"+file_path+"'")
    threads.append(thread)
    thread.start()
    handle_threads(threads, printer, handle_result, 0)
    send_usage_statistics('Deploy Resource Bundle')

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
        try:
            res = json.loads(msg_string) 
        except:
            res = msg_string
        self.result = res

#executes doxygen in the background
class ExecuteDoxygen(threading.Thread):
    def __init__(self, dinput, doutput):
        self.result = None
        self.dinput = dinput
        self.doutput = doutput
        threading.Thread.__init__(self)   

    def run(self):
        command = '( cat Doxyfile ; echo "INPUT=\\"'+self.dinput+'\\"" ; echo "EXTENSION_MAPPING=cls=Java" ; echo "OUTPUT_DIRECTORY=\\"'+self.doutput+'\\"" ; echo "OPTIMIZE_OUTPUT_JAVA = YES" ; echo "FILE_PATTERNS += *.cls" ; echo "GENERATE_LATEX = NO" ; echo "GENERATE_HTML = NO" ; echo "GENERATE_XML = YES" ) | ./doxygen -'
        print command
        os.chdir(mm_dir + "/bin")
        os.system(command)

#handles the completion of doxygen execution
def handle_doxygen_threads(threads, printer):
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
        sublime.set_timeout(lambda: handle_doxygen_threads(threads, printer), 200)
        return

    for filename in os.listdir(mm_project_directory() + "/config/.class_docs/xml"):
        print filename
        if filename.startswith('_') or filename.startswith('dir_'): 
            os.remove(mm_project_directory() + "/config/.class_docs/xml/" + filename) 
            continue
        if filename == 'combine.xslt' or filename == 'compound.xsd': 
            os.remove(mm_project_directory() + "/config/.class_docs/xml/" + filename)
            continue
        tempName = filename
        if tempName.startswith('class_'):
            tempName = tempName.replace('class_', '', 1)
        elif tempName.startswith('enum_'):
            tempName = tempName.replace('enum_', '', 1)
        elif tempName.startswith('interface_'):
            tempName = tempName.replace('interface_', '', 1)
        tempName = tempName.replace('_', '')
        os.rename(mm_project_directory() + "/config/.class_docs/xml/" + filename, mm_project_directory() + "/config/.class_docs/xml/" + tempName)

    printer.write('\n[Indexing complete]' + '\n')
    printer.hide() 

# future functionality
# def generic_handle_threads(threads, result_callback):
#     operation_result = ""
#     next_threads = []
#     for thread in threads:
#         if thread.is_alive():
#             next_threads.append(thread)
#             continue
#         if thread.result == False:
#             continue
#         operation_result = thread.result
    
#     threads = next_threads

#     if len(threads):
#         sublime.set_timeout(lambda: generic_handle_threads(threads, result_callback), 600)
#         return

#     result_callback(operation_result)

# def write_overlays(overlay_result):
#     print overlay_result
#     sublime.set_timeout(lambda: mark_line_numbers([int(float('17'))], "dot"), 2000)

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

def print_debug_panel_message(message):
    printer = PanelPrinter.get(sublime.active_window().id())
    printer.show()
    printer.write(message)

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
                mark_line_numbers([int(float(msg['line_number']))], "bookmark")
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
            mark_line_numbers([int(float(res['line']))], "bookmark")
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

def handle_refresh_result(printer, result):
    print_result_message(result, printer) 
    if 'check_deploy_status_response' in result: 
        res = result['check_deploy_status_response']['result']
        if res['success'] == True and 'location' in res :
            sublime.active_window().open_file(res['location'])
        if res['success'] == True and hide_panel == True:
            printer.hide()            
            #refresh_active_view()
    elif 'success' in result:
        if result['success'] == True and hide_panel == True:
            printer.hide() 
            #refresh_active_view()

def refresh_active_view():
    sublime.set_timeout(sublime.active_window().active_view().run_command('revert'), 100)

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

#preps code completion object for search in doxygen documentation
def prep_for_search(name): 
    #s1 = re.sub('(.)([A-Z]+)', r'\1_\2', name).strip()
    #return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    #return re.sub('([A-Z])', r'\1_', name)
    return name.replace('_', '')

def send_usage_statistics(action):
    if settings.get('mm_send_usage_statistics') == True:
        sublime.set_timeout(lambda: UsageReporter(action).start(), 3000)

def check_for_updates():
    if settings.get('mm_check_for_updates') == True:
        sublime.set_timeout(lambda: AutomaticUpgrader().start(), 5000)

# future functionality

#TODO: deploys the currently open tabs
class CompileTabsCommand(sublime_plugin.WindowCommand):
    def run(self):
        printer = PanelPrinter.get(self.window.id())
        printer.show()
        printer.write('\nCompiling tabs\n')

        files = get_tab_file_names()
        files_list = ', '.join(files)
        print files_list
        temp = tempfile.NamedTemporaryFile(delete=False, prefix="mm")
        try:
            temp.write(files_list)
        finally:
            temp.close()
        threads = []
        thread = MetadataAPICall("compile_selected_metadata", "'"+temp.name+"' '"+mm_project_directory()+"'")
        threads.append(thread)
        thread.start()
        handle_threads(threads, printer, handle_result, 0)  
        send_usage_statistics('Compile Tabs')


def get_tab_file_names():
    from os import path
    from operator import itemgetter
    from datetime import datetime
    tabs = []
    win = sublime.active_window()
    for vw in win.views():
       if vw.file_name() is not None:
          #_, tail = path.split(vw.file_name())
          #modified = path.getmtime(vw.file_name())
          #tabs.append((tail, vw, modified))
          #tabs.append('"'+vw.file_name()+'"')
          tabs.append(vw.file_name())
       else:
          pass      # leave new/untitled files (for the moment)
    return tabs 

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

# #visualforce completions
# class VisualforceCompletions(sublime_plugin.EventListener):
#     def on_query_completions(self, view, prefix, locations):
#         # Only trigger within HTML
#         # if not view.match_selector(locations[0],
#         #         "text.html - source"):
#         #     return []
#         # print len(prefix)  
#         # pt = locations[0] - len(prefix) - 1
#         # ch = view.substr(sublime.Region(pt, pt + 1))
#         # if ch != ':':
#         #     return []
#         # print ch
#         # word = view.substr(view.word(pt))
#         # print word
        
#         # return ([
#         #     ("foooooo\tTag", "a href=\"$1\">$2</a>")
#         # ], sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
#         return []

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

    def __init__(self, thread, message, success_message):
        self.thread = thread
        self.message = message
        self.success_message = success_message
        self.addend = 1
        self.size = 8
        sublime.set_timeout(lambda: self.run(0), 100)

    def run(self, i):
        if not self.thread.is_alive():
            if hasattr(self.thread, 'result') and not self.thread.result:
                sublime.status_message('')
                return
            sublime.status_message(self.success_message)
            sublime.message_dialog("MavensMate has been updated successfully!")
            printer = PanelPrinter.get(sublime.active_window().id())
            printer.hide()
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
            traceback.print_exc(file=sys.stdout)
            print 'failed to send usage statistic'

class AutomaticUpgrader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            json_data = open(mm_dir+"/packages.json")
            data = json.load(json_data)
            json_data.close()
            current_version = data["packages"][0]["platforms"]["osx"][0]["version"]
            import urllib
            j = json.load(urllib.urlopen("https://raw.github.com/joeferraro/MavensMate-SublimeText/master/packages.json"))
            latest_version = j["packages"][0]["platforms"]["osx"][0]["version"]
            release_notes = "\n\nRelease Notes: "
            try:
                release_notes += j["packages"][0]["platforms"]["osx"][0]["release_notes"] + "\n\n"
            except:
                release_notes = ""
            current_array = current_version.split(".")
            latest_array = latest_version.split(".")

            needs_update = False
            if current_array[0] < latest_array[0]:
                needs_update = True
            elif current_array[1] < latest_array[1]:
                needs_update = True
            elif current_array[2] < latest_array[2]:
                needs_update = True

            if needs_update == True:
                if sublime.ok_cancel_dialog("A new version of MavensMate ("+latest_version+") is available. "+release_notes+"Would you like to update?", "Update"):
                    sublime.set_timeout(lambda: sublime.run_command("update_me"), 1)
        except:
            print 'skipping MavensMate update check' 

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
  
check_for_updates()
send_usage_statistics('Startup')