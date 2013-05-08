# Written by Joe Ferraro (@joeferraro / www.joe-ferraro.com)
import sublime
import sublime_plugin
import os
import sys
import subprocess
import tempfile  
#import ast
import copy
import threading
if os.name != 'nt':
    import unicodedata
import unicodedata, re
from xml.dom.minidom import parse, parseString
try:
    import util
    from util import PanelPrinter
    from util import ThreadProgress
    import apex_reserved 
    import command_helper 
except:
    import MavensMate.util as util
    import MavensMate.apex_reserved as apex_reserved
    import MavensMate.command_helper as command_helper
    from MavensMate.util import PanelPrinter
    from MavensMate.util import ThreadProgress
import json

try:
    mm_dir = os.getcwdu()
except:
    mm_dir = os.path.dirname(__file__)

settings = sublime.load_settings('mavensmate.sublime-settings')
sublime_version = int(float(sublime.version()))

####### <--START--> COMMANDS THAT USE THE MAVENSMATE UI ##########

#displays new project dialog
class NewProjectCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        util.mm_call('new_project', False)
        util.send_usage_statistics('New Project')

#displays edit project dialog
class EditProjectCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        util.mm_call('edit_project', False)
        util.send_usage_statistics('Edit Project')

    def is_enabled(command):
        return util.is_mm_project()

#displays unit test dialog
class RunApexUnitTestsCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        active_file = util.get_active_file()
        if os.path.exists(active_file):
            filename, ext = os.path.splitext(os.path.basename(util.get_active_file()))
            params = {
                "selected"         : [filename]
            }
        else:
            params = {}
        util.mm_call('unit_test', context=command, params=params)
        util.send_usage_statistics('Apex Unit Testing')

    def is_enabled(command):
        return util.is_mm_project()

#launches the execute anonymous UI
class ExecuteAnonymousCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        util.mm_call('execute_apex', False)
        util.send_usage_statistics('Execute Anonymous')

    def is_enabled(command):
        return util.is_mm_project()

#displays deploy dialog
class DeployToServerCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        #TODO check for org connections before allowing deploy ui to open
        util.mm_call('deploy', False)
        util.send_usage_statistics('Deploy to Server')

    def is_enabled(command):
        return util.is_mm_project()

####### <--END--> COMMANDS THAT USE THE MAVENSMATE UI ##########

class MavensStubCommand(sublime_plugin.WindowCommand):
    def run(self):
        return True
    def is_enabled(self):
        return False
    def is_visible(self):
        return not util.is_mm_project();

#deploys the currently active file
class CompileActiveFileCommand(sublime_plugin.WindowCommand):
    def run(self):       
        params = {
            "files" : [util.get_active_file()]
        }
        util.mm_call('compile', context=self, params=params)

    def is_enabled(command):
        return util.is_mm_file()

    def is_visible(command):
        return util.is_mm_project()

#handles compiling to server on save
class RemoteEdit(sublime_plugin.EventListener):
    def on_post_save(self, view):
        settings = sublime.load_settings('mavensmate.sublime-settings')
        if settings.get('mm_compile_on_save') == True and util.is_mm_file() == True:
            params = {
                "files" : [util.get_active_file()]
            }
            util.mm_call('compile', context=view, params=params)

class MenuModifier(sublime_plugin.EventListener):
    def on_activated_async(self, view):
        view.file_name()

#compiles the selected files
class CompileSelectedFilesCommand(sublime_plugin.WindowCommand):
    def run (self, files):
        #print files
        params = {
            "files"         : files
        }
        util.mm_call('compile', context=self, params=params)
        util.send_usage_statistics('Compile Selected Files')

    def is_visible(self, files):
        return util.is_mm_project()

    def is_enabled(self, files):
        if files != None and type(files) is list and len(files) > 0:
            for f in files:
                if util.is_mm_file(f):
                    return True
        return False

#deploys the currently open tabs
class CompileTabsCommand(sublime_plugin.WindowCommand):
    def run (self):
        params = {
            "files"         : util.get_tab_file_names()
        }
        util.mm_call('compile', context=self, params=params)
        util.send_usage_statistics('Compile Tabs')

