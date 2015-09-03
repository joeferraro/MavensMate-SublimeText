import sublime
import threading
import json
import sys
import time
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

debug = config.debug

def check_server():
    try:
        settings = sublime.load_settings('mavensmate.sublime-settings')
        port_number = settings.get('mm_app_server_port', '56248')
        urllib.request.urlopen('http://localhost:'+str(port_number)+'/app/home/index')
    except urllib.error.URLError as e:
        debug(e)
        raise MMException('Could not contact local MavensMate server, please ensure the MavensMate app is installed and running (https://github.com/joeferraro/mavensmate-app/releases). MavensMate will not run properly until resolved. If you are seeing this message unexpectedly, you may not realize that you are running a prerelease copy of MavensMate for Sublime Text. For more information please visit https://github.com/joeferraro/MavensMate/issues/483#issuecomment-130609793')
    except Exception as e:
        debug(e)
        raise MMException(str(e))

#prepares and submits a threaded call to the mm executable
def call(operation, use_mm_panel=True, **kwargs):
    debug('Calling cli')
    debug('OPERATION: '+operation)
    debug(kwargs)

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
        start_time=time.time(),
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
        self.start_time     = kwargs.get('start_time', time.time())
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

        port_number = self.settings.get('mm_app_server_port', '56248')
        ####### ---> new
        if util.is_mm_project():
            url = 'http://localhost:'+str(port_number)+'/execute?command='+self.operation+'&async=1&pid='+util.get_project_settings()['id']
        else:
            url = 'http://localhost:'+str(port_number)+'/execute?command='+self.operation+'&async=1'
        debug(url)

        try:
            if self.body != None:
                body = json.dumps(self.body).encode('utf8')
                debug('posting to MavensMate:')
                debug(body)
                req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json', 'MavensMate-Editor-Agent': 'sublime'})
                response = urllib.request.urlopen(req)
            else:
                response = urllib.request.urlopen(url)

            debug('response from MavensMate')
            debug(response)

            mm_response = json.loads(response.read().decode('utf-8'))

            request_id = mm_response['id']
            status = mm_response['status']
            result = None
            while status == 'pending':
                url = 'http://localhost:'+str(port_number)+'/status?id='+request_id
                req = urllib.request.Request(url, headers={'MavensMate-Editor-Agent': 'sublime'})

                response = urllib.request.urlopen(url)
                response_body = response.read().decode('utf-8')
                status_response = json.loads(response_body)
                if 'status' in status_response and status_response['status'] == 'pending':
                    time.sleep(0.5)
                else:
                    result = status_response
                    status = 'done'

        except urllib.error.HTTPError as e:
            debug('urllib.error.HTTPError')
            result = e.read().decode('utf-8')
            debug(result)
            result = str(result)
            response_body = { 'error': 'Request to the local MavensMate server failed. '+str(result) }
            status = 'done'
        except urllib.error.URLError as e:
            debug('urllib.error.URLError')
            result = 'Error contacting MavensMate server: '+str(e)
            response_body = { 'error': 'Request to the local MavensMate server failed. please ensure the MavensMate app is running.' }
            status = 'done'
        except Exception as e:
            debug('Exception')
            result = 'Error contacting MavensMate server: '+str(e)
            response_body = { 'error': 'Request to the local MavensMate server failed. '+str(e) }
            status = 'done'


        debug(result)
        self.result = response_body

        self.calculate_process_region()

        ThreadTracker.remove(self)

#handles the result of the mm script
def handle_result(operation, process_id, start_time, printer, res, thread):
    try:
        context = {
            "operation"      : operation,
            "process_id"     : process_id,
            "start_time"      : start_time,
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
