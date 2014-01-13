# Written by Joe Ferraro (@joeferraro / www.joe-ferraro.com)
import os
import subprocess 
import json
import sys
import re
#dist_dir = os.path.dirname(os.path.abspath(__file__))
#sys.path.insert(0, dist_dir)
from xml.dom.minidom import parse, parseString

if sys.version_info >= (3, 0):
    # Python 3
    import MavensMate.config as config
    import MavensMate.util as util
    import MavensMate.lib.command_helper as command_helper
    import MavensMate.lib.mm_interface as mm
    import MavensMate.lib.upgrader as upgrader
    import MavensMate.lib.resource_bundle as resource_bundle
    import MavensMate.lib.server.lib.server_threaded as server
    import MavensMate.lib.server.lib.config as server_config
    from MavensMate.lib.printer import PanelPrinter
    from MavensMate.lib.threads import ThreadTracker
    import MavensMate.lib.parsehelp as parsehelp
    import MavensMate.lib.vf as vf
    from MavensMate.lib.mm_merge import *
    from MavensMate.lib.completioncommon import *
else:
    # Python 2
    import config
    import util 
    import lib.command_helper as command_helper
    import lib.mm_interface as mm
    import lib.resource_bundle as resource_bundle
    import lib.vf as vf
    from lib.printer import PanelPrinter
    from lib.threads import ThreadTracker
    from lib.mm_merge import *

import sublime
import sublime_plugin

debug = None
settings = sublime.load_settings('mavensmate.sublime-settings')
sublime_version = int(float(sublime.version()))

