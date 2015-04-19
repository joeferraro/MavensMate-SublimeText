import sublime
import threading
import json
import subprocess
import os
import sys
import time
import html.parser
import socket
from .threads import ThreadTracker
from .threads import ThreadProgress
from .threads import PanelThreadProgress
from .printer import PanelPrinter
import MavensMate.lib.command_helper as command_helper
from MavensMate.lib.response_handler import MavensMateResponseHandler
from MavensMate.lib.exceptions import *
import MavensMate.util as util
import MavensMate.config as config
import MavensMate.lib.community as community

sublime_version = int(float(sublime.version()))
settings = sublime.load_settings('mavensmate.sublime-settings')
html_parser = html.parser.HTMLParser()
debug = config.debug

path_to_port_dict = {}
server_pids = []

class MavensMateUiServer(threading.Thread):
    def __init__(self, **kwargs):
        self.settings = sublime.load_settings('mavensmate.sublime-settings')
        self.debug = kwargs.get('debug')
        self.port = kwargs.get('port')
        threading.Thread.__init__(self)

    def run(self):
        self.debug('starting ui server!')

        if util.mm_project_directory():
            os.chdir(util.mm_project_directory());

        node_path = self.settings.get('mm_node_path')

        mm_server_executable_setting = self.settings.get('mm_server_executable_path')
        if mm_server_executable_setting == 'default':
            mm_server_executable_path = os.path.join(sublime.packages_path(),"User","MavensMate","node_modules","mavensmate","bin","server")
        else:
            mm_server_executable_path = mm_server_executable_setting

        self.debug('starting ui server on port: '+self.port)

        cmd = [ node_path, mm_server_executable_path, '--headless', '--editor', 'sublime', '--port', self.port ]
        if util.mm_project_directory():
            cmd.append('--project')
            cmd.append(util.mm_project_directory())

        # self.debug(cmd)
        # cmd = '/usr/local/bin/node /Users/josephferraro/Development/Github/MavensMate/bin/server --headless -e sublime'
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        # global child_pid
        child_pid = process.pid
        server_pids.append(child_pid)
        self.debug('Mavensmate UI server pid is: '+str(child_pid)) # TODO: kill this process when ST closes
        stdout, stderr = process.communicate()
        self.debug('MAVENSMATE UI: ')
        self.debug(stdout)
        self.debug(stderr)

def start_ui_server(port):
    serverThread = MavensMateUiServer(debug=debug, port=port)
    serverThread.daemon = True
    serverThread.start()

def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    addr, port = s.getsockname()
    s.close()
    return str(port)

