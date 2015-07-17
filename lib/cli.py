import sublime
import threading
import json
import subprocess
import signal
import os
import sys
import time
# import shutil
import socket
import urllib.request
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
import MavensMate.lib.platform_util as platform_util
import MavensMate.lib.printer as printer

# print(shutil.which('npm'))
# print(shutil.which('node'))

sublime_version = int(float(sublime.version()))
settings = sublime.load_settings('mavensmate.sublime-settings')
debug = config.debug

path_to_port_dict = {}

class MavensMateUiServer(threading.Thread):
    def __init__(self, **kwargs):
        self.settings = sublime.load_settings('mavensmate.sublime-settings')
        self.debug = kwargs.get('debug')
        self.port = kwargs.get('port')
        threading.Thread.__init__(self)

    def run(self):
        if util.mm_project_directory():
            os.chdir(util.mm_project_directory());

        node_path = platform_util.node_path()

        mm_server_executable_setting = self.settings.get('mm_local_server_path')
        if mm_server_executable_setting == 'default':
            mm_local_server_path = os.path.join(sublime.packages_path(),"User","MavensMate","node_modules","mavensmate","bin","server")
        else:
            mm_local_server_path = mm_server_executable_setting

        self.debug('starting MavensMate server on port: '+self.port)

        cmd = [ node_path, mm_local_server_path, '--headless', '--editor', 'sublime', '--port', self.port ]
        if util.mm_project_directory():
            cmd.append('--project')
            cmd.append(util.mm_project_directory())
        self.debug('start server command: ')
        self.debug(cmd)
        # cmd = '/usr/local/bin/node /Users/josephferraro/Development/Github/MavensMate/bin/server --headless -e sublime'
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        global server_pid
        global server_port
        server_pid = process.pid
        server_port = self.port
        self.debug('MavensMate server pid is: '+str(server_pid)) # TODO: kill this process when ST closes
        stdout, stderr = process.communicate()
        self.debug('Server output: ')
        if stdout != None:
            self.debug(stdout)
            # printer.write_to_active_printer(str(stdout))
        elif stderr != None:
            self.debug(stderr)
            message = '\n[OPERATION FAILED]: MavensMate server failed to start: '+str(stderr)
            printer.write_to_active_printer(message)

def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    addr, port = s.getsockname()
    s.close()
    return str(port)

def start_server():
    server_port_defined = 'server_port' in globals()
    if server_port_defined:
        port = server_port
    else:
        port = get_free_port()
    serverThread = MavensMateUiServer(debug=debug, port=port)
    serverThread.daemon = True
    serverThread.start()
    time.sleep(1)

def kill_servers():
    if platform_util.is_windows:
        os.system('taskkill /f /im "mavensmate server - sublime"')
    else:
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if 'mavensmate server - sublime' in str(line):
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

#prepares and submits a threaded call to the mm executable
def call(operation, use_mm_panel=True, **kwargs):
    debug('Calling cli')
    debug('OPERATION: '+operation)
    debug(kwargs)

    if not util.valid_workspace():
        message = '\n[OPERATION FAILED]: Please ensure mm_workspace is set to existing location(s) on your local drive\n'
        printer.write_to_active_printer(message)
        return

    window, view = util.get_window_and_view_based_on_context(kwargs.get('context', None))

    if operation != 'compile-metadata':
        community.sync_activity(operation)

    threads = []
    thread = MavensMateTerminalCall(
        operation,
        active_file=util.get_active_file(),
        body=kwargs.get('body', None),
        context=kwargs.get('context', None),
        message=kwargs.get('message', None),
        use_mm_panel=use_mm_panel,
        process_id=util.get_random_string(10),
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
        self.body           = kwargs.get('body', None)
        self.context        = kwargs.get('context', None)
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
            self.message = command_helper.get_message(self.body, self.operation)

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

        ####### ---> new
        if util.is_mm_project():
            # url = 'http://localhost:8002/execute?command='+self.operation+'&async=1&pid='+util.get_project_settings()['id']
            url = 'http://localhost:'+server_port+'/execute?command='+self.operation+'&async=1&pid='+util.get_project_settings()['id']
        else:
            # url = 'http://localhost:8002/execute?command='+self.operation+'&async=1'
            url = 'http://localhost:'+server_port+'/execute?command='+self.operation+'&async=1'
        debug(url)

        try:
            if self.body != None:
                body = json.dumps(self.body).encode('utf8')
                debug(body)
                req = urllib.request.Request(url, data=body, headers={'content-type': 'application/json'})
                response = urllib.request.urlopen(req)
            else:
                response = urllib.request.urlopen(url)
            mm_response = json.loads(response.read().decode('utf-8'))

            request_id = mm_response['id']
            status = mm_response['status']
            result = None
            while status == 'pending':
                # url = 'http://localhost:8002/status?id='+request_id
                url = 'http://localhost:'+server_port+'/status?id='+request_id
                response = urllib.request.urlopen(url)
                response_body = response.read().decode('utf-8')
                status_response = json.loads(response_body)
                if 'status' in status_response and status_response['status'] == 'pending':
                    time.sleep(0.5)
                else:
                    result = status_response
                    status = 'done'

        except urllib.error.URLError as e:
            result = 'Error contacting MavensMate server: '+str(e)
            response_body = { 'error': 'Request to the local MavensMate server failed. Try restarting the server (MavensMate > Utilities > Restart MavensMate server)' }
            status = 'done'

        debug(result)
        self.result = response_body

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
        sublime.set_timeout(lambda: delete_result_handler(result_handler), 5000)
    except Exception as e:
        raise e

def delete_result_handler(handler):
    del handler
