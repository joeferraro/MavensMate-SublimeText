# Written by Joe Ferraro (@joeferraro / www.joe-ferraro.com)
import sublime
import sublime_plugin
import os
import json
import sys
import re
from xml.dom.minidom import parse

import MavensMate.config as config
import MavensMate.util as util
import MavensMate.lib.cli as mm
from MavensMate.lib.printer import PanelPrinter
from MavensMate.lib.threads import ThreadTracker
import MavensMate.lib.parsehelp as parsehelp
import MavensMate.lib.vf as vf
from MavensMate.lib.merge import *
from MavensMate.lib.completioncommon import *
import MavensMate.lib.community as community

import shutil

debug = None
settings = sublime.load_settings('mavensmate.sublime-settings')
sublime_version = int(float(sublime.version()))

completioncommon = imp.load_source("completioncommon", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib","completioncommon.py"))
apex_completions = util.parse_json_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib", "apex", "completions.json"))
apex_system_completions = []
for top_level_class_name in apex_completions["publicDeclarations"]["System"].keys():
    apex_system_completions.append((top_level_class_name+"\t[Standard Apex Class]", top_level_class_name))

reloader_name = 'MavensMate.lib.reloader'
from imp import reload
# Make sure all dependencies are reloaded on upgrade
if reloader_name in sys.modules and sys.version_info >= (3, 0):
    reload(sys.modules[reloader_name])
    from .lib import reloader

import MavensMate.lib.reloader as reloader

def plugin_loaded():
    settings = sublime.load_settings('mavensmate.sublime-settings')

    config.setup_logging()
    global debug
    debug = config.debug
    debug('=============> Starting MavensMate for Sublime Text')

    active_window_id = sublime.active_window().id()
    printer = PanelPrinter.get(active_window_id)

    merge_settings = sublime.load_settings('mavensmate-merge.sublime-settings')
    config.settings = settings
    config.merge_settings = merge_settings
    util.package_check()

    try:
        mm.check_server()

        message = 'Happy coding :)'
        printer.show()
        printer.write('\n'+message+'\n')
    except Exception as e:
        printer.show()
        message = '[ERROR]: '+str(e)+'\n'
        printer.write('\n'+message+'\n')
        return

    community.sync_activity('startup')

####### <--START--> COMMANDS THAT USE THE MAVENSMATE UI ##########

#displays mavensmate ui
class OpenMavensMateUi(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('open-ui', True, body={'args': { 'ui' : True }})

#opens salesforce setup
class OpenSalesforceOrg(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('open-sfdc', True, body={'args': { 'ui' : True }})

    def is_enabled(command):
        return util.is_mm_project()

#opens salesforce setup
class OpenSettings(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('open-settings', True, body={'args': { 'ui' : True }})

#displays new project dialog
class NewProjectCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('new-project', True, body={'args': { 'ui' : True }})

#creates a MavensMate project from an existing directory
class CreateMavensMateProject(sublime_plugin.WindowCommand):
    def run (self, dirs):
        mm.call('new-project-from-existing-directory', False, body={'args': { 'ui': True, 'directory': dirs[0] }})

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

#displays edit project dialog
class EditProjectCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('edit-project', True, body={'args': { 'ui' : True }})

    def is_enabled(command):
        return util.is_mm_project()

#displays unit test dialog
class RunApexUnitTestsCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        active_file = util.get_active_file()
        body = {}
        try:
            if os.path.exists(active_file):
                filename, ext = os.path.splitext(os.path.basename(util.get_active_file()))
                if ext == '.cls':
                    body = {
                        "classes"         : [filename]
                    }
                else:
                    body = {}
            else:
                body = {}
        except:
            body = {}
        body['args'] = { 'ui' : True }
        mm.call('run-tests', True, context=command, body=body)

    def is_enabled(command):
        return util.is_mm_project()

#launches the execute anonymous UI
class ExecuteAnonymousCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('execute-apex', True, body={'args': { 'ui' : True }})

    def is_enabled(command):
        return util.is_mm_project()

#displays deploy dialog
class DeployToServerCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('deploy', True, body={'args': { 'ui' : True }})

    def is_enabled(command):
        return util.is_mm_project()

#displays new apex class dialog
class NewApexClassCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('new-metadata', True, body={'args': { 'ui': True, 'type': 'ApexClass' }})

    def is_enabled(command):
        return util.is_mm_project()

#displays new apex trigger dialog
class NewApexTriggerCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('new-metadata', True, body={'args': { 'ui': True, 'type': 'ApexTrigger' }})

    def is_enabled(command):
        return util.is_mm_project()

#displays new apex page dialog
class NewApexPageCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('new-metadata', False, body={'args': { 'ui': True, 'type': 'ApexPage' }})

    def is_enabled(command):
        return util.is_mm_project()

#displays new apex component dialog
class NewApexComponentCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('new-metadata', True, body={'args': { 'ui': True, 'type': 'ApexComponent' }})

    def is_enabled(command):
        return util.is_mm_project()

#displays new apex component dialog
class NewLightningAppCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('new-lightning-app', True, body={'args': { 'ui' : True }})

    def is_enabled(command):
        return util.is_mm_project()

#displays new apex component dialog
class NewLightningComponentCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('new-lightning-component', True, body={'args': { 'ui' : True }})

    def is_enabled(command):
        return util.is_mm_project()

#displays new apex component dialog
class NewLightningEventCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('new-lightning-event', True, body={'args': { 'ui' : True }})

    def is_enabled(command):
        return util.is_mm_project()

#displays new apex component dialog
class NewLightningInterfaceCommand(sublime_plugin.ApplicationCommand):
    def run(command):
        mm.call('new-lightning-interface', True, body={'args': { 'ui' : True }})

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
        body = {
            "paths"     : files,
            "force"     : True
        }
        mm.call('compile-metadata', context=self.window, body=body)

    def is_enabled(self):
       return util.is_mm_project();

#deploys the currently active file
class ForceCompileFileCommand(sublime_plugin.WindowCommand):
    def run(self, paths=None):
        debug('FORCE COMPILING!')
        if paths == None:
            paths = [util.get_active_file()]
        body = {
            "paths"     : paths,
            "force"     : True
        }
        mm.call('compile-metadata', context=self.window, body=body)

#handles compiling to server on save
class SaveListener(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        settings = sublime.load_settings('mavensmate.sublime-settings')
        if settings.get('mm_compile_on_save') == True and util.is_mm_file() == True:
            body = {
                "paths" : [util.get_active_file()]
            }
            mm.call('compile-metadata', context=view, body=body)

#deploys the currently active file
class CompileActiveFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        body = {
            "paths" : [util.get_active_file()]
        }
        mm.call('compile-metadata', context=self, body=body)

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
            elif ext == '.app' or ext == '.auradoc' or ext == '.cmp':
                if "linux" in sys.platform or "darwin" in sys.platform:
                    view.set_syntax_file(os.path.join("Packages","XML","XML.tmLanguage"))
                else:
                    view.set_syntax_file(os.path.join("Packages/XML/XML.tmLanguage"))
            elif ext == '.log' and ('/debug/' in fn or '\\debug\\' in fn or '\\apex-scripts\\log\\' in fn or '/apex-scripts/log/' in fn):
                if "linux" in sys.platform or "darwin" in sys.platform:
                    view.set_syntax_file(os.path.join("Packages","MavensMate","sublime","lang","MMLog.tmLanguage"))
                else:
                    view.set_syntax_file(os.path.join("Packages/MavensMate/sublime/lang/MMLog.tmLanguage"))
        except:
            pass

class MenuModifier(sublime_plugin.EventListener):
    def on_activated_async(self, view):
        view.file_name()

#compiles the selected files
class CompileSelectedFilesCommand(sublime_plugin.WindowCommand):
    def run (self, files):
        #print files
        body = {
            "paths" : files
        }
        mm.call('compile-metadata', context=self, body=body)

    def is_visible(self, files):
        return util.is_mm_project()

    def is_enabled(self, files):
        if files != None and type(files) is list and len(files) > 0:
            for f in files:
                if util.is_mm_file(f):
                    return True
        return False

class RunAllTestsAsyncCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('run_all_tests', context=self)

    def is_enabled(command):
        return util.is_mm_project()

#runs apex unit tests using the async api
class RunAsyncApexTestsCommand(sublime_plugin.WindowCommand):
    def run(self):
        active_file = util.get_active_file()
        try:
            if os.path.exists(active_file):
                filename, ext = os.path.splitext(os.path.basename(util.get_active_file()))
                if ext == '.cls':
                    body = {
                        "paths" : [filename]
                    }
                else:
                    body = {}
            else:
                body = {}
        except:
            body = {}
        mm.call('run-tests', context=self, body=body, message="Running Apex unit test(s)...")

    def is_enabled(command):
        return util.is_apex_class_file()

#deploys the currently open tabs
class CompileTabsCommand(sublime_plugin.WindowCommand):
    def run (self):
        body = {
            "paths"         : util.get_tab_file_names()
        }
        mm.call('compile-metadata', context=self, body=body)

#replaces local copy of metadata with latest server copies
class CleanProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.ok_cancel_dialog("Are you sure you want to clean this project? All local (non-server) files will be deleted and your project will be refreshed from the server", "Clean"):
            mm.call('clean-project', context=self)

    def is_enabled(command):
        return util.is_mm_project()

class OpenProjectSettingsCommand(sublime_plugin.WindowCommand):
    def run(self):
        path = os.path.join(util.mm_project_directory(),util.get_project_name()+'.sublime-settings')
        sublime.active_window().open_file(path)

    def is_enabled(command):
        return util.is_mm_project()

class RunApexScriptCommand(sublime_plugin.WindowCommand):
    def run(self):
        body = {
            "paths" : [ util.get_active_file() ]
        }
        mm.call('run-apex-script', context=self, body=body, message='Running Apex Script: '+os.path.basename(util.get_active_file()))

    def is_enabled(command):
        try:
            return "apex-scripts" in util.get_active_file() and '.cls' in util.get_active_file()
        except:
            return False

class NewApexScriptCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sublime.active_window().show_input_panel("Apex Script Name", "MyScriptName", self.finish, None, None)

    def finish(self, name):
        mm.call('new-apex-script', False, body={ 'name': name }, message='Creating new Apex Script: '+name)

    def is_enabled(command):
        return util.is_mm_project()

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
                body = {
                    'paths': dirs
                }
            elif files != None and type(files) is list and len(files) > 0:
                body = {
                    'paths': files
                }
            mm.call('refresh-metadata', context=self, body=body)

    def is_visible(self, dirs, files):
        return util.is_mm_project()

#refreshes the currently active file from the server
class RefreshActiveFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.ok_cancel_dialog("Are you sure you want to overwrite this file's contents from Salesforce?", "Refresh"):
            body = {
                'paths': [util.get_active_file()]
            }
            mm.call('refresh-metadata', context=self, body=body)

    def is_visible(self):
        return util.is_mm_file()

#opens the apex class, trigger, component or page on the server
class RunActiveApexTestsCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename, ext = os.path.splitext(os.path.basename(util.get_active_file()))
        body = {
            'classes': [filename]
        }
        mm.call('run-tests', context=self, body=body, message='Running Apex unit test(s)...')

    def is_visible(self):
        return util.is_apex_class_file()

    def is_enabled(self):
        return util.is_apex_test_file()

#opens the apex class, trigger, component or page on the server
class RunSelectedApexTestsCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        if files != None and type(files) is list and len(files) > 0:
            body = {
                'classes': files
            }
            mm.call('run-tests', context=self, body=body, message='Running Apex unit test(s)...')

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
        body = {
            'paths': [util.get_active_file()],
            'callThrough': True
        }
        mm.call('open-metadata', context=self, body=body)

    def is_visible(self):
        return util.is_mm_file()

    def is_enabled(self):
        return util.is_browsable_file()

#opens the apex class, trigger, component or page on the server
class OpenSelectedSfdcUrlCommand(sublime_plugin.WindowCommand):
    def run (self, files):
        if files != None and type(files) is list and len(files) > 0:
            body = {
                'paths': files,
                'callThrough': True
            }
        mm.call('open-metadata', context=self, body=body)

    def is_visible(self, files):
        if not util.is_mm_project: return False
        if files != None and type(files) is list and len(files) > 0:
            for f in files:
                if util.is_browsable_file(f): return True
        return False

#deletes selected metadata
class DeleteMetadataCommand(sublime_plugin.WindowCommand):
    def run(self, dirs, files):
        if dirs != None and len(dirs) > 0:
            if sublime.ok_cancel_dialog("Are you sure you want to delete the selected paths from Salesforce?", "Delete"):
                body = {
                    "paths": dirs
                }
                mm.call('delete-metadata', context=self, body=body)
        else:
            if sublime.ok_cancel_dialog("Are you sure you want to delete the selected files from Salesforce?", "Delete"):
                body = {
                    "paths": files
                }
                mm.call('delete-metadata', context=self, body=body)

    def is_visible(self):
        return util.is_mm_file()

    def is_enabled(self):
        return util.is_mm_file()

#deletes selected metadata
class RefreshProjectApexSymbols(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('index-apex', context=self, message="Refreshing Symbol Tables")

    def is_enabled(self):
        return util.is_mm_project()

#deletes selected metadata
class RefreshApexSymbols(sublime_plugin.WindowCommand):
    def run(self, files):
        if files != None and type(files) is list and len(files) == 1:
            class_names = []
            for f in files:
                class_names.append(os.path.basename(f).replace(".json",".cls"))
            body = {
                "paths" : class_names
            }
            mm.call('index-apex', context=self, body=body, message="Refreshing Symbol Table(s) for selected Apex Classes")

    def is_visible(self, files):
        try:
            if not util.is_mm_project():
                return False

            if files != None and type(files) is list and len(files) == 1:
                for f in files:
                    if os.path.join(util.mm_project_directory(),"src","classes") not in f:
                        return False
                    if "-meta.xml" in f:
                        return False
            elif files != None and type(files) is list and len(files) == 0:
                return False

            return True
        except:
            return False

    def is_enabled(self):
        return util.is_mm_project()

#deletes selected metadata
class DeleteActiveMetadataCommand(sublime_plugin.WindowCommand):
    def run(self):
        active_path = util.get_active_file()
        active_file = os.path.basename(active_path)
        if sublime.ok_cancel_dialog("Are you sure you want to delete "+active_file+" file from Salesforce?", "Delete"):
            body = {
                "paths" : [ active_path ]
            }
            mm.call('delete-metadata', context=self, body=body)
            self.window.run_command("close")

    def is_enabled(self):
        return util.is_mm_file()

    def is_visible(self):
        return util.is_mm_project()

#attempts to compile the entire project
class CompileProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        if sublime.ok_cancel_dialog("Are you sure you want to compile the entire project?", "Compile Project"):
            mm.call('compile-project', context=self)

    def is_enabled(command):
        return util.is_mm_project()

#refreshes the currently active file from the server
class IndexApexFileProperties(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('index-apex', False, context=self)

    def is_enabled(command):
        return util.is_mm_project()

#indexes the meta data based on packages.xml
class IndexMetadataCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('index-metadata', True, context=self)

    def is_enabled(command):
        return util.is_mm_project()

class StartLoggingCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('start-logging', True)

    def is_enabled(self):
        return util.is_mm_project()

class StopLoggingCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('stop-logging', True)

    def is_enabled(self):
        return util.is_mm_project()

class FlushDebugLogsCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('flush-logs', True, message='Flushing local debug logs...')

    def is_enabled(self):
        return util.is_mm_project()

#refreshes the currently active file from the server
class FetchCheckpointsCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('fetch_checkpoints', True)

    def is_enabled(self):
        return util.is_mm_project()

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
            fileName, ext = os.path.splitext(os.path.basename(util.get_active_file()))
            if ext == ".cls" or ext == ".trigger":
                api_name = fileName
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
        fileName, ext = os.path.splitext(os.path.basename(util.get_active_file()))
        if ext == ".cls" or ext == ".trigger":
            self.api_name = fileName
            overlays = util.get_execution_overlays(util.get_active_file())
            for o in overlays:
                options.append(['Line '+str(o["Line"]), str(o["Id"])])
        self.results = options
        self.window.show_quick_panel(options, self.panel_done, sublime.MONOSPACE_FONT)

    def panel_done(self, picked):
        if 0 > picked < len(self.results):
            return
        self.overlay = self.results[picked]
        body = {
            "id" : self.overlay[1]
        }
        mm.call('delete_apex_overlay', context=self, body=body, message="Deleting checkpoint...", callback=self.reload)

    def reload(self, cmd=None):
        debug("Reloading Apex Checkpoints")
        cmd.window.run_command("show_apex_checkpoints")

    def is_enabled(self):
        return util.is_apex_class_file()

#refreshes the currently active file from the server
class IndexApexCheckpointsCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('index_apex_overlays', False, context=self, callback=self.reload)

    def is_enabled(command):
        return util.is_mm_project()

    def reload(self, cmd=None):
        debug("Reloading Apex Checkpoints")
        cmd.window.run_command("show_apex_checkpoints")

#gets apex code coverage for the current class
class GetApexCodeCoverageCommand(sublime_plugin.WindowCommand):
    def run(self):
        body = {
            "paths" : [util.get_active_file()]
        }
        mm.call('get_coverage', True, context=self, message="Retrieving Apex Code Coverage for "+util.get_file_name_no_extension(body["classes"][0]), body=body)

    def is_enabled(command):
        return util.is_apex_class_file()

#gets apex code coverage for the current class
class HideCoverageCommand(sublime_plugin.WindowCommand):
    def run(self):
        util.clear_marked_line_numbers(self.window.active_view(), "no_apex_coverage")

    def is_enabled(command):
        return util.is_apex_class_file()

#refreshes the currently active file from the server
class GetOrgWideTestCoverageCommand(sublime_plugin.WindowCommand):
    def run(self):
        mm.call('get-coverage', True, context=self, body={'global': True}, message="Retrieving org-wide test coverage...")

    def is_enabled(command):
        return util.is_mm_project()

#creates a new overlay
class NewApexCheckpoint(sublime_plugin.WindowCommand):
    def run(self):
        fileName, ext = os.path.splitext(os.path.basename(util.get_active_file()))
        if ext == ".cls" or ext == ".trigger":
            if ext == '.cls':
                self.object_type = 'ApexClass'
            else:
                self.object_type = 'ApexTrigger'
            self.api_name = fileName
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
        body = {
            "ActionScriptType"      : "None",
            "Object_Type"           : self.object_type,
            "API_Name"              : self.api_name,
            "IsDumpingHeap"         : True,
            "Iteration"             : 1,
            "Line"                  : int(self.line_number)
        }
        #util.mark_overlay(self.line_number) #cant do this here bc it removes the rest of them
        mm.call('new_apex_overlay', context=self, body=body, message="Creating new checkpoint at line "+self.line_number+"...", callback=self.reload)

    def reload(self, cmd=None):
        debug("Reloading Apex Checkpoints")
        cmd.window.run_command("show_apex_checkpoints")

    def is_enabled(self):
        return util.is_apex_class_file()

#right click context menu support for resource bundle creation
class NewResourceBundleCommand(sublime_plugin.WindowCommand):
    def run(self, files, dirs):
        if sublime.ok_cancel_dialog("Are you sure you want to create a resource bundle for the selected static resource", "Create Resource Bundle"):
            mm.call('new-resource-bundle', True, context=self, message="Creating resource bundle...", body={ "paths": [ files[0] ] })

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
        static_resource_path = os.path.join(util.mm_project_directory(),"src","staticresources",self.results[picked])
        mm.call('new-resource-bundle', True, body={ "paths" : [ static_resource_path ] }, context=self, message="Creating resource bundle...")

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
        bundle_path = os.path.join(util.mm_project_directory(),"resource-bundles",self.results[picked])
        mm.call('deploy-resource-bundle', True, body={ "paths": [ bundle_path ] }, context=self, message="Deploying resource bundle...")

#right click context menu support for resource bundle refresh
class RefreshResourceBundleCommand(sublime_plugin.WindowCommand):
    def run(self, dirs, files):
        if sublime.ok_cancel_dialog("This command will refresh the resource bundle(s) based on your local project's corresponding static resource(s). Do you wish to continue?", "Refresh"):
            #TODO: cli referesh
            pass

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

#completions for visualforce
class VisualforceCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        #if user has opted out of autocomplete or this isnt a mm project, ignore it
        settings = sublime.load_settings('mavensmate.sublime-settings')
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
        settings = sublime.load_settings('mavensmate.sublime-settings')
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
        #if 'string.quoted.brackets.soql.apex' in scope_name:
        #    return []

        ch = view.substr(sublime.Region(pt, pt + 1))
        if ch == '.' and 'string.quoted.brackets.soql.apex' not in scope_name: return []
        ltr = view.substr(sublime.Region(pt, pt + 2))
        if not ltr.isupper() and 'string.quoted.brackets.soql.apex' not in scope_name: return [] #if not an uppercase letter, ignore

        _completions = []

        if 'string.quoted.brackets.soql.apex' in scope_name:
            return []
            # if ch == '.':
            #     word = view.substr(view.word(pt))
            #     if not word.endswith('__r'):
            #         return []
            #     base_word = word.replace("__r","")
            #     if base_word in util.standard_object_names():
            #         object_name = base_word
            #     else:
            #         object_name = word.replace("__r","__c")
            #     debug("Retrieving field completions for: ",object_name)
            #     return util.get_field_completions(object_name)
            # else:
            #     #debug(view.substr(pt))
            #     #debug(len(view.substr(pt)))
            #     #if view.substr(pt) == " ": #TODO
            #     #    return []
            #     data = view.substr(sublime.Region(0, locations[0]-len(prefix)))
            #     lines = parsehelp.collapse_square_brackets(data).split("\n")
            #     for line in reversed(lines):
            #         stem  = line.split("[")[0]
            #         if "[" in line:
            #             if len(stem.strip()) == 0: continue
            #         words = stem.split()
            #         for word in reversed(words):
            #             if re.match('^[\w-]+$', word) == None:
            #                 continue
            #             vartype = parsehelp.get_var_type(data, word)
            #             if vartype != None:
            #                 object_name = vartype.group(1).strip()
            #                 debug("Retrieving field completions for: ",object_name)
            #                 return util.get_field_completions(object_name)
            #             break
            #         break
            #     return []

        if settings.get('mm_use_org_metadata_for_completions', False):
            if os.path.isfile(os.path.join(util.mm_project_directory(),"config",".org_metadata")): #=> parse org metadata, looking for object names
                jsonData = util.parse_json_from_file(os.path.join(util.mm_project_directory(),"config",".org_metadata"))
                for metadata_type in jsonData:
                    if 'xmlName' in metadata_type and metadata_type['xmlName'] == 'CustomObject':
                        for object_type in metadata_type['children']:
                            _completions.append((object_type['text']+"\t[Sobject Name]", object_type['text']))

        if os.path.isdir(os.path.join(util.mm_project_directory(),"config",".symbols")): #=> get list of classes
            for (dirpath, dirnames, filenames) in os.walk(os.path.join(util.mm_project_directory(),"config",".symbols")):
                for f in filenames:
                    if '-meta.xml' in f: continue
                    class_name = f.replace(".json", "")
                    _completions.append((class_name+"\t[Custom Apex Class]", class_name))
        #debug(apex_system_completions)
        _completions.extend(apex_system_completions)

        return _completions

#completions for force.com-specific use cases
class ApexCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        #if user has opted out of autocomplete or this isnt a mm project, ignore it
        settings = sublime.load_settings('mavensmate.sublime-settings')
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
        debug('data: ')
        debug(data)
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
        clazz = parsehelp.extract_class(data)
        #inheritance = parsehelp.extract_inheritance(data, clazz)

        if symbol_table != None and "innerClasses" in symbol_table and type(symbol_table["innerClasses"] is list and len(symbol_table["innerClasses"]) > 0):
            for ic in symbol_table["innerClasses"]:
                if ic["name"].lower() == typedef_class_lower:
                    _completions = util.get_completions_for_inner_class(ic)
                    return sorted(_completions)

        if os.path.isfile(os.path.join(util.mm_project_directory(),"src","classes",typedef_class+".cls")): #=> apex classes
            _completions = util.get_apex_completions(typedef_class, typedef_class_extra)
            # if inheritance != None:
            #     _inheritance_completions = util.get_apex_completions(inheritance, None)
            #     _final_completions = _completions + _inheritance_completions
            #else:
            _final_completions = _completions
            return sorted(_final_completions)

        # if inheritance != None:
        #     if os.path.isfile(os.path.join(util.mm_project_directory(),"src","classes",inheritance+".cls")): #=> apex classes
        #         _completions = util.get_apex_completions(inheritance, typedef_class)
        #         return sorted(_completions)

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
        elif os.path.isfile(os.path.join(util.mm_project_directory(),"config",".org_metadata")) and settings.get('mm_use_org_metadata_for_completions', False): #=> parse org metadata, looking for object fields
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
                        body = {
                            'metadata_types' : ['CustomObject']
                        }
                        mm.call('refresh_metadata_index', False, body=body)
                except:
                    debug('Failed to index custom object metadata')
            else:
                _completions.append(('Id', 'Id'))
                return (sorted(_completions), completion_flags)
        else:
            return []

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

class ScrubLogCommand(sublime_plugin.WindowCommand):
    def run(self):
        community.sync_activity('scrub_log')
        active_view = self.window.active_view()
        fileName, ext = os.path.splitext(active_view.file_name())

        lines = []
        new_lines = []

        with open(active_view.file_name()) as f:
            lines = f.readlines()

        for file_line in lines:
            if '|USER_DEBUG|' in file_line and '|DEBUG|' in file_line:
                new_lines.append(file_line)
            elif '|EXCEPTION_THROWN|' in file_line or '|FATAL_ERROR|' in file_line:
                new_lines.append(file_line)

        string = "\n".join(new_lines)
        new_view = self.window.new_file()
        if "linux" in sys.platform or "darwin" in sys.platform:
            new_view.set_syntax_file(os.path.join("Packages","MavensMate","sublime","lang","MMLog.tmLanguage"))
        else:
            new_view.set_syntax_file(os.path.join("Packages/MavensMate/sublime/lang/MMLog.tmLanguage"))
        new_view.set_scratch(True)
        new_view.set_name("Scrubbed Log")
        new_view.run_command('generic_text', {'text': string })

    def is_enabled(command):
        try:
            active_view = sublime.active_window().active_view()
            fn, ext = os.path.splitext(active_view.file_name())
            if util.is_mm_project():
                if ext == '.log' and ('/debug/' in fn or '\\debug\\' in fn or '\\apex-scripts\\log\\' in fn or '/apex-scripts/log/' in fn):
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

class ListFieldsForObjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.objects = []
        self.org_metadata = {}
        if os.path.exists(os.path.join(util.mm_project_directory(),"src","objects")): #=> object fields from src directory (more info on field metadata, so is primary)
            for (dirpath, dirnames, filenames) in os.walk(os.path.join(util.mm_project_directory(),"src","objects")):
                for f in filenames:
                    self.objects.append(f.replace(".object",""))

        if self.objects == [] and os.path.isfile(os.path.join(util.mm_project_directory(),"config",".org_metadata")): #=> parse org metadata, looking for object names
            self.org_metadata = util.parse_json_from_file(os.path.join(util.mm_project_directory(),"config",".org_metadata"))
            for metadata_type in self.org_metadata:
                if 'xmlName' in metadata_type and metadata_type['xmlName'] == 'CustomObject':
                    for object_type in metadata_type['children']:
                        self.objects.append(object_type['text'])

        self.window.show_quick_panel(self.objects, self.panel_done,
            sublime.MONOSPACE_FONT)

    def panel_done(self, picked):
        fields = []
        selected_object = self.objects[picked]
        nodes = ['fullName', 'description', 'type', 'label', 'picklist']
        if os.path.isfile(os.path.join(util.mm_project_directory(),"src","objects",selected_object+".object")):
            object_dom = parse(os.path.join(util.mm_project_directory(),"src","objects",selected_object+".object"))
            for node in object_dom.getElementsByTagName('fields'):
                field_name = ''
                field_type = ''
                field_label = ''
                field_description = ''
                field_picklists = ''
                is_picklist = False
                for child in node.childNodes:
                    if child.nodeName not in nodes: continue
                    if child.nodeName == 'fullName':
                        field_name = child.firstChild.nodeValue
                    elif child.nodeName == 'type':
                        field_type = child.firstChild.nodeValue
                    elif child.nodeName == 'label':
                        field_label = child.firstChild.nodeValue
                    elif child.nodeName == 'description':
                        field_description = child.firstChild.nodeValue
                        field_description = field_description.replace("\n"," - ")
                    elif child.nodeName == 'picklist':
                        is_picklist = True
                        pvalues = []
                        for picklist_values_tag in child.childNodes:
                            for tag in picklist_values_tag.childNodes:
                                if tag.nodeName == 'fullName':
                                    pvalues.append(tag.firstChild.nodeValue)
                        field_picklists = '\n      - value: '.join(pvalues)

                if field_label == '':
                    field_label = field_name
                field_string = field_label+":\n   - description: "+field_description+"\n   - api_name: "+field_name+"\n   - field_type: "+field_type
                if is_picklist:
                    field_string += "\n   - picklist:"+field_picklists
                fields.append(field_string)
        elif self.org_metadata != {}:
            for metadata_type in self.org_metadata:
                if 'xmlName' in metadata_type and metadata_type['xmlName'] == 'CustomObject':
                   for object_name in metadata_type['children']:
                       if 'text' in object_name and object_name['text'] == selected_object:
                           for attr in object_name['children']:
                               if 'text' in attr and attr['text'] == 'fields':
                                   for field in attr['children']:
                                       fields.append(field['text'])

        string = "Object_Name: "+selected_object+"\n\n"
        string += "\n".join(fields)
        new_view = self.window.new_file()
        if "linux" in sys.platform or "darwin" in sys.platform:
            new_view.set_syntax_file(os.path.join("Packages","YAML","YAML.tmLanguage"))
        else:
            new_view.set_syntax_file(os.path.join("Packages/YAML/YAML.tmLanguage"))
        new_view.set_scratch(True)
        new_view.set_name("Field List: "+selected_object)
        new_view.run_command('generic_text', {'text': string })

    def is_enabled(command):
        return util.is_mm_project()

#generic handler for writing text to an output panel (sublime text 3 requirement)
class GenericTextCommand(sublime_plugin.TextCommand):
    def run(self, edit, text, *args, **kwargs):
        size = self.view.size()
        self.view.set_read_only(False)
        self.view.insert(edit, size, text)
        #self.view.set_read_only(True)
        self.view.show(size)

    def is_visible(self):
        return False

    def is_enabled(self):
        return True

    def description(self):
        return

class ShowSublimeConsole(sublime_plugin.WindowCommand):
    def run(self):
        sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})
