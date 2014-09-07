import sublime
import threading
import json
import pipes 
import subprocess
import os
import sys
import time
import html.parser
import re
from .threads import ThreadTracker
from .threads import ThreadProgress
from .threads import PanelThreadProgress
from .printer import PanelPrinter
from .mm_merge import MavensMateDiffThread
import MavensMate.lib.command_helper as command_helper
from MavensMate.lib.mm_response_handlers import MMResultHandler
from MavensMate.lib.exceptions import *
import MavensMate.util as util
import MavensMate.config as config
import MavensMate.lib.community as community
import shutil

sublime_version = int(float(sublime.version()))
settings = sublime.load_settings('mavensmate.sublime-settings')
html_parser = html.parser.HTMLParser()
debug = config.debug

#prepares and submits a threaded call to the mm executable
def call(operation, use_mm_panel=True, **kwargs):
    debug('Calling mm_interface')
    debug('OPERATION: '+operation)
    debug(kwargs)

    settings = sublime.load_settings('mavensmate.sublime-settings')
    
    if settings.get("mm_developer_mode", False) and not os.path.isfile(settings.get("mm_python_location")):
        active_window_id = sublime.active_window().id()
        printer = PanelPrinter.get(active_window_id)
        printer.show()
        message = '[OPERATION FAILED]: mm_developer_mode is set to true, but we could not find your system python install. Please set the location at mm_python_location'
        printer.write('\n'+message+'\n')
        return
    else:
        if settings.get('mm_path', 'default') != 'default' and not os.path.isfile(settings.get('mm_path')):
            active_window_id = sublime.active_window().id()
            printer = PanelPrinter.get(active_window_id)
            printer.show()
            message = '[OPERATION FAILED]: Could not find the mm executable. If you wish to use the default location, ensure your mm_path setting is set to "default", then run MavensMate > Install/Update MavensMate API (mm). If you wish to run mm from a different location, ensure mm_path is pointed to that location on your local drive.'
            printer.write('\n'+message+'\n')
            return

        if sys.platform == 'linux' or sys.platform == 'darwin':
            if settings.get('mm_path', 'default') == 'default' and not os.path.isfile(os.path.join(sublime.packages_path(),"User","MavensMate","mm","mm")):
                active_window_id = sublime.active_window().id()
                printer = PanelPrinter.get(active_window_id)
                printer.show()
                message = '[OPERATION FAILED]: Could not find the mm executable. Please run MavensMate > Install/Update MavensMate API (mm) to install mm to your MavensMate for Sublime Text plugin directory.'
                printer.write('\n'+message+'\n')
                return
        else:
            if settings.get('mm_path', 'default') == 'default' and not os.path.isfile(os.path.join(sublime.packages_path(),"User","MavensMate","mm","mm.exe")):
                active_window_id = sublime.active_window().id()
                printer = PanelPrinter.get(active_window_id)
                printer.show()
                message = '[OPERATION FAILED]: Could not find the mm executable. Please run MavensMate > Install/Update MavensMate API (mm) to install mm to your MavensMate for Sublime Text plugin directory.'
                printer.write('\n'+message+'\n')
                return 

    if 'linux' in sys.platform:
        if not os.path.isfile(settings.get('mm_subl_location')):
            active_window_id = sublime.active_window().id()
            printer = PanelPrinter.get(active_window_id)
            printer.show()
            message = '[OPERATION FAILED]: Could not locate Sublime Text "subl" executable. Please set mm_subl_location to location of "subl" on the disk.'
            printer.write('\n'+message+'\n')
            return

    if 'win32' in sys.platform:
        if not os.path.isfile(settings.get('mm_windows_subl_location')):
            active_window_id = sublime.active_window().id()
            printer = PanelPrinter.get(active_window_id)
            printer.show()
            message = '[OPERATION FAILED]: Could not locate Sublime Text. Please set mm_windows_subl_location to location of sublime_text.exe on the disk.'
            printer.write('\n'+message+'\n')
            return

    if not util.valid_workspace():
        active_window_id = sublime.active_window().id()
        printer = PanelPrinter.get(active_window_id)
        printer.show()
        message = '[OPERATION FAILED]: Please ensure mm_workspace is set to existing location(s) on your local drive'
        printer.write('\n'+message+'\n')
        return

    window, view = util.get_window_and_view_based_on_context(kwargs.get('context', None))

    #if it's a legacy project, need to intercept the call and open the upgrade ui
    #TODO: this should probably be handled in mm
    if operation != 'new_project' and operation != 'new_project_from_existing_directory' and util.is_project_legacy(window) == True:
        operation = 'upgrade_project'
    
    community.sync_activity(operation)

    threads = []
    thread = MavensMateTerminalCall(
        operation, 
        project_name=util.get_project_name(window), 
        active_file=util.get_active_file(), 
        params=kwargs.get('params', None),
        context=kwargs.get('context', None),
        message=kwargs.get('message', None),
        use_mm_panel=use_mm_panel,
        process_id=util.get_random_string(10),
        mm_path=settings.get('mm_path'),
        callback=kwargs.get('callback', None)
    )
    if operation == 'index_apex':
        thread.daemon = True
    threads.append(thread)        
    thread.start()