completioncommon = imp.load_source("completioncommon", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib","completioncommon.py"))
apex_completions = util.parse_json_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib", "apex", "completions.json"))
apex_system_completions = []
for top_level_class_name in apex_completions["publicDeclarations"]["System"].keys():
    apex_system_completions.append((top_level_class_name+"\t[Standard Apex Class]", top_level_class_name))

st_version = 2
# Warn about out-dated versions of ST3
if sublime.version() == '':
    st_version = 3
elif int(sublime.version()) > 3000:
    st_version = 3

if st_version == 3:
    installed_dir, _ = __name__.split('.')
elif st_version == 2:
    installed_dir = os.path.basename(os.getcwd())

reloader_name = 'lib.reloader'

# ST3 loads each package as a module, so it needs an extra prefix
if st_version == 3:
    reloader_name = 'MavensMate.' + reloader_name
    from imp import reload

# Make sure all dependencies are reloaded on upgrade
if reloader_name in sys.modules and sys.version_info >= (3, 0):
    reload(sys.modules[reloader_name])
    from .lib import reloader

try:
    # Python 3
    import MavensMate.lib.reloader as reloader
except (ValueError):
    # Python 2
    import lib.reloader as reloader

def plugin_loaded():
    config.setup_logging()
    server_config.setup_logging()
    global debug
    debug = config.debug
    debug('Loading MavensMate for Sublime Text')
    settings = sublime.load_settings('mavensmate.sublime-settings')
    merge_settings = sublime.load_settings('mavensmate-merge.sublime-settings')
    try:
        server.run(port=settings.get('mm_server_port'))
    except Exception as e:
        debug(e)
    config.settings = settings
    config.merge_settings = merge_settings
    util.package_check()
    util.start_mavensmate_app()  
    util.check_for_updates()
    util.send_usage_statistics('Startup')

####### <--START--> COMMANDS THAT USE THE MAVENSMATE UI ##########

#displays new project dialog
class NewProjectCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        util.check_for_workspace()
        mm.call('new_project', False)
        util.send_usage_statistics('New Project')

#displays edit project dialog
class EditProjectCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('edit_project', False)
        util.send_usage_statistics('Edit Project')

    def is_enabled(command):
        return util.is_mm_project()

#displays unit test dialog
class RunApexUnitTestsCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        active_file = util.get_active_file()
        try:
            if os.path.exists(active_file):
                filename, ext = os.path.splitext(os.path.basename(util.get_active_file()))
                if ext == '.cls':
                    params = {
                        "selected"         : [filename]
                    }
                else:
                    params = {}
            else:
                params = {}
        except:
            params = {}
        mm.call('unit_test', context=command, params=params)
        util.send_usage_statistics('Apex Unit Testing')

    def is_enabled(command):
        return util.is_mm_project()

#launches the execute anonymous UI
class ExecuteAnonymousCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('execute_apex', False)
        util.send_usage_statistics('Execute Anonymous')

    def is_enabled(command):
        return util.is_mm_project()

#displays deploy dialog
class DeployToServerCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('deploy', False)
        util.send_usage_statistics('Deploy to Server')

    def is_enabled(command):
        return util.is_mm_project()

#displays deploy dialog
class NewDebugLogCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('debug_log', True)
        util.send_usage_statistics('New Debug Log')

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
class ForceCompileFileMainMenuCommand(sublime_plugin.WindowCommand):
    def run(self, files=None):       
        debug('FORCE COMPILING!')
        if files == None:
            files = [util.get_active_file()]
        params = {
            "files"     : files,
            "action"    : "overwrite"
        }
        mm.call('compile', context=self.window, params=params)
    
    def is_enabled(self):
       return util.is_mm_project();

#deploys the currently active file
class ForceCompileFileCommand(sublime_plugin.WindowCommand):
    def run(self, files=None):       
        debug('FORCE COMPILING!')
        if files == None:
            files = [util.get_active_file()]
        params = {
            "files"     : files,
            "action"    : "overwrite"
        }
        mm.call('compile', context=self.window, params=params)

#deploys the currently active file
class CompileActiveFileCommand(sublime_plugin.WindowCommand):
    def run(self):       
        params = {
            "files" : [util.get_active_file()]
        }
        mm.call('compile', context=self, params=params)

    def is_enabled(command):
        return util.is_mm_file()

    def is_visible(command):
        return util.is_mm_project()

class SyntaxHandler(sublime_plugin.EventListener):
    def on_load_async(self, view):
        try:
            fn = view.file_name()
            ext = util.get_file_extension(fn)
            if ext == '.cls' or ext == '.trigger':
                if "linux" in sys.platform or "darwin" in sys.platform:
                    view.set_syntax_file(os.path.join("Packages","MavensMate","sublime","lang","Apex.tmLanguage"))
                else:
                    view.set_syntax_file(os.path.join("Packages/MavensMate/sublime/lang/Apex.tmLanguage"))
            elif ext == '.page' or ext == '.component':
                if "linux" in sys.platform or "darwin" in sys.platform:
                    view.set_syntax_file(os.path.join("Packages","HTML","HTML.tmLanguage"))
                else:
                    view.set_syntax_file(os.path.join("Packages/HTML/HTML.tmLanguage"))
            elif ext == '.log' and ('/debug/' in fn or '\\debug\\' in fn or '\\apex-scripts\\logs\\' in fn or '/apex-scripts/logs/' in fn):
                if "linux" in sys.platform or "darwin" in sys.platform:
                    view.set_syntax_file(os.path.join("Packages","MavensMate","sublime","lang","MMLog.tmLanguage"))
                else:
                    view.set_syntax_file(os.path.join("Packages/MavensMate/sublime/lang/MMLog.tmLanguage"))
        except:
            pass

#handles compiling to server on save
class RemoteEdit(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        settings = sublime.load_settings('mavensmate.sublime-settings')
        if settings.get('mm_compile_on_save') == True and util.is_mm_file() == True:
            params = {
                "files" : [util.get_active_file()]
            }
            mm.call('compile', context=view, params=params)

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
        mm.call('compile', context=self, params=params)
        util.send_usage_statistics('Compile Selected Files')

    def is_visible(self, files):
        return util.is_mm_project()

    def is_enabled(self, files):
        if files != None and type(files) is list and len(files) > 0:
            for f in files:
                if util.is_mm_file(f):
                    return True
        return False

#displays unit test dialog
class RunAsyncApexTestsCommand(sublime_plugin.WindowCommand):
    def run(self):
        active_file = util.get_active_file()
        try:
            if os.path.exists(active_file):
                filename, ext = os.path.splitext(os.path.basename(util.get_active_file()))
                if ext == '.cls':
                    params = {
                        "classes"         : [filename]
                    }
                else:
                    params = {}
            else:
                params = {}
        except:
            params = {}
        mm.call('test_async', context=self, params=params)
        util.send_usage_statistics('Async Apex Test')

    def is_enabled(command):
        return util.is_apex_class_file()

#deploys the currently open tabs
class CompileTabsCommand(sublime_plugin.WindowCommand):
    def run (self):
        params = {
            "files"         : util.get_tab_file_names()
        }
        mm.call('compile', context=self, params=params)
        util.send_usage_statistics('Compile Tabs')

#replaces local copy of metadata with latest server copies
class CleanProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.ok_cancel_dialog("Are you sure you want to clean this project? All local (non-server) files will be deleted and your project will be refreshed from the server", "Clean"):
            mm.call('clean_project', context=self)
            util.send_usage_statistics('Clean Project')

    def is_enabled(command):
        return util.is_mm_project()  

#opens a project in the current workspace
class OpenProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        util.check_for_workspace()
        open_projects = []
        try:
            for w in sublime.windows():
                if len(w.folders()) == 0:
                    continue;
                root = w.folders()[0]
                if util.mm_workspace() not in root:
                    continue
                #project_name = root.split("/")[-1]
                project_name = util.get_file_name_no_extension(root)

                open_projects.append(project_name)
        except:
            pass

        import os
        self.dir_map = {}
        dirs = [] 
        #debug(util.mm_workspace())
        workspaces = util.mm_workspace()
        if type(workspaces) is not list:
            workspaces = [workspaces]

        for w in workspaces:
            for dirname in os.listdir(w):
                if dirname == '.DS_Store' or dirname == '.' or dirname == '..' or dirname == '.logs' : continue
                if dirname in open_projects : continue
                if not os.path.isdir(os.path.join(w,dirname)) : continue
                sublime_project_file = dirname+'.sublime-project'
                for project_content in os.listdir(os.path.join(w,dirname)):
                    if '.' not in project_content: continue
                    if project_content == '.sublime-project':
                        sublime_project_file = '.sublime-project'
                        continue
                dirs.append([dirname, "Workspace: "+os.path.basename(w)])
                self.dir_map[dirname] = [dirname, sublime_project_file, w]
        self.results = dirs
        #debug(self.results)
        self.window.show_quick_panel(dirs, self.panel_done,
            sublime.MONOSPACE_FONT)

    def panel_done(self, picked):
        if 0 > picked < len(self.results):
            return
        self.picked_project = self.results[picked]
        project_file = self.dir_map[self.picked_project[0]][1]  
        project_name = self.dir_map[self.picked_project[0]][0]
        workspace = self.dir_map[self.picked_project[0]][2]
        project_file_location = os.path.join(workspace,project_name,project_file)
        #debug(project_file_location)
        
        if not os.path.isfile(project_file_location):
            sublime.message_dialog("Cannot find project file for: "+project_name)
            return

        settings = sublime.load_settings('mavensmate.sublime-settings')
        if sys.platform == 'darwin':
            sublime_path = settings.get('mm_plugin_client_location', '/Applications')
            if sublime_version >= 3000:
                if os.path.exists(os.path.join(sublime_path, 'Sublime Text 3.app')):
                    subprocess.Popen("'"+sublime_path+"/Sublime Text 3.app/Contents/SharedSupport/bin/subl' --project '"+project_file_location+"'", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                elif os.path.exists(os.path.join(sublime_path, 'Sublime Text.app')):
                    subprocess.Popen("'"+sublime_path+"/Sublime Text.app/Contents/SharedSupport/bin/subl' --project '"+project_file_location+"'", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            else:
                subprocess.Popen("'/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl' --project '"+project_file_location+"'", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        elif 'linux' in sys.platform:
            subl_location = settings.get('mm_subl_location', '/usr/local/bin/subl')
            subprocess.Popen("'{0}' --project '"+project_file_location+"'".format(subl_location), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        else:
            subl_location = settings.get('mm_windows_subl_location', '/usr/local/bin/subl')
            if not os.path.isfile(subl_location) and "x86" not in subl_location:
                subl_location = subl_location.replace("Program Files", "Program Files (x86)")
            subprocess.Popen('"{0}" --project "{1}"'.format(subl_location, project_file_location), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

class RunApexScriptCommand(sublime_plugin.WindowCommand):
    def run(self):
        params = {
            "script_name"         : os.path.basename(util.get_active_file())
        }
        mm.call('run_apex_script', context=self, params=params)
        util.send_usage_statistics('Run Apex Script')

    def is_enabled(command):
        try:
            return "apex-scripts" in util.get_active_file() and '.cls' in util.get_active_file()
        except:
            return False

class NewApexScriptCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        sublime.active_window().show_input_panel("Apex Script Name", "MyScriptName", self.finish, None, None)

    def finish(self, name):
        if not os.path.exists(os.path.join(util.mm_project_directory(), "apex-scripts")):
            os.makedirs(os.path.join(util.mm_project_directory(), "apex-scripts"))

        if ".cls" not in name:
            name = name + ".cls"

        f = open(os.path.join(util.mm_project_directory(), "apex-scripts", name), "w")
        f.close()

        sublime.active_window().open_file(os.path.join(util.mm_project_directory(), "apex-scripts", name))

    def is_enabled(command):
        return util.is_mm_project()

#displays new apex class dialog
class NewApexClassCommand(sublime_plugin.TextCommand):
    
    def __init__(self, *args, **kwargs):
        sublime_plugin.TextCommand.__init__(self, *args, **kwargs)
        self.template_options   = None
        self.github_templates   = None
        self.api_name           = None
        self.github_template    = None

    def run(self, edit, api_name="MyClass", class_type="default"): 
        self.template_options = []
        self.github_templates = util.parse_templates_package("ApexClass")
        for t in self.github_templates:
            self.template_options.append([t["name"], t["description"], "Author: "+t["author"]])
        sublime.active_window().show_quick_panel(self.template_options, self.on_select_from_github_template)
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
        mm.call('new_metadata', params=options) 

    def on_select_from_github_template(self, selection):
        if selection != -1:
            template_name = self.template_options[selection][0]
            for t in self.github_templates:
                if t["name"] == template_name:
                    self.github_template = t
                    break

            sublime.active_window().show_input_panel("Apex Class Name", "MyClassName", self.finish_github_template_selection, None, None)
             
    def finish_github_template_selection(self, api_name):
        if '.cls' in api_name:
            api_name = api_name.replace('.cls', '')
        params = {
            'metadata_type'     : 'ApexClass',
            'metadata_name'     : api_name,
            'github_template'   : self.github_template
        }
        mm.call('new_metadata', params=params)


    def is_enabled(self):
        return util.is_mm_project()

#displays new apex trigger dialog
class NewApexTriggerCommand(sublime_plugin.TextCommand):
    def __init__(self, *args, **kwargs):
        sublime_plugin.TextCommand.__init__(self, *args, **kwargs)
        self.template_options   = None
        self.github_templates   = None
        self.api_name           = None
        self.github_template    = None

    def run(self, edit, api_name="MyAccountTrigger", sobject_name="Account", class_type="default"): 
        self.template_options = []
        self.github_templates = util.parse_templates_package("ApexTrigger")
        for t in self.github_templates:
            self.template_options.append([t["name"], t["description"], "Author: "+t["author"]])
        sublime.active_window().show_quick_panel(self.template_options, self.on_select_from_github_template)
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
        mm.call('new_metadata', params=options) 

    def on_select_from_github_template(self, selection):
        if selection != -1:
            template_name = self.template_options[selection][0]
            for t in self.github_templates:
                if t["name"] == template_name:
                    self.github_template = t
                    break
            sublime.active_window().show_input_panel("Apex Trigger Name, Trigger Object API Name", "MyTriggerName, Account", self.finish_github_template_selection, None, None)
             
    def finish_github_template_selection(self, api_name):
        api_name, sobject_name = [x.strip() for x in api_name.split(',')]
        params = {
            'metadata_type'     : 'ApexTrigger',
            'object_api_name'   : sobject_name,
            'metadata_name'     : api_name,
            'github_template'   : self.github_template
        }
        mm.call('new_metadata', params=params)

    def is_enabled(command):
        return util.is_mm_project() 

#displays new apex page dialog
class NewApexPageCommand(sublime_plugin.TextCommand):
    def __init__(self, *args, **kwargs):
        sublime_plugin.TextCommand.__init__(self, *args, **kwargs)
        self.template_options   = None
        self.github_templates   = None
        self.api_name           = None
        self.github_template    = None

    def run(self, edit, api_name="MyPage", class_type="default"): 
        self.template_options = []
        self.github_templates = util.parse_templates_package("ApexPage")
        for t in self.github_templates:
            self.template_options.append([t["name"], t["description"], "Author: "+t["author"]])
        sublime.active_window().show_quick_panel(self.template_options, self.on_select_from_github_template)
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
        mm.call('new_metadata', params=options) 

    def on_select_from_github_template(self, selection):
        if selection != -1:
            template_name = self.template_options[selection][0]
            for t in self.github_templates:
                if t["name"] == template_name:
                    self.github_template = t
                    break

            sublime.active_window().show_input_panel("Visualforce Page Name", "MyVisualforcePageName", self.finish_github_template_selection, None, None)
             
    def finish_github_template_selection(self, api_name):
        if '.cls' in api_name:
            api_name = api_name.replace('.page', '')
        params = {
            'metadata_type'     : 'ApexPage',
            'metadata_name'     : api_name,
            'github_template'   : self.github_template
        }
        mm.call('new_metadata', params=params)

    def is_enabled(command):
        return util.is_mm_project()

#displays new apex component dialog
class NewApexComponentCommand(sublime_plugin.TextCommand):
    def __init__(self, *args, **kwargs):
        sublime_plugin.TextCommand.__init__(self, *args, **kwargs)
        self.template_options   = None
        self.github_templates   = None
        self.api_name           = None
        self.github_template    = None

    def run(self, edit, api_name="MyComponent", class_type="default"): 
        self.template_options = []
        self.github_templates = util.parse_templates_package("ApexComponent")
        for t in self.github_templates:
            self.template_options.append([t["name"], t["description"], "Author: "+t["author"]])
        sublime.active_window().show_quick_panel(self.template_options, self.on_select_from_github_template)
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
        mm.call('new_metadata', params=options) 

    def on_select_from_github_template(self, selection):
        if selection != -1:
            template_name = self.template_options[selection][0]
            for t in self.github_templates:
                if t["name"] == template_name:
                    self.github_template = t
                    break

            sublime.active_window().show_input_panel("Visualforce Component Name", "MyComponentName", self.finish_github_template_selection, None, None)
             
    def finish_github_template_selection(self, api_name):
        if '.cls' in api_name:
            api_name = api_name.replace('.component', '')
        params = {
            'metadata_type'     : 'ApexComponent',
            'metadata_name'     : api_name,
            'github_template'   : self.github_template
        }
        mm.call('new_metadata', params=params)

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
        sublime.message_dialog("MavensMate for Sublime Text v"+version+"\n\nMavensMate for Sublime Text is an open source Sublime Text plugin for Force.com development.\n\nhttp://mavensmate.com")

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
            mm.call('refresh', context=self, params=params)
            util.send_usage_statistics('Refresh Selected From Server')

    def is_visible(self, dirs, files):
        return util.is_mm_project()

    # def is_enabled(self, dirs, files):
    #     if dirs != None and type(dirs) is list and len(dirs) > 0:
    #         for d in dirs:
    #             if util.is_config.mm_dir(d):
    #                 return True
    #     if files != None and type(files) is list and len(files) > 0:
    #         for f in files:
    #             if util.util.is_mm_file(f):
    #                 return True
    #     return False

class RefreshActivePropertiesFromServerCommand(sublime_plugin.WindowCommand):
    def run (self):
        if sublime.ok_cancel_dialog("Are you sure you want to overwrite the selected files' apex properties from Salesforce?", "Refresh Apex Properties"):
            params = {
                "files"         : [util.get_active_file()]
            }
            mm.call('refresh_properties', context=self, params=params)
            util.send_usage_statistics('Refresh Active Properties From Server')

    def is_visible(self):
        if not util.is_mm_file():
            return False
        filename = util.get_active_file()
        basename = os.path.basename(filename)
        data = util.get_apex_file_properties()
        if not basename in data:
            return True
        elif 'conflict' in data[basename] and data[basename]['conflict'] == True:
            return True
        else:
            return False

class RefreshPropertiesFromServerCommand(sublime_plugin.WindowCommand):
    def run (self, dirs, files):
        if sublime.ok_cancel_dialog("Are you sure you want to overwrite the selected files' apex properties from Salesforce?", "Refresh Apex Properties"):
            if dirs != None and type(dirs) is list and len(dirs) > 0:
                params = {
                    "directories"   : dirs
                }
            elif files != None and type(files) is list and len(files) > 0:
                params = {
                    "files"         : files
                }
            mm.call('refresh_properties', context=self, params=params)
            util.send_usage_statistics('Refresh Selected Properties From Server')

    def is_visible(self, dirs, files):
        if not util.is_mm_project():
            return False
        if files != None and type(files) is list and len(files) > 0:
            filename = files[0]
            basename = os.path.basename(filename)
            data = util.get_apex_file_properties()
            if not basename in data:
                return True
            elif 'conflict' in data[basename] and data[basename]['conflict'] == True:
                return True
            else:
                return False
        return True

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
class RefreshActiveFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.ok_cancel_dialog("Are you sure you want to overwrite this file's contents from Salesforce?", "Refresh"):
            params = {
                "files"         : [util.get_active_file()]
            }
            mm.call('refresh', context=self, params=params)
            util.send_usage_statistics('Refresh Active File From Server')

    def is_visible(self):
        return util.is_mm_file()

#refreshes the currently active file from the server
class SynchronizeActiveMetadataCommand(sublime_plugin.WindowCommand):
    def run(self):
        params = {
            "files"         : [util.get_active_file()]
        }
        mm.call('synchronize', context=self, params=params)
        util.send_usage_statistics('Synchronized Active File to Server')

    def is_visible(self):
        return util.is_mm_file()


#opens the apex class, trigger, component or page on the server
class SynchronizeSelectedMetadataCommand(sublime_plugin.WindowCommand):
    def run (self, dirs, files):
        if dirs != None and type(dirs) is list and len(dirs) > 0:
            params = {
                "directories"   : dirs
            }
        elif files != None and type(files) is list and len(files) > 0:
            params = {
                "files"         : files
            }
        mm.call('synchronize', context=self, params=params)
        util.send_usage_statistics('Synchronized Selected Metadata With Server')

    def is_visible(self, dirs, files):
        if dirs != None and type(dirs) is list and len(dirs) > 0:
            for d in dirs:
                if util.is_config.mm_dir(d):
                    return True
        if files != None and type(files) is list and len(files) > 0:
            for f in files:
                if util.is_mm_file(f):
                    return True
        return False

#opens the apex class, trigger, component or page on the server
class RunActiveApexTestsCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename, ext = os.path.splitext(os.path.basename(util.get_active_file()))
        params = {
            "selected"         : [filename]
        }
        mm.call('unit_test', context=self, params=params)
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

            mm.call('unit_test', context=self, params=params)
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
        mm.call('open_sfdc_url', context=self, params=params)
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
        mm.call('open_sfdc_url', context=self, params=params)
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
        mm.call('open_sfdc_url', context=self, params=params)
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
        mm.call('open_sfdc_url', context=self, params=params)
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
            mm.call('delete', context=self, params=params)
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
            result = mm.call('delete', context=self, params=params)
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
            mm.call('compile_project', context=self)
            util.send_usage_statistics('Compile Project')

    def is_enabled(command):
        return util.is_mm_project()

#refreshes the currently active file from the server
class IndexApexFileProperties(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('index_apex', False, context=self)
        util.send_usage_statistics('Index Apex File Properties')  

    def is_enabled(command):
        return util.is_mm_project()

#indexes the meta data based on packages.xml
class IndexMetadataCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('index_metadata', True, context=self)
        util.send_usage_statistics('Index Metadata')  

    def is_enabled(command):
        return util.is_mm_project()

class NewQuickLogCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('new_quick_log', True)
        util.send_usage_statistics('New Quick Log')

#refreshes the currently active file from the server
class FetchLogsCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('fetch_logs', True)
        util.send_usage_statistics('Fetch Apex Logs')  

#refreshes the currently active file from the server
class FetchCheckpointsCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('fetch_checkpoints', True)
        util.send_usage_statistics('Fetch Apex Checkpoints')  


#when a class or trigger file is opened, adds execution overlay markers if applicable
class HideApexCheckpoints(sublime_plugin.WindowCommand):
    def run(self):
        try:
            util.clear_marked_line_numbers(self.window.active_view(), "overlay")
        except Exception:
            debug('error hidding checkpoints')

    def is_enabled(self):
        return util.is_apex_class_file() 

#when a class or trigger file is opened, adds execution overlay markers if applicable
class ShowApexCheckpoints(sublime_plugin.WindowCommand):
    def run(self):
        debug('attempting to load apex overlays for current file')
        try:
            active_view = self.window.active_view()
            fileName, ext = os.path.splitext(active_view.file_name())
            debug(fileName)
            debug(ext)
            if ext == ".cls" or ext == ".trigger":
                api_name = fileName.split("/")[-1] 
                overlays = util.parse_json_from_file(util.mm_project_directory()+"/config/.overlays")
                lines = []
                for o in overlays:
                    if o['API_Name'] == api_name:
                        lines.append(int(o["Line"]))
                sublime.set_timeout(lambda: util.mark_overlays(active_view, lines), 10)
        except Exception as e:
            debug('execution overlay loader error')
            debug('', e)

    def is_enabled(self):
        return util.is_apex_class_file() 

#deletes overlays
class DeleteApexCheckpointCommand(sublime_plugin.WindowCommand):
    def run(self):
        #options = [['Delete All In This File', '*']]
        options = []
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
        mm.call('delete_apex_overlay', context=self, params=params, message="Deleting checkpoint...", callback=self.reload)
        util.send_usage_statistics('Delete Apex Checkpoint') 

    def reload(self, cmd=None):
        debug("Reloading Apex Checkpoints")
        cmd.window.run_command("show_apex_checkpoints") 

    def is_enabled(self):
        return util.is_apex_class_file()  


#refreshes the currently active file from the server
class IndexApexCheckpointsCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('index_apex_overlays', False, context=self, callback=self.reload)
        util.send_usage_statistics('Index Apex Overlays')  

    def is_enabled(command):
        return util.is_mm_project()

    def reload(self, cmd=None):
        debug("Reloading Apex Checkpoints")
        cmd.window.run_command("show_apex_checkpoints")

#refreshes the currently active file from the server
class ResetMetadataContainerCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('reset_metadata_container', True, context=self, message="Fetching new MetadataContainer...")
        util.send_usage_statistics('Reset Metadata Container')  

    def is_enabled(command):
        return util.is_mm_project()

#creates a new overlay
class NewApexCheckpoint(sublime_plugin.WindowCommand):
    def run(self):
        fileName, ext = os.path.splitext(util.get_active_file())
        if ext == ".cls" or ext == ".trigger":
            if ext == '.cls':
                self.object_type = 'ApexClass'
            else: 
                self.object_type = 'ApexTrigger'
            self.api_name = fileName.split("/")[-1] 
            number_of_lines = util.get_number_of_lines_in_file(util.get_active_file())
            lines = list(range(number_of_lines))
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
        mm.call('new_apex_overlay', context=self, params=params, message="Creating new checkpoint at line "+self.line_number+"...", callback=self.reload)
        util.send_usage_statistics('New Apex Overlay')  

    def reload(self, cmd=None):
        debug("Reloading Apex Checkpoints")
        cmd.window.run_command("show_apex_checkpoints")

    def is_enabled(self):
        return util.is_apex_class_file() 

#right click context menu support for resource bundle creation
class NewResourceBundleCommand(sublime_plugin.WindowCommand):
    def run(self, files, dirs):
        if sublime.ok_cancel_dialog("Are you sure you want to create resource bundle(s) for the selected static resource(s)", "Create Resource Bundle(s)"):
            resource_bundle.create(self, files) 
            util.send_usage_statistics('New Resource Bundle (Sidebar)')

    def is_visible(self, files, dirs):
        if not util.is_mm_project():
            return False
        if dirs != None and type(dirs) is list and len(dirs) > 0:
            return False
        is_ok = True
        if files != None and type(files) is list and len(files) > 0:
            for f in files:
                basename = os.path.basename(f)
                if "." not in basename:
                    is_ok = False
                    return
                if "." in basename and basename.split(".")[-1] != "resource":
                    is_ok = False
                    break
        return is_ok   

#right click context menu support for resource bundle refresh
class RefreshResourceBundleCommand(sublime_plugin.WindowCommand):
    def run(self, dirs, files):
        if sublime.ok_cancel_dialog("This command will refresh the resource bundle(s) based on your local project's corresponding static resource(s). Do you wish to continue?", "Refresh"):
            resource_bundle.refresh(self, dirs) 
            util.send_usage_statistics('Refresh Resource Bundle (Sidebar)')
    def is_visible(self, dirs, files):
        try:
            if files != None and type(files) is list and len(files) > 0:
                return False

            if not util.is_mm_project():
                return False
            is_ok = True
            if dirs != None and type(dirs) is list and len(dirs) > 0:
                for d in dirs:
                    basename = os.path.basename(d)
                    if "." not in basename:
                        is_ok = False
                        break
                    if "." in basename and basename.split(".")[-1] != "resource":
                        is_ok = False
                        break
            return is_ok  
        except:
            return False 

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
        
        dir_entries = os.listdir(os.path.join(directory,"src"))
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
        mm.call('new_project_from_existing_directory', params=params)
        util.send_usage_statistics('New Project From Existing Directory')  

    def is_visible(self, dirs):
        if dirs != None and type(dirs) is list and len(dirs) > 1:
            return False
        if util.is_mm_project():
            return False
        directory = dirs[0]
        if not os.path.isfile(os.path.join(directory, "src", "package.xml")):
            return False
        if not os.path.exists(os.path.join(directory, "src")):
            return False
        return True

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

class WriteOperationStatus(sublime_plugin.TextCommand):
    def run(self, edit, text, *args, **kwargs):
        kw_region = kwargs.get('region', [0,0])
        status_region = sublime.Region(kw_region[0],kw_region[1])
        size = self.view.size()
        self.view.set_read_only(False)
        self.view.replace(edit, status_region, text)
        self.view.set_read_only(True)
        #self.view.show(size)

    def is_visible(self):
        return False

    def is_enabled(self):
        return True

    def description(self):
        return

class CancelCurrentCommand(sublime_plugin.WindowCommand):
    
    def run(self):
        current_thread = ThreadTracker.get_current(self.window.id())
        if current_thread:
            current_thread.kill()

    #def is_visible(self, paths = None):
    #    return ThreadTracker.get_current(self.window.id()) != None

####### <--START--> COMMANDS THAT ARE NOT *OFFICIALLY* SUPPORTED IN 2.0 BETA ##########

#updates MavensMate plugin
class UpdateMeCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        if 'darwin' in sys.platform:
            sublime.message_dialog("Use the \"Plugins\" option in MavensMate.app to update MavensMate for Sublime Text.")
        elif 'linux' in sys.platform:
            printer = PanelPrinter.get(sublime.active_window().id())
            upgrader.execute(printer)
        elif 'win32' in sys.platform or 'win64' in sys.platform:
            updater_path = os.path.join(os.environ["ProgramFiles"],"MavensMate","MavensMate-SublimeText.exe")
            if not os.path.isfile(updater_path):
                updater_path = updater_path.replace("Program Files", "Program Files (x86)")
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen('"{0}"'.format(updater_path), startupinfo=startupinfo)

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
                mm.call('new_metadata', params=options)
            elif ps[0] == 'bundle' or ps[0] == 'b':
                deploy_resource_bundle(ps[1])
            else:
                util.print_debug_panel_message('Unrecognized command: ' + input + '\n')
        except:
            util.print_debug_panel_message('Unrecognized command: ' + input + '\n')

#completions for visualforce
class VisualforceCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        #if user has opted out of autocomplete or this isnt a mm project, ignore it
        if settings.get('mm_autocomplete') == False or util.is_mm_project() == False:
            return []

        #only run completions for Apex Pages and Components
        ext = util.get_file_extension(view.file_name())
        if ext != '.page' and ext != '.component':
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        ch2 = view.substr(sublime.Region(pt, pt + 2))
        
        if ch2 == '<a' or ch2 == '<c':
            _completions = []
            for t in vf.tag_list:
                 _completions.append((t, t))
            return _completions

        elif ch == ':':
            debug('SCOPE: ', view.scope_name(pt))
            word = view.substr(view.word(pt))        
            _completions = []
            for t in vf.tag_list:
                if word in t:
                    _completions.append((t, t))
            return _completions

        elif ch == ' ':
            debug('SCOPE: ', view.scope_name(pt))
            scope_names = view.scope_name(pt).split(' ')
            if 'string.quoted.double.html' in scope_names or 'string.quoted.single.html' in scope_names:
                return []

            if 'meta.tag.other.html' in scope_names:
                region_from_top_to_current_word = sublime.Region(0, pt + 1)
                lines = view.lines(region_from_top_to_current_word)
                
                _completions = []
                tag_def = None
                for line in reversed(lines):
                    line_contents = view.substr(line)
                    line_contents = line_contents.replace("\t", "").strip()
                    if line_contents.find('<') == -1: continue #skip the line if the opening bracket isn't in the line
                    tag_def = line_contents.split('<')[-1].split(' ')[0]
                    break

                #debug(tag_def)
                if tag_def in vf.tag_defs:
                    def_entry = vf.tag_defs[tag_def]

                    for key, value in def_entry['attribs'].items():
                        _completions.append((key + '\t(' + value['type'] + ')', key+'="${1:'+value['type']+'}"'))

                    return sorted(_completions)
                else:
                    completion_flags = (
                        sublime.INHIBIT_WORD_COMPLETIONS |
                        sublime.INHIBIT_EXPLICIT_COMPLETIONS
                    )
                    return ([], completion_flags)
            elif 'source.js.embedded.html' in scope_names:
                return []
            else:
                completion_flags = (
                    sublime.INHIBIT_WORD_COMPLETIONS |
                    sublime.INHIBIT_EXPLICIT_COMPLETIONS
                )
                return ([], completion_flags)
        else:
            completion_flags = (
                sublime.INHIBIT_WORD_COMPLETIONS |
                sublime.INHIBIT_EXPLICIT_COMPLETIONS
            )
            return ([], completion_flags)

class SalesforceGenericCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        #if user has opted out of autocomplete or this isnt a mm project, ignore it
        if settings.get('mm_autocomplete') == False or util.is_mm_project() == False:
            return []

        #only run completions for Apex Triggers and Classes
        ext = util.get_file_extension(view.file_name())
        if ext != '.cls' and ext != '.trigger':
            return []

        # debug('prefix: ',prefix)
        # debug('locations: ',locations)
        # pt1 = locations[0] - len(prefix) + 1
        # right_of_point = view.substr(pt1)
        # debug('right of pt: ',right_of_point)

        #now get the autocomplete context
        #if not dot notation, ignore
        pt = locations[0] - len(prefix) - 1
        # debug(view.scope_name(pt))
        scope_name = view.scope_name(pt)
        #debug(scope_name)
        if 'string.quoted.single.java' in scope_name:
            return []
        if 'string.quoted.brackets.soql.apex' in scope_name:
            return []

        ch = view.substr(sublime.Region(pt, pt + 1))
        if ch == '.': return []
        ltr = view.substr(sublime.Region(pt, pt + 2))
        if not ltr.isupper(): return []

        _completions = []

        if os.path.isfile(os.path.join(util.mm_project_directory(),"config",".org_metadata")): #=> parse org metadata, looking for object names
            jsonData = util.parse_json_from_file(os.path.join(util.mm_project_directory(),"config",".org_metadata"))
            for metadata_type in jsonData:
                if 'xmlName' in metadata_type and metadata_type['xmlName'] == 'CustomObject':
                    for object_type in metadata_type['children']:
                        _completions.append((object_type['text']+"\t[Sobject Name]", object_type['text']))

        if os.path.isfile(os.path.join(util.mm_project_directory(),"config",".apex_file_properties")): #=> parse org metadata, looking for object names
            jsonData = util.parse_json_from_file(os.path.join(util.mm_project_directory(),"config",".apex_file_properties"))
            for element in jsonData.keys():
                if "unpackaged/classes" in element or "unpackaged\classes" in element:
                    continue
                if ".cls" in element:
                    class_name = element.replace(".cls", "")
                    if "/" in class_name:
                        class_name = class_name.split("/")[-1]
                    if "\\" in class_name:
                        class_name = class_name.split("\\")[-1]
                    _completions.append((class_name+"\t[Custom Apex Class]", class_name))

        #debug(apex_system_completions)
        _completions.extend(apex_system_completions)

        return _completions

#completions for force.com-specific use cases
class ApexCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        #if user has opted out of autocomplete or this isnt a mm project, ignore it
        if settings.get('mm_autocomplete') == False or util.is_mm_project() == False:
            return []

        #only run completions for Apex Triggers and Classes
        ext = util.get_file_extension(view.file_name())
        if ext != '.cls' and ext != '.trigger':
            return []

        full_file_path = os.path.splitext(util.get_active_file())[0]
        base = os.path.basename(full_file_path)
        file_name = os.path.splitext(base)[0] 

        #now get the autocomplete context
        #if not dot notation, ignore
        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if not ch == '.': return []
        scope_name = view.scope_name(pt)
        debug(scope_name)
        if 'string.quoted.brackets.soql.apex' in scope_name:
            return []

        #myVariable.
        #if we cant find myVariable properly, exit out
        word = view.substr(view.word(pt))        
        if word == None or word == '':
            return [] 

        debug('autocomplete word: ', word)
        
        ##OK START COMPLETIONS
        _completions = []
        lower_word = word.lower()
        completion_flags = (
            sublime.INHIBIT_WORD_COMPLETIONS |
            sublime.INHIBIT_EXPLICIT_COMPLETIONS
        )

        data = view.substr(sublime.Region(0, locations[0]-len(prefix)))

        #full_data = view.substr(sublime.Region(0, view.size()))
        typedef = parsehelp.get_type_definition(data)
        debug('autocomplete type definition: ', typedef)

        if '<' not in typedef[2] and '[' not in typedef[2]:
            if '.' in typedef[2] and '<' not in typedef[2]:
                type_parts = typedef[2].split('.')
                typedef_class = type_parts[0] #e.g. ApexPages
                typedef_class_lower = typedef_class.lower()
                typedef_class_extra = type_parts[1] #e.g. StandardController
                typedef_class_extra_lower = typedef_class_extra.lower()
            else:
                typedef_class = typedef[2] #e.g. ApexPages
                typedef_class_lower = typedef_class.lower()
                typedef_class_extra = typedef[4].replace('.','') #e.g. StandardController
                typedef_class_extra_lower = typedef_class_extra.lower()

            if '<' in typedef_class:
                typedef_class_lower = re.sub('\<.*?\>', '', typedef_class_lower)
                typedef_class_lower = re.sub('\<', '', typedef_class_lower)
                typedef_class_lower = re.sub('\>', '', typedef_class_lower)
                typedef_class       = re.sub('\<.*?\>', '', typedef_class)
                typedef_class       = re.sub('\<', '', typedef_class)
                typedef_class       = re.sub('\>', '', typedef_class)

            if '[' in typedef_class:
                typedef_class_lower = re.sub('\[.*?\]', '', typedef_class_lower)
                typedef_class       = re.sub('\[.*?\]', '', typedef_class)
        else:
            if '<' in typedef[2]:
                typedef_class = typedef[2].split('<')[0]
            elif '[' in typedef[2]:
                typedef_class = typedef[2].split('[')[0]
            typedef_class_lower = typedef_class.lower()
            typedef_class_extra = ''
            typedef_class_extra_lower = ''



        debug('autocomplete type: ', typedef_class) #String
        debug('autocomplete type extra: ', typedef_class_extra) #String

        legacy_classes = ['system', 'search', 'limits', 'enum', 'trigger']

        if typedef_class_lower in legacy_classes and os.path.isfile(os.path.join(config.mm_dir,"lib","apex","classes",typedef_class_lower+".json")): #=> apex instance methods
            json_data = open(os.path.join(config.mm_dir,"lib","apex","classes",typedef_class_lower+".json"))
            data = json.load(json_data)
            json_data.close()
            pd = data["static_methods"]
            for method in pd:
                _completions.append((method, method))
            completion_flags = (
                sublime.INHIBIT_WORD_COMPLETIONS |
                sublime.INHIBIT_EXPLICIT_COMPLETIONS
            )
            #return (_completions, completion_flags)
            return sorted(_completions)

        if word == 'Page' and os.path.isdir(os.path.join(util.mm_project_directory(),"src","pages")):
            for (dirpath, dirnames, filenames) in os.walk(os.path.join(util.mm_project_directory(),"src","pages")):
                for f in filenames:
                    if '-meta.xml' in f: continue
                    base_page_name = f.replace(".page", "")
                    _completions.append((base_page_name+"\t[Visualforce Page]", base_page_name))
            completion_flags = (
                sublime.INHIBIT_WORD_COMPLETIONS |
                sublime.INHIBIT_EXPLICIT_COMPLETIONS
            )
            return (_completions, completion_flags)

        if len(typedef[4]) > 1 and '.' in typedef[4]:
            #deeply nested, need to look for properties
            #TODO 
            return []

        apex_class_key = typedef_class
        if apex_class_key == 'DateTime':
            apex_class_key = 'Datetime'

        if apex_class_key in apex_completions["publicDeclarations"] and typedef_class_extra_lower == '':
            apex_class_key = word
            if apex_class_key == 'DateTime':
                apex_class_key = 'Datetime'
            comp_def = apex_completions["publicDeclarations"].get(apex_class_key)
            for i in comp_def:
                _completions.append((i, i))
            return sorted(_completions)
        elif apex_completions["publicDeclarations"].get(apex_class_key) != None:
            top_level = apex_completions["publicDeclarations"].get(typedef_class)
            sub_def = top_level.get(word)
            if sub_def == None:
                sub_def = top_level.get(typedef_class_extra)
            _completions = util.get_symbol_table_completions(sub_def)
            return sorted(_completions)
        elif apex_class_key in apex_completions["publicDeclarations"]["System"]:
            if typedef_class == 'DateTime':
                typedef_class = 'Datetime'
            if word == typedef_class: #static
                comp_def = apex_completions["publicDeclarations"]["System"].get(apex_class_key)
            else: #instance
                comp_def = apex_completions["publicDeclarations"]["System"].get(typedef_class)
            _completions = util.get_symbol_table_completions(comp_def)
            return sorted(_completions)

        ## HANDLE CUSTOM APEX CLASS STATIC METHODS 
        ## MyCustomClass.some_static_method
        elif os.path.isfile(os.path.join(util.mm_project_directory(),"src","classes",word+".cls")):
            try:
                _completions = util.get_apex_completions(word) 
                return sorted(_completions) 
            except:
                return [] 

        if typedef_class_lower == None:
            return []

        ## HANDLE CUSTOM APEX INSTANCE METHOD ## 
        ## MyClass foo = new MyClass()
        ## foo.??  
        symbol_table = util.get_symbol_table(file_name)

        if symbol_table != None and "innerClasses" in symbol_table and type(symbol_table["innerClasses"] is list and len(symbol_table["innerClasses"]) > 0):
            for ic in symbol_table["innerClasses"]:
                if ic["name"].lower() == typedef_class_lower:
                    _completions = util.get_completions_for_inner_class(ic)
                    return sorted(_completions)  

        if os.path.isfile(os.path.join(util.mm_project_directory(),"src","classes",typedef_class+".cls")): #=> apex classes
            _completions = util.get_apex_completions(typedef_class, typedef_class_extra)
            return sorted(_completions)
        
        if typedef_class.endswith('__r'):
            typedef_class = typedef_class.replace('__r', '__c')
        if os.path.isfile(os.path.join(util.mm_project_directory(),"src","objects",typedef_class+".object")): #=> object fields from src directory (more info on field metadata, so is primary)
            object_dom = parse(os.path.join(util.mm_project_directory(),"src","objects",typedef_class+".object"))
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
        elif os.path.isfile(os.path.join(util.mm_project_directory(),"config",".org_metadata")): #=> parse org metadata, looking for object fields
            jsonData = util.parse_json_from_file(os.path.join(util.mm_project_directory(),"config",".org_metadata"))
            for metadata_type in jsonData:
                if 'xmlName' in metadata_type and metadata_type['xmlName'] == 'CustomObject':
                    for object_type in metadata_type['children']:
                        if 'text' in object_type and object_type['text'].lower() == typedef_class_lower:
                            for attr in object_type['children']:
                                if 'text' in attr and attr['text'] == 'fields':
                                    for field in attr['children']:
                                        _completions.append((field['text'], field['text']))
            if len(_completions) == 0 and '__c' in typedef_class_lower:
                try:
                    #need to index custom objects here, because it couldnt be found
                    if len(ThreadTracker.get_pending_mm_panel_threads(sublime.active_window())) == 0:
                        params = {
                            'metadata_types' : ['CustomObject']
                        }
                        mm.call('refresh_metadata_index', False, params=params)
                except:
                    debug('Failed to index custom object metadata')
            else:
                _completions.append(('Id', 'Id'))
                return (sorted(_completions), completion_flags)
        else:
            return []

#prompts users to select a static resource to create a resource bundle
class CreateResourceBundleCommand(sublime_plugin.WindowCommand):
    def run(self):
        srs = []
        for dirname in os.listdir(os.path.join(util.mm_project_directory(),"src","staticresources")):
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
        ps.append(os.path.join(util.mm_project_directory(),"src","staticresources",self.results[picked]))
        resource_bundle.create(self, ps)

#deploys selected resource bundle to the server
class DeployResourceBundleCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.rbs_map = {}
        rbs = []
        for dirname in os.listdir(os.path.join(util.mm_project_directory(),"resource-bundles")):
            if dirname == '.DS_Store' or dirname == '.' or dirname == '..' : continue
            rbs.append(dirname)
        self.results = rbs
        self.window.show_quick_panel(rbs, self.panel_done,
            sublime.MONOSPACE_FONT)

    def panel_done(self, picked):
        if 0 > picked < len(self.results):
            return
        resource_bundle.deploy(self.results[picked])

#opens a file 
class OpenFileInProject(sublime_plugin.ApplicationCommand):
    def run(self, project_name, file_name, line_number):       
        window = sublime.active_window()
        for w in sublime.windows():
            if w.project_file_name() == None:
                continue
            if project_name+".sublime-project" in w.project_file_name():
                window = w
                break
        window.open_file("{0}:{1}:{2}".format(file_name, line_number, 0), sublime.ENCODED_POSITION)
        view = window.active_view()
        view.erase_regions("health_item")
        if line_number != 0:
            sublime.set_timeout(lambda: self.mark_line(view, line_number), 100)

    def mark_line(self, view, line_number):
        view.add_regions("health_item", [view.line(view.text_point(line_number-1, 0))], "foo", "bookmark", sublime.DRAW_OUTLINED)

class ProjectHealthCheckCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('project_health_check')
        util.send_usage_statistics('Project Health Check')  

    def is_enabled(command):
        return util.is_mm_project()

class SignInWithGithub(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('github')
        util.send_usage_statistics('Github Sign In')

    def is_enabled(command):
        return util.is_mm_project()

class ConnectProjectWithGithub(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('github_connect_project')
        util.send_usage_statistics('Github Project Connect')

    def is_enabled(command):
        if util.is_mm_project():
            if os.path.isfile(os.path.join(util.mm_project_directory(),"config",".github")):
                return True
        return False