#replaces local copy of metadata with latest server copies
class CleanProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.ok_cancel_dialog("Are you sure you want to clean this project? All local (non-server) files will be deleted and your project will be refreshed from the server", "Clean"):
            util.mm_call('clean_project', context=self)
            util.send_usage_statistics('Clean Project')

    def is_enabled(command):
        return util.is_mm_project()  

#opens a project in the current workspace
class OpenProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        open_projects = []
        try:
            for w in sublime.windows():
                if len(w.folders()) == 0:
                    continue;
                root = w.folders()[0]
                if util.mm_workspace() not in root:
                    continue
                project_name = root.split("/")[-1]
                open_projects.append(project_name)
        except:
            pass

        import os
        self.dir_map = {}
        dirs = [] 
        print(util.mm_workspace())
        for dirname in os.listdir(util.mm_workspace()):
            if dirname == '.DS_Store' or dirname == '.' or dirname == '..' or dirname == '.logs' : continue
            if dirname in open_projects : continue
            if not os.path.isdir(util.mm_workspace()+"/"+dirname) : continue
            sublime_project_file = dirname+'.sublime-project'
            for project_content in os.listdir(util.mm_workspace()+"/"+dirname):
                if '.' not in project_content: continue
                if project_content == '.sublime-project':
                    sublime_project_file = '.sublime-project'
                    continue
            dirs.append(dirname)
            self.dir_map[dirname] = [dirname, sublime_project_file]
        self.results = dirs
        print(self.results)
        self.window.show_quick_panel(dirs, self.panel_done,
            sublime.MONOSPACE_FONT)

    def panel_done(self, picked):
        if 0 > picked < len(self.results):
            return
        self.picked_project = self.results[picked]
        print('opening project: ' + self.picked_project)
        project_file = self.dir_map[self.picked_project][1]
        if os.path.isfile(util.mm_workspace()+"/"+self.picked_project+"/"+project_file):
            if sublime_version >= 3000:
                p = subprocess.Popen("'/Applications/Sublime Text 3.app/Contents/SharedSupport/bin/subl' --project '"+util.mm_workspace()+"/"+self.picked_project+"/"+project_file+"'", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            else:
                p = subprocess.Popen("'/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl' --project '"+util.mm_workspace()+"/"+self.picked_project+"/"+project_file+"'", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        else:
            sublime.message_dialog("Cannot find: "+util.mm_workspace()+"/"+self.picked_project+"/"+project_file)

#displays new apex class dialog
class NewApexClassCommand(sublime_plugin.TextCommand):
    def run(self, edit, api_name="MyClass", class_type="default"): 
        templates = get_merged_apex_templates("ApexClass")
        sublime.active_window().show_input_panel("Apex Class Name, Template "+str(sorted(templates.keys())), api_name+", "+class_type, self.on_input, None, None)
        util.send_usage_statistics('New Apex Class')

    def on_input(self, input): 
        api_name, class_type = [x.strip() for x in input.split(',')]
        if not check_apex_templates(get_merged_apex_templates("ApexClass"), { "api_name":api_name, "class_type":class_type }, "new_apex_class"):
            return
        options = {
            'metadata_type'     : 'ApexClass',
            'metadata_name'     : api_name,
            'apex_class_type'   : class_type
        }
        util.mm_call('new_metadata', params=options) 

    def is_enabled(self):
        return util.is_mm_project()

#displays new apex trigger dialog
class NewApexTriggerCommand(sublime_plugin.TextCommand):
    def run(self, edit, api_name="MyAccountTrigger", sobject_name="Account", class_type="default"): 
        templates = get_merged_apex_templates("ApexTrigger")
        sublime.active_window().show_input_panel("Apex Trigger Name, SObject Name, Template "+str(sorted(templates.keys())), api_name+", "+sobject+", "+template, self.on_input, None, None)
        util.send_usage_statistics('New Apex Trigger')

    def on_input(self, input):
        api_name, sobject_name, class_type = [x.strip() for x in input.split(',')]
        if not check_apex_templates(get_merged_apex_templates("ApexTrigger"), { "api_name":api_name, "sobject_name":sobject_name, "class_type":class_type }, "new_apex_trigger"):
            return
        options = {
            'metadata_type'     : 'ApexTrigger',
            'metadata_name'     : api_name,
            'object_api_name'   : sobject_name,
            'apex_class_type'   : class_type
        }
        util.mm_call('new_metadata', params=options) 

    def is_enabled(command):
        return util.is_mm_project()

#displays new apex page dialog
class NewApexPageCommand(sublime_plugin.TextCommand):
    def run(self, edit, api_name="ApexPage", class_type="default"): 
        templates = get_merged_apex_templates("ApexPage")
        sublime.active_window().show_input_panel("Visualforce Page Name, Template", api_name+", "+class_type, self.on_input, None, None)
        util.send_usage_statistics('New Visualforce Page')
    
    def on_input(self, input): 
        api_name, class_type = [x.strip() for x in input.split(',')]
        if not check_apex_templates(get_merged_apex_templates("ApexPage"), { "api_name":api_name, "class_type":class_type }, "new_apex_page"):
            return
        options = {
            'metadata_type'     : 'ApexPage',
            'metadata_name'     : api_name,
            'apex_class_type'   : class_type
        }
        util.mm_call('new_metadata', params=options) 

    def is_enabled(command):
        return util.is_mm_project()

#displays new apex component dialog
class NewApexComponentCommand(sublime_plugin.TextCommand):
    def run(self, edit, api_name="ApexComponent", class_type="default"): 
        templates = get_merged_apex_templates("ApexComponent")
        sublime.active_window().show_input_panel("Visualforce Component Name, Template", api_name+", "+class_type, self.on_input, None, None)
        util.send_usage_statistics('New Visualforce Component')
    
    def on_input(self, input): 
        api_name, class_type = [x.strip() for x in input.split(',')]
        if not check_apex_templates(get_merged_apex_templates("ApexComponent"), { "api_name":api_name, "class_type":class_type }, "new_apex_component"):
            return
        options = {
            'metadata_type'     : 'ApexComponent',
            'metadata_name'     : api_name,
            'apex_class_type'   : class_type
        }
        util.mm_call('new_metadata', params=options) 

    def is_enabled(command):
        return util.is_mm_project()

def check_apex_templates(templates, args, command):
    if "class_type" not in args or args["class_type"] not in templates:
        sublime.error_message(str(args["class_type"])+" is not a valid template, please choose one of: "+str(sorted(templates.keys())))
        sublime.active_window().run_command(command, args)
        return False
    return True

def get_merged_apex_templates(apex_type):
    settings = sublime.load_settings('mavensmate.sublime-settings')
    template_map = settings.get('mm_default_apex_templates_map', {})
    custom_templates = settings.get('mm_apex_templates_map', {})
    if apex_type not in template_map:
        return {}
    if apex_type in custom_templates:
        template_map[apex_type] = dict(template_map[apex_type], **custom_templates[apex_type])
    return template_map[apex_type]

#displays mavensmate panel
class ShowDebugPanelCommand(sublime_plugin.WindowCommand):
    def run(self): 
        if util.is_mm_project() == True:
            PanelPrinter.get(self.window.id()).show(True)

#hides mavensmate panel
class HideDebugPanelCommand(sublime_plugin.WindowCommand):
    def run(self):
        if util.is_mm_project() == True:
            PanelPrinter.get(self.window.id()).show(False)

#shows mavensmate info modal
class ShowVersionCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        version = util.get_version_number()
        sublime.message_dialog("MavensMate for Sublime Text v"+version+"\n\nMavensMate for Sublime Text is an open source Sublime Text package for Force.com development.\n\nhttp://mavens.io/mm")

#refreshes selected directory (or directories)
# if src is refreshed, project is "cleaned"
class RefreshFromServerCommand(sublime_plugin.WindowCommand):
    def run (self, dirs, files):
        if sublime.ok_cancel_dialog("Are you sure you want to overwrite the selected files' contents from Salesforce?", "Refresh"):
            if dirs != None and type(dirs) is list and len(dirs) > 0:
                params = {
                    "directories"   : dirs
                }
            elif files != None and type(files) is list and len(files) > 0:
                params = {
                    "files"         : files
                }
            util.mm_call('refresh', context=self, params=params)
            util.send_usage_statistics('Refresh Selected From Server')

    def is_visible(self, dirs, files):
        return util.is_mm_project()

    def is_enabled(self, dirs, files):
        if dirs != None and type(dirs) is list and len(dirs) > 0:
            for d in dirs:
                if util.is_mm_dir(d):
                    return True
        if files != None and type(files) is list and len(files) > 0:
            for f in files:
                if util.is_mm_file(f):
                    return True
        return False

#refreshes the currently active file from the server
class RefreshActiveFile(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.ok_cancel_dialog("Are you sure you want to overwrite this file's contents from Salesforce?", "Refresh"):
            params = {
                "files"         : [util.get_active_file()]
            }
            util.mm_call('refresh', context=self, params=params)
            util.send_usage_statistics('Refresh Active File From Server')

    def is_visible(self):
        return util.is_mm_file()

#opens the apex class, trigger, component or page on the server
class RunActiveApexTestsCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename, ext = os.path.splitext(os.path.basename(util.get_active_file()))
        params = {
            "selected"         : [filename]
        }
        util.mm_call('unit_test', context=self, params=params)
        util.send_usage_statistics('Run Apex Tests in Active File')

    def is_visible(self):
        return util.is_apex_class_file()

    def is_enabled(self):
        return util.is_apex_test_file()


#opens the apex class, trigger, component or page on the server
class RunSelectedApexTestsCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        if files != None and type(files) is list and len(files) > 0:
            params = {
                "selected"         : []
            }
            for f in files:
                filename, ext = os.path.splitext(os.path.basename(f))
                params['selected'].append(filename)

            util.mm_call('unit_test', context=self, params=params)
            util.send_usage_statistics('Run Apex Tests in Active File')

    def is_visible(self, files):
        if files != None and type(files) is list and len(files) > 0:
            for f in files:
                if util.is_apex_class_file(f): 
                    return True
        return False
        
    def is_enabled(self, files):
        if files != None and type(files) is list and len(files) > 0:
            for f in files:
                if util.is_apex_test_file(f): return True
        return False

#opens the apex class, trigger, component or page on the server
class OpenActiveSfdcUrlCommand(sublime_plugin.WindowCommand):
    def run(self):
        params = {
            "files"         : [util.get_active_file()]
        }
        util.mm_call('open_sfdc_url', context=self, params=params)
        util.send_usage_statistics('Open Active File On Server')

    def is_visible(self):
        return util.is_mm_file()

    def is_enabled(self):
        return util.is_browsable_file()

#opens the WSDL file for apex webservice classes
class OpenActiveSfdcWsdlUrlCommand(sublime_plugin.WindowCommand):
    def run(self):
        params = {
            "files"         : [util.get_active_file()],
            "type"          : "wsdl"
        }
        util.mm_call('open_sfdc_url', context=self, params=params)
        util.send_usage_statistics('Open Active WSDL File On Server')

    def is_visible(self):
        return util.is_apex_class_file()

    def is_enabled(self):
        if util.is_apex_webservice_file(): 
            return True
        return False

#opens the apex class, trigger, component or page on the server
class OpenSelectedSfdcUrlCommand(sublime_plugin.WindowCommand):
    def run (self, files):
        if files != None and type(files) is list and len(files) > 0:
            params = {
                "files"         : files
            }
        util.mm_call('open_sfdc_url', context=self, params=params)
        util.send_usage_statistics('Open Selected File On Server')

    def is_visible(self, files):
        if not util.is_mm_project: return False
        if files != None and type(files) is list and len(files) > 0:
            for f in files:
                if util.is_browsable_file(f): return True
        return False

#opens the WSDL file for apex webservice classes
class OpenSelectedSfdcWsdlUrlCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        if files != None and type(files) is list and len(files) > 0:
            params = {
                "files"         : files,
                "type"          : "wsdl"
            }
        util.mm_call('open_sfdc_url', context=self, params=params)
        util.send_usage_statistics('Open Selected WSDL File On Server')

    def is_visible(self, files):
        if files != None and type(files) is list and len(files) > 0:
            for f in files:
                if util.is_apex_class_file(f): 
                    return True
        return False
        
    def is_enabled(self, files):
        if files != None and type(files) is list and len(files) > 0:
            for f in files:
                if util.is_apex_webservice_file(f): 
                    return True
        return False

#deletes selected metadata
class DeleteMetadataCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        if sublime.ok_cancel_dialog("Are you sure you want to delete the selected files from Salesforce?", "Delete"):
            params = {
                "files" : files
            }
            util.mm_call('delete', context=self, params=params)
            util.send_usage_statistics('Delete Metadata')

    def is_visible(self):
        return util.is_mm_file()

    def is_enabled(self):
        return util.is_mm_file()

#deletes selected metadata
class DeleteActiveMetadataCommand(sublime_plugin.WindowCommand):
    def run(self):
        active_path = util.get_active_file()
        active_file = os.path.basename(active_path)
        if sublime.ok_cancel_dialog("Are you sure you want to delete "+active_file+" file from Salesforce?", "Delete"):
            params = {
                "files" : [active_file]
            }
            result = util.mm_call('delete', context=self, params=params)
            self.window.run_command("close")
            util.send_usage_statistics('Delete Metadata')

    def is_enabled(self):
        return util.is_mm_file()

    def is_visible(self):
        return util.is_mm_project()

#attempts to compile the entire project
class CompileProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.ok_cancel_dialog("Are you sure you want to compile the entire project?", "Compile Project"):
            util.mm_call('compile_project', context=self)
            util.send_usage_statistics('Compile Project')

    def is_enabled(command):
        return util.is_mm_project()

#refreshes the currently active file from the server
class IndexApexOverlaysCommand(sublime_plugin.WindowCommand):
    def run(self):
        util.mm_call('index_apex_overlays', False, context=self)
        util.send_usage_statistics('Index Apex Overlays')  

    def is_enabled(command):
        return util.is_mm_project()

#indexes the meta data based on packages.xml
class IndexMetadataCommand(sublime_plugin.WindowCommand):
    def run(self):
        util.mm_call('index_metadata', True, context=self)
        util.send_usage_statistics('Index Metadata')  

    def is_enabled(command):
        return util.is_mm_project()

#refreshes the currently active file from the server
class FetchLogsCommand(sublime_plugin.WindowCommand):
    def run(self):
        util.mm_call('fetch_logs', False)
        util.send_usage_statistics('Fetch Apex Logs')  

#when a class or trigger file is opened, adds execution overlay markers if applicable
class ExecutionOverlayLoader(sublime_plugin.EventListener):
    def on_load(self, view):
        print('attempting to load apex overlays for current file')
        try:
            fileName, ext = os.path.splitext(view.file_name())
            if ext == ".cls" or ext == ".trigger":
                api_name = fileName.split("/")[-1] 
                overlays = util.parse_json_from_file(util.mm_project_directory()+"/config/.overlays")
                lines = []
                for o in overlays:
                    if o['API_Name'] == api_name:
                        lines.append(int(o["Line"]))
                sublime.set_timeout(lambda: util.mark_overlays(lines), 100)
        except Exception as e:
            print('execution overlay loader error')

#deletes overlays
class DeleteOverlaysCommand(sublime_plugin.WindowCommand):
    def run(self):
        options = [['Delete All In This File', '*']]
        fileName, ext = os.path.splitext(util.get_active_file())
        if ext == ".cls" or ext == ".trigger":
            self.api_name = fileName.split("/")[-1] 
            overlays = util.get_execution_overlays(util.get_active_file())
            for o in overlays:
                options.append(['Line '+str(o["Line"]), str(o["Id"])])
        self.results = options
        self.window.show_quick_panel(options, self.panel_done, sublime.MONOSPACE_FONT)

    def panel_done(self, picked):
        if 0 > picked < len(self.results):
            return
        self.overlay = self.results[picked]
        params = {
            "id" : self.overlay[1]
        }
        util.mm_call('delete_apex_overlay', context=self, params=params)
        util.send_usage_statistics('New Apex Overlay') 

#creates a new overlay
class NewOverlayCommand(sublime_plugin.WindowCommand):
    def run(self):
        fileName, ext = os.path.splitext(util.get_active_file())
        if ext == ".cls" or ext == ".trigger":
            if ext == '.cls':
                self.object_type = 'ApexClass'
            else: 
                self.object_type = 'ApexTrigger'
            self.api_name = fileName.split("/")[-1] 
            number_of_lines = util.get_number_of_lines_in_file(util.get_active_file())
            lines = list(xrange(number_of_lines))
            options = []
            lines.pop(0)
            for l in lines:
                options.append(str(l))
            self.results = options
            self.window.show_quick_panel(options, self.panel_done, sublime.MONOSPACE_FONT)

    def panel_done(self, picked):
        if 0 > picked < len(self.results):
            return
        self.line_number = self.results[picked]
        #print self.line_number
        params = {
            "ActionScriptType"      : "None",
            "Object_Type"           : self.object_type,
            "API_Name"              : self.api_name,
            "IsDumpingHeap"         : True,
            "Iteration"             : 1,
            "Line"                  : int(self.line_number)
        }
        #util.mark_overlay(self.line_number) #cant do this here bc it removes the rest of them
        util.mm_call('new_apex_overlay', context=self, params=params)
        util.send_usage_statistics('New Apex Overlay')  

#right click context menu support for resource bundle creation
class NewResourceBundleCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        if sublime.ok_cancel_dialog("Are you sure you want to create resource bundle(s) for the selected static resource(s)", "Create Resource Bundle(s)"):
            util.create_resource_bundle(self, files) 
            util.send_usage_statistics('New Resource Bundle (Sidebar)')
    def is_visible(self):
        return util.is_mm_project()

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

        params = {
            "directory" : directory
        }
        util.mm_call('new_project_from_existing_directory', params=params)
        util.send_usage_statistics('New Project From Existing Directory')  

    def is_visible(self):
        return not util.is_mm_project()

#generic handler for writing text to an output panel (sublime text 3 requirement)
class MavensMateOutputText(sublime_plugin.TextCommand):
    def run(self, edit, text, *args, **kwargs):
        size = self.view.size()
        self.view.set_read_only(False)
        self.view.insert(edit, size, text)
        self.view.set_read_only(True)
        self.view.show(size)

    def is_visible(self):
        return False

    def is_enabled(self):
        return True

    def description(self):
        return

####### <--START--> COMMANDS THAT ARE NOT *OFFICIALLY* SUPPORTED IN 2.0 BETA ##########

#updates MavensMate plugin
class UpdateMeCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.message_dialog("Use the \"Plugins\" option in MavensMate.app to update MavensMate for Sublime Text.")

#opens the MavensMate shell
class NewShellCommand(sublime_plugin.TextCommand):
    def run(self, edit): 
        util.send_usage_statistics('New Shell Command')
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
                util.mm_call('new_metadata', params=options)
            elif ps[0] == 'bundle' or ps[0] == 'b':
                deploy_resource_bundle(ps[1])
            else:
                util.print_debug_panel_message('Unrecognized command: ' + input + '\n')
        except:
            util.print_debug_panel_message('Unrecognized command: ' + input + '\n')

#completions for force.com-specific use cases
class MavensMateCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        settings = sublime.load_settings('mavensmate.sublime-settings')
        if settings.get('mm_autocomplete') == False or util.is_mm_project() == False:
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if not ch == '.': return []

        word = view.substr(view.word(pt))
        #print '------'
        #print "trying to find instantiation of: " + word
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
            elif os.path.isfile(util.mm_project_directory()+"/src/classes/"+word+".cls"): #=> custom apex class static methods
                search_name = util.prep_for_search(word)
                #print search_name
                #print 'looking for class def in: ' + util.mm_project_directory()+"/config/.class_docs/xml/class_"+search_name+".xml"
                if os.path.isfile(util.mm_project_directory()+"/config/.class_docs/xml/"+search_name+".xml"):
                    object_dom = parse(util.mm_project_directory()+"/config/.class_docs/xml/"+search_name+".xml")
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
                            #print member_args 
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
                        #print 'skipping because word found inside string'
                        continue #skip if we match our word inside of an Apex string

                    pattern = "'("+word+")'"
                    m = re.search(pattern, line_contents)
                    if m != None: 
                        #print 'skipping because word found inside exact string'
                        continue #skip if we match our word, in an exact Apex string

                    pattern = re.compile("(system.debug.*\(.*"+word+")", re.IGNORECASE)
                    m = re.search(pattern, line_contents)
                    if m != None: 
                        #print 'skipping because word found inside system.debug'
                        continue #skip if we match our word inside system.debug

                    #STILL NEED TO WORK ON THIS
                    #String bat;
                    #foo.bar(foo, bar, bat)
                    #bat. #=> this will be found in the parens above
                    #for (Opportunity o : opps)
                    pattern = re.compile("\(%s\)" % word, re.IGNORECASE)
                    m = re.search(pattern, line_contents)
                    if m != None: 
                        #print 'skipping because word found inside parens'
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
                        #print 'skipping because word found inside query'
                        continue #skip if being bound in a query

                    #print "contents of line before strip: " + line_contents

                    object_name = None
                    #object_name = line_contents[0:line_contents.find(word)]
                    try:
                        #object_name = line_contents[0:re.search(r"\b%s\b" % word, line_contents).start()]
                        object_name = line_contents[0:re.search(r"\b%s(\:)?\b" % word, line_contents).start()]
                    except: continue
                    object_name = object_name.strip()

                    #print "contents of line after strip: " + object_name

                    pattern = re.compile("^map\s*<", re.IGNORECASE)
                    m = re.search(pattern, line_contents)
                    if m != None:
                        object_name_lower = "map"
                        object_name = "Map"
                        #print "our object: " + object_name
                        break

                    pattern = re.compile("^list\s*<", re.IGNORECASE)
                    m = re.search(pattern, line_contents)
                    if m != None:
                        object_name_lower = "list"
                        object_name = "List"
                        #print "our object: " + object_name
                        break

                    pattern = re.compile("^set\s*<", re.IGNORECASE)
                    m = re.search(pattern, line_contents)
                    if m != None:
                        object_name_lower = "set"
                        object_name = "Set"
                        #print "our object: " + object_name
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

                    #print "our object: " + object_name_lower

                    if object_name_lower in apex_reserved.keywords: continue

                    object_name = object_name.strip()
                    object_name = object_name[::-1] #=> reverses line
                    parts = object_name.split(" ")
                    object_name = parts[0]
                    object_name = object_name[::-1] #=> reverses line
                    object_name = re.sub(r'\W+', '', object_name) #remove non alphanumeric chars
                    #print "our object capped: " + object_name

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
                elif os.path.isfile(util.mm_project_directory()+"/config/objects/"+object_name_lower+".object"): #=> object fields
                    object_dom = parse(util.mm_project_directory()+"/config/objects/"+object_name_lower+".object")
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
                elif os.path.isfile(util.mm_project_directory()+"/src/objects/"+object_name_lower+".object"): #=> object fields
                    object_dom = parse(util.mm_project_directory()+"/src/objects/"+object_name_lower+".object")
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
                elif os.path.isfile(util.mm_project_directory()+"/src/classes/"+object_name_lower+".cls"): #=> apex classes
                    search_name = util.prep_for_search(object_name)
                    #print search_name
                    #print 'looking for class def in: ' + util.mm_project_directory()+"/config/.class_docs/xml/class_"+search_name+".xml"
                    if os.path.isfile(util.mm_project_directory()+"/config/.class_docs/xml/"+search_name+".xml"):
                        object_dom = parse(util.mm_project_directory()+"/config/.class_docs/xml/"+search_name+".xml")
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
                                #print member_args 
                                if member_name != '' and member_name != 'set' and member_name != 'get':
                                    _completions.append((member_name+member_args+" \t"+member_type, member_name + member_args))
                        return sorted(_completions)

#uses doxygen to generate xml-based documentation which assists in code completion/suggest functionality in MavensMate
class GenerateApexClassDocsCommand(sublime_plugin.WindowCommand):
    def run(self):
        dinput = util.mm_project_directory() + "/src/classes"
        doutput = util.mm_project_directory() + "/config/.class_docs"
        if os.path.exists(util.mm_project_directory() + "/config/.class_docs/xml"):
            import shutil
            shutil.rmtree(util.mm_project_directory() + "/config/.class_docs/xml")
        if not os.path.exists(util.mm_project_directory() + "/config/.class_docs"):
            os.makedirs(util.mm_project_directory() + "/config/.class_docs")
        if not os.path.exists(util.mm_project_directory() + "/config/.class_docs/xml"):
            os.makedirs(util.mm_project_directory() + "/config/.class_docs/xml")


        printer = PanelPrinter.get(self.window.id())  
        printer.show() 
        printer.write('\nIndexing Apex class definitions...\n')
        threads = []
        thread = ExecuteDoxygen(dinput, doutput)
        threads.append(thread)
        thread.start()
        handle_doxygen_threads(threads, printer)   

    def is_enabled(command):
        return util.is_mm_project()

#prompts users to select a static resource to create a resource bundle
class CreateResourceBundleCommand(sublime_plugin.WindowCommand):
    def run(self):
        srs = []
        for dirname in os.listdir(util.mm_project_directory()+"/src/staticresources"):
            if dirname == '.DS_Store' or dirname == '.' or dirname == '..' or '-meta.xml' in dirname : continue
            srs.append(dirname)
        self.results = srs
        self.window.show_quick_panel(srs, self.panel_done,
            sublime.MONOSPACE_FONT)
    def is_visible(self):
        return util.is_mm_project()

    def panel_done(self, picked):
        if 0 > picked < len(self.results):
            return
        ps = []
        ps.append(util.mm_project_directory()+"/src/staticresources/"+self.results[picked])
        util.create_resource_bundle(self, ps)
        
#deploys selected resource bundle to the server
class DeployResourceBundleCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.rbs_map = {}
        rbs = []
        for dirname in os.listdir(util.mm_project_directory()+"/resource-bundles"):
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
    if os.path.exists(util.mm_project_directory()+"/src/staticresources/"+bundle_name):
        os.remove(util.mm_project_directory()+"/src/staticresources/"+bundle_name)
    # zip bundle to static resource dir 
    os.chdir(util.mm_project_directory()+"/resource-bundles/"+bundle_name)
    cmd = "zip -r -X '"+util.mm_project_directory()+"/src/staticresources/"+bundle_name+"' *"      
    os.system(cmd)
    #compile
    file_path = util.mm_project_directory()+"/src/staticresources/"+bundle_name
    params = {
        "files" : [file_path]
    }
    util.mm_call('compile', params=params)
    util.send_usage_statistics('Deploy Resource Bundle')

#executes doxygen in the background
class ExecuteDoxygen(threading.Thread):
    def __init__(self, dinput, doutput):
        self.result = None
        self.dinput = dinput
        self.doutput = doutput
        threading.Thread.__init__(self)   

    def run(self):
        command = '( cat Doxyfile ; echo "INPUT=\\"'+self.dinput+'\\"" ; echo "EXTENSION_MAPPING=cls=Java" ; echo "OUTPUT_DIRECTORY=\\"'+self.doutput+'\\"" ; echo "OPTIMIZE_OUTPUT_JAVA = YES" ; echo "FILE_PATTERNS += *.cls" ; echo "GENERATE_LATEX = NO" ; echo "GENERATE_HTML = NO" ; echo "GENERATE_XML = YES" ) | ./doxygen -'
        print(command)
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

    for filename in os.listdir(util.mm_project_directory() + "/config/.class_docs/xml"):
        print(filename)
        if filename.startswith('_') or filename.startswith('dir_'): 
            os.remove(util.mm_project_directory() + "/config/.class_docs/xml/" + filename) 
            continue
        if filename == 'combine.xslt' or filename == 'compound.xsd': 
            os.remove(util.mm_project_directory() + "/config/.class_docs/xml/" + filename)
            continue
        tempName = filename
        if tempName.startswith('class_'):
            tempName = tempName.replace('class_', '', 1)
        elif tempName.startswith('enum_'):
            tempName = tempName.replace('enum_', '', 1)
        elif tempName.startswith('interface_'):
            tempName = tempName.replace('interface_', '', 1)
        tempName = tempName.replace('_', '')
        os.rename(util.mm_project_directory() + "/config/.class_docs/xml/" + filename, util.mm_project_directory() + "/config/.class_docs/xml/" + tempName)

    printer.write('\n[Indexing complete]' + '\n')
    printer.hide() 

util.package_check()
util.start_mavensmate_app()  
util.check_for_updates()
util.send_usage_statistics('Startup')