#thread that calls out to the mm tool
#pushes to background threads and reads the piped response
class MavensMateTerminalCall(threading.Thread):
    def __init__(self, operation, **kwargs):
        self.operation      = operation #operation being requested
        self.project_name   = kwargs.get('project_name', None)
        self.active_file    = kwargs.get('active_file', None)
        self.params         = kwargs.get('params', None)
        self.context        = kwargs.get('context', None)
        self.mm_path    = kwargs.get('mm_path', None)
        self.message        = kwargs.get('message', None)
        self.view           = None
        self.window         = None
        self.printer        = None
        self.process_id     = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        self.use_mm_panel   = kwargs.get('use_mm_panel', False)
        self.result         = None #result of operation
        self.callback       = handle_result
        self.alt_callback   = kwargs.get('callback', None) #this is a callback requested by a command
        self.window_id      = None
        self.status_region  = None

        self.settings = sublime.load_settings('mavensmate.sublime-settings')
        self.define_sublime_context()
        self.printer = PanelPrinter.get(self.window.id())

        if self.message == None:
            self.message = command_helper.get_message(self.params, self.operation)
        
        if self.project_name == None:
            self.project_name = util.get_project_name(self.window)

        if self.use_mm_panel:
            self.printer.show()
            self.printer.writeln(' ')
            self.printer.writeln('                                                                          ')
            self.printer.writeln('Operation: '+self.message)
            self.printer.writeln('Timestamp: '+self.process_id)
            self.printer.writeln('   Result:           ')
        elif 'index' not in self.operation:
            ThreadProgress(self, self.message, 'Operation complete')

        threading.Thread.__init__(self)

    #ensures the thread has proper context (related to a specific window and/or view)
    def define_sublime_context(self):
        try:
            if isinstance(self.context, sublime.View):
                self.view = self.context
                self.window = self.view.window()
            elif isinstance(self.context, sublime.Window):
                self.window = self.context
                self.view = self.window.active_view()
            else:
                self.window = sublime.active_window()
                self.view = self.window.active_view() 
        except:
            self.window = sublime.active_window()
            self.view = self.window.active_view()

    def get_arguments(self, ui=False, html=False):
        args = {
            '-o'        : self.operation,
            '--html'    : html
        }
        if self.settings.get('mm_verbose', False):
            args['--verbose'] = True
        if sublime_version >= 3000:
            args['-c'] = 'SUBLIME_TEXT_3'
        else:
            args['-c'] = 'SUBLIME_TEXT_2'
        ui_operations = [
            'edit_project', 
            'new_project', 
            'unit_test', 
            'deploy', 
            'execute_apex', 
            'upgrade_project', 
            'new_project_from_existing_directory', 
            'debug_log', 
            'project_health_check',
            'github'
        ]
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

    def submit_payload(self, process):
        o = self.operation
        
        if o == 'new_metadata':
            # unique payload parameters
            payload = {
                'project_name'                  : self.project_name,
                'metadata_type'                 : self.params.get('metadata_type', None),
                'github_template'               : self.params.get('github_template', None),
                'params'                        : self.params.get('params', [])
            }
            workspace = util.get_project_settings().get("workspace")
            if workspace != None:
                payload['workspace'] = util.get_project_settings().get("workspace")
            else:
                payload['workspace'] = os.path.dirname(util.mm_project_directory())
        else:
            payload = {}
            
            if o != 'new_project' and o != 'new_project_from_existing_directory':
                payload['project_name'] = self.project_name
                workspace = util.get_project_settings().get("workspace")
                if workspace != None:
                    payload['workspace'] = util.get_project_settings().get("workspace")
                else:
                    payload['workspace'] = os.path.dirname(util.mm_project_directory())
        
            #open type
            if o == 'open_sfdc_url':
                payload['type'] = self.params.get('type', 'edit')
            
            if o == 'run_apex_script':
                payload['script_name'] = self.params.get('script_name', None)
                payload['return_log'] = False

            ##catch all
            if self.params != None:
                for key in self.params:
                    if key not in payload:
                        payload[key] = self.params[key]
                
        #debug('>>>>>> ',payload)    

        if type(payload) is dict:
            payload = json.dumps(payload)  
        debug(payload)  
        try:
            process.stdin.write(payload)
        except:
            process.stdin.write(payload.encode('utf-8'))
        process.stdin.close()

    def kill(self):
        #TODO: need to do some cleanup here
        ThreadTracker.set_current(self.window_id, None)

    def calculate_process_region(self):
        process_region = self.printer.panel.find(self.process_id,0)
        self.status_region = self.printer.panel.find('   Result: ',process_region.begin())

    def run(self):
        if self.use_mm_panel:
            if sys.version_info >= (3, 0):
                self.calculate_process_region()
            PanelThreadProgress(self)

        #last_thread = ThreadTracker.get_last_added(self.window)
        ThreadTracker.add(self)

        # if user wishes to run mm.py via python install, ensure mm_python_location and mm_mm_py_location are set
        if self.settings.get('mm_developer_mode', False): 
            python_path = self.settings.get('mm_python_location')
            mm_mm_py_location = self.settings.get('mm_mm_py_location')

            debug('mm.py command: ')
            debug('"{0}" "{1}" {2}'.format(python_path, mm_mm_py_location, self.get_arguments()))

            if 'linux' in sys.platform or 'darwin' in sys.platform:
                #osx, linux
                process = subprocess.Popen('\'{0}\' \'{1}\' {2}'.format(python_path, mm_mm_py_location, self.get_arguments()), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            else:
                #windows
                process = subprocess.Popen('"{0}" "{1}" {2}'.format(python_path, mm_mm_py_location, self.get_arguments()), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        else: # otherwise, run mm executable normally
            if self.mm_path == 'default': #default location is in plugin root 'mm' directory
                if sys.platform == 'linux' or sys.platform == 'darwin':
                    self.mm_path = os.path.join(sublime.packages_path(),"User","MavensMate","mm","mm")
                else:
                    self.mm_path = os.path.join(sublime.packages_path(),"User","MavensMate","mm","mm.exe")
            
            # if 'win32' in sys.platform and '.exe' not in self.mm_path:
            #     self.mm_path = self.mm_path+'.exe'

            if 'linux' in sys.platform or 'darwin' in sys.platform:
                debug('mm command: ')
                debug("{0} {1}".format(pipes.quote(self.mm_path), self.get_arguments()))
                process = subprocess.Popen("{0} {1}".format(pipes.quote(self.mm_path), self.get_arguments()), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            else:
                debug('mm command: ')
                debug('"{0}" {1}'.format(self.mm_path, self.get_arguments()))
                process = subprocess.Popen('"{0}" {1}'.format(self.mm_path, self.get_arguments()), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        self.submit_payload(process)
        if process.stdout is not None: 
            mm_response = process.stdout.readlines()
        elif process.stderr is not None:
            mm_response = process.stderr.readlines()
        try:
            response_body = '\n'.join(mm_response)
        except:
            strs = []
            for line in mm_response:
                strs.append(line.decode('utf-8'))   
            response_body = '\n'.join(strs)

        debug('response from mm: ' + response_body)
        self.result = response_body
        if self.operation == 'compile':
            compile_callback(self, response_body)
        
        self.calculate_process_region()
            
        ThreadTracker.remove(self)

#handles the result of the mm script
def handle_result(operation, process_id, printer, res, thread):
    try:
        context = {
            "operation"      : operation,
            "process_id"     : process_id,
            "printer"        : printer,
            "result"         : res,
            "thread"         : thread
        }
        result_handler = MMResultHandler(context)
        result_handler.execute()
        #del result_handler
        sublime.set_timeout(lambda: delete_result_handler(result_handler), 5000)
    except Exception as e:
        raise e

def delete_result_handler(handler):
    del handler

def compile_callback(thread, result):
    try:
        result = json.loads(result)
        if 'success' in result and result['success'] == True:
            util.clear_marked_line_numbers(thread.view)
            #if settings.get('mm_autocomplete') == True: 
            sublime.set_timeout(lambda: index_apex_code(thread), 100)
        elif 'State' in result and result['State'] == 'Completed':
            util.clear_marked_line_numbers(thread.view)
            #if settings.get('mm_autocomplete') == True: 
            sublime.set_timeout(lambda: index_apex_code(thread), 100)
    except BaseException as e:
        debug('Issue handling compile result in callback')
        debug(e) 

def index_overlays(window):
    pending_threads = ThreadTracker.get_pending(window)
    run_index_thread = True
    for t in pending_threads:
        if t.operation == 'index_apex_overlays':
            run_index_thread = False
            break
    if run_index_thread:
        call('index_apex_overlays', False)

def index_apex_code(thread):
    pending_threads = ThreadTracker.get_pending(thread.window)
    run_index_thread = True
    for t in pending_threads:
        if t.operation == 'index_apex':
            run_index_thread = False
            break
    if run_index_thread:
        params = {
            "files" : thread.params.get('files', [])
        }
        call('index_apex', False, params=params)  