#prepares and submits a threaded call to the mm executable
def call(operation, use_mm_panel=True, **kwargs):
    debug('Calling cli')
    debug('OPERATION: '+operation)
    debug(kwargs)

    settings = sublime.load_settings('mavensmate.sublime-settings')

    # if not os.path.isfile(settings.get('mm_node_path')):
    #     active_window_id = sublime.active_window().id()
    #     printer = PanelPrinter.get(active_window_id)
    #     printer.show()
    #     message = '[OPERATION FAILED]: Could not find Node.js on the local system.'
    #     message += '\n\n1. Ensure Node.js is installed (http://nodejs.org/)'
    #     message += '\n2. Install MavensMate node package (npm install mavensmate -g)'
    #     message += '\n3. In your MavensMate for Sublime Text user settings, set mm_node_path to the location of the Node.Js executable (you can find it on *nix by running \'which node\').'
    #     message += '\n4. In your MavensMate for Sublime Text user settings, set mm_mavensmate_npm_executable_path to the location of the mavensmate executable (you can find it on *nix by running \'which mavensmate\').'
    #     printer.write('\n'+message+'\n')
    #     return

    # if not os.path.isfile(settings.get('mm_mavensmate_npm_executable_path')):
    #     active_window_id = sublime.active_window().id()
    #     printer = PanelPrinter.get(active_window_id)
    #     printer.show()
    #     message = '[OPERATION FAILED]: Could not find the MavensMate executable.'
    #     message += '\n1. Install MavensMate node package (npm install mavensmate -g)'
    #     message += '\n2. In your MavensMate for Sublime Text user settings, set mm_mavensmate_npm_executable_path to the location of the mavensmate executable (you can find it on *nix by running \'which mavensmate\').'
    #     printer.write('\n'+message+'\n')
    #     return

    # if 'linux' in sys.platform:
    #     if not os.path.isfile(settings.get('mm_subl_location')):
    #         active_window_id = sublime.active_window().id()
    #         printer = PanelPrinter.get(active_window_id)
    #         printer.show()
    #         message = '[OPERATION FAILED]: Could not locate Sublime Text "subl" executable. Please set mm_subl_location to location of "subl" on the disk.'
    #         printer.write('\n'+message+'\n')
    #         return

    # if 'win32' in sys.platform:
    #     if not os.path.isfile(settings.get('mm_windows_subl_location')):
    #         active_window_id = sublime.active_window().id()
    #         printer = PanelPrinter.get(active_window_id)
    #         printer.show()
    #         message = '[OPERATION FAILED]: Could not locate Sublime Text. Please set mm_windows_subl_location to location of sublime_text.exe on the disk.'
    #         printer.write('\n'+message+'\n')
    #         return

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
    # if operation != 'new_project' and operation != 'new_project_from_existing_directory' and util.is_project_legacy(window) == True:
    #     operation = 'upgrade_project'

    community.sync_activity(operation)

    threads = []
    thread = MavensMateTerminalCall(
        operation,
        active_file=util.get_active_file(),
        params=kwargs.get('params', None),
        context=kwargs.get('context', None),
        message=kwargs.get('message', None),
        use_mm_panel=use_mm_panel,
        process_id=util.get_random_string(10),
        mm_path=settings.get('mm_path'),
        callback=kwargs.get('callback', None),
        flags=kwargs.get('flags', None)
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
        self.active_file    = kwargs.get('active_file', None)
        self.params         = kwargs.get('params', None)
        self.context        = kwargs.get('context', None)
        self.mm_path        = kwargs.get('mm_path', None)
        self.message        = kwargs.get('message', None)
        self.flags          = kwargs.get('flags', None)
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

    def submit_payload(self, process):
        payload = self.params
        if payload:
            if type(payload) is dict:
                payload = json.dumps(payload)
            debug('writing payload to STDIN:')
            debug(payload)
            try:
                process.stdin.write(payload)
            except:
                process.stdin.write(payload.encode('utf-8'))
        process.stdin.close()

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

        node_path = self.settings.get('mm_node_path')

        mm_executable_setting = self.settings.get('mm_executable_path')
        if mm_executable_setting == 'default':
            mm_executable_path = os.path.join(sublime.packages_path(),"User","MavensMate","node_modules","mavensmate","bin","mavensmate")
        else:
            mm_executable_path = mm_executable_setting

        cmd = [ node_path, mm_executable_path, '--headless', '-e', 'sublime' ]

        if not util.mm_project_directory() in path_to_port_dict:
            free_port = get_free_port()
            path_to_port_dict[util.mm_project_directory()] = free_port
            start_ui_server(free_port)
            cmd.append('--port')
            cmd.append(free_port)
            time.sleep(2)
        else:
            cmd.append('--port')
            cmd.append(path_to_port_dict[ util.mm_project_directory() ])

        cmd.append(self.operation)

        if self.flags != None:
            cmd.extend(self.flags)

        debug('mavensmate command: ')
        debug(cmd)
        debug(util.mm_project_directory())

        os.chdir(util.mm_project_directory());

        if 'linux' in sys.platform or 'darwin' in sys.platform:
            #osx, linux
            # cmd = '/usr/local/bin/node /Users/josephferraro/Development/Github/MavensMate/bin/mavensmate --headless -e sublime compile-metadata';
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        else:
            #windows
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)

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
            "response"       : res,
            "thread"         : thread
        }
        result_handler = MavensMateResponseHandler(context)
        result_handler.execute()
        #del result_handler
        sublime.set_timeout(lambda: delete_result_handler(result_handler), 5000)
    except Exception as e:
        raise e

def delete_result_handler(handler):
    del handler

def compile_callback(thread, response):
    try:
        result = json.loads(response['result'])
        if 'success' in result and result['success'] == True:
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
            "paths" : thread.params.get('files', [])
        }
        call('index-apex', False, params=params)
