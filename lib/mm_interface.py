import sublime
import threading
import json
import pipes 
import subprocess
import os
import sys
import time
try:
    from .threads import ThreadTracker
    from .threads import ThreadProgress
    from .threads import PanelThreadProgress
    from .printer import PanelPrinter
    import MavensMate.lib.command_helper as command_helper
    import MavensMate.util as util
except:
    from lib.threads import ThreadTracker
    from lib.threads import ThreadProgress
    from lib.threads import PanelThreadProgress
    from lib.printer import PanelPrinter
    import lib.command_helper as command_helper
    import util

sublime_version = int(float(sublime.version()))
settings = sublime.load_settings('mavensmate.sublime-settings')

#prepares and submits a threaded call to the mm executable
def call(operation, use_mm_panel=True, **kwargs):
    settings = sublime.load_settings('mavensmate.sublime-settings')
    
    #if the mm tool is missing, we can't do anything
    if not os.path.exists(settings.get('mm_location')) and settings.get('mm_development_mode') == False:
        active_window_id = sublime.active_window().id()
        printer = PanelPrinter.get(active_window_id)
        printer.show()
        message = '[OPERATION FAILED]: Could not find MavensMate.app. Download MavensMate.app from http://www.joe-ferraro.com/mavensmate/MavensMate.app and place in /Applications. Also, please ensure mm_app_location and mm_location are set properly in Sublime Text (MavensMate --> Settings --> User)'
        printer.write('\n'+message+'\n')
        return

    #if it's a legacy project, need to intercept the call and open the upgrade ui
    #TODO: this should probably be handled in mm
    if operation != 'new_project' and operation != 'new_project_from_existing_directory' and util.is_project_legacy() == True:
        operation = 'upgrade_project'
    
    threads = []
    thread = MavensMateTerminalCall(
        operation, 
        project_name=util.get_project_name(), 
        active_file=util.get_active_file(), 
        params=kwargs.get('params', None),
        context=kwargs.get('context', None),
        message=kwargs.get('message', None),
        use_mm_panel=use_mm_panel,
        process_id=util.get_random_string(10),
        mm_location=settings.get('mm_location')
    )
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
        self.mm_location    = kwargs.get('mm_location', None)
        self.message        = kwargs.get('message', None)
        self.view           = None
        self.window         = None
        self.printer        = None
        self.process_id     = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        self.use_mm_panel   = kwargs.get('use_mm_panel', False)
        self.result         = None #result of operation
        self.callback       = None
        self.window_id      = None
        self.status_region  = None
        #if self.params != None:
        #    self.callback   = self.params.get('callback', None)
        self.callback = handle_result

        self.settings = sublime.load_settings('mavensmate.sublime-settings')
        self.define_sublime_context()
        self.printer = PanelPrinter.get(self.window.id())

        if self.message == None:
            self.message = command_helper.get_message(self.params, self.operation)
        
        if self.use_mm_panel:
            self.printer.show()
            self.printer.writeln(' ')
            self.printer.writeln('==============================================')
            self.printer.writeln(self.message)
            self.printer.writeln('Timestamp: '+self.process_id)
            self.printer.writeln('Result:          ')
        else:
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
        if sublime_version >= 3000:
            args['-c'] = 'SUBLIME_TEXT_3'
        else:
            args['-c'] = 'SUBLIME_TEXT_2'
        ui_operations = ['edit_project', 'new_project', 'unit_test', 'deploy', 'execute_apex', 'upgrade_project', 'new_project_from_existing_directory']
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
                'api_name'                      : self.params.get('metadata_name', None),
                'metadata_type'                 : self.params.get('metadata_type', None),
                'apex_trigger_object_api_name'  : self.params.get('object_api_name', None),
                'apex_class_type'               : self.params.get('apex_class_type', None)
            }
        elif o == 'new_project_from_existing_directory':
            # no project name
            payload = self.params
        else:

            params = {
                'selected': [
                    'unit_test',
                    'deploy'
                ],
                'files': [
                    'compile',
                    'synchronize',
                    'refresh',
                    'refresh_properties',
                    'open_sfdc_url',
                    'delete'
                ],
                'directories': [
                    'refresh',
                    'synchronize',
                    'refresh_properties'
                ],
                'type': [
                    'open_sfdc_url'
                ]
            }

            # common parameters
            if o == 'new_apex_overlay' or o == 'delete_apex_overlay':
                payload = self.params
            else:
                payload = {}

            payload['project_name'] = self.project_name

            #selected files
            if o in params['files']:
                payload['files'] = self.params.get('files', [])
            #directories
            if o in params['directories']: 
                payload['directories'] = self.params.get('directories', [])
            #selected metadata
            if o in params['selected']:
                if self.params != None:
                    payload['selected'] = self.params.get('selected', [])
            #open type
            if o in params['type']:
                payload['type'] = self.params.get('type', 'edit')

        if type(payload) is dict:
            payload = json.dumps(payload)  
        print(payload)  
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
        self.status_region = self.printer.panel.find('Result:',process_region.begin())

    def run(self):
        if self.use_mm_panel:
            if sys.version_info >= (3, 0):
                self.calculate_process_region()
            PanelThreadProgress(self)

        last_thread = ThreadTracker.get_last_added(self.window)
        ThreadTracker.add(self)
        if last_thread != None:
            last_thread.join()

        #mm_location = self.settings.get('mm_location')

        print('[MAVENSMATE] executing mm terminal call:')
        print("{0} {1}".format(pipes.quote(self.mm_location), self.get_arguments()))
        
        process = subprocess.Popen("{0} {1}".format(self.mm_location, self.get_arguments()), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        #process = subprocess.Popen("{0} {1}".format(pipes.quote(mm_location), self.get_arguments()), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        #process = subprocess.Popen("/Users/josephferraro/Development/joey2/bin/python /Users/josephferraro/Development/Python/mavensmate/mm/mm.py {0}".format(self.get_arguments()), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
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

        print('[MAVENSMATE] response from mm: ' + response_body)
        self.result = response_body
        if self.operation == 'compile':
            compile_callback(self, response_body)
        if self.operation == 'new_apex_overlay' or self.operation == 'delete_apex_overlay':
            sublime.set_timeout(lambda : index_overlays(self.window), 100)
        #if self.callback != None:
        #    print(self.callback)
        #    self.callback(response_body)

        # result = {
        #     "body"      : response_body,
        #     "operation" : self.operation,
        #     "window"    : self.window,
        #     "view"      : self.view
        # }
        if sys.version_info >= (3, 0):
            self.calculate_process_region()
        #else:
        #    sublime.set_timeout(self.calculate_process_region(), 10)
        ThreadTracker.remove(self)

#handles the result of the mm script
def handle_result(operation, process_id, printer, result, thread):
    #print(thread.process_id)
    #print(thread.params)
    process_region = printer.panel.find(process_id,0)
    status_region = printer.panel.find('Result:',process_region.begin())

    try:
        result = json.loads(result)
        if operation == 'compile' and 'conflict' in result and util.to_bool(result['conflict']) == True:
            if sublime.ok_cancel_dialog(result["problem"], "That's OK, overwrite the server copy."):
                printer.write('\n[MAVENSMATE]: Overwriting server copy')
                thread.params['override'] = True
                sublime.set_timeout(lambda: call('compile', params=thread.params), 100)
            else:
                printer.write('\n[MAVENSMATE]: Operation canceled.')
        else:
            print_result_message(operation, process_id, status_region, result, printer, thread) 
            if operation == 'new_metadata' and 'success' in result and util.to_bool(result['success']) == True:
                if 'messages' in result:
                    if type(result['messages']) is not list:
                        result['messages'] = [result['messages']]
                    for m in result['messages']:
                        if 'package.xml' not in m['fileName']:
                            file_name = m['fileName']
                            location = util.mm_project_directory() + "/" + file_name.replace('unpackaged/', 'src/')
                            sublime.active_window().open_file(location)
                            break
            if 'success' in result and util.to_bool(result['success']) == True:
                if printer != None and len(ThreadTracker.get_pending_mm_panel_threads(thread.window)) == 0:
                    printer.hide()  
            elif 'State' in result and result['State'] == 'Completed' and len(ThreadTracker.get_pending_mm_panel_threads(thread.window)) == 0:
                #tooling api
                if printer != None:
                    printer.hide()
            if operation == 'refresh':            
                sublime.set_timeout(lambda: sublime.active_window().active_view().run_command('revert'), 200)
                util.clear_marked_line_numbers()
    except AttributeError:   
        if printer != None:
            printer.write('\n[RESPONSE FROM MAVENSMATE]: '+result+'\n')
            msg = ' [OPERATION FAILED]: Whoops, unable to parse the response. Please report this issue at https://github.com/joeferraro/MavensMate-SublimeText\n'
            msg += '[RESPONSE FROM MAVENSMATE]: '+result
            printer.panel.run_command('write_operation_status', {'text': msg, 'region': [status_region.end(), status_region.end()+10] })
    except Exception:
        if printer != None:
            printer.write('\n[RESPONSE FROM MAVENSMATE]: '+result+'\n')
            msg = ' [OPERATION FAILED]: Whoops, unable to parse the response. Please report this issue at https://github.com/joeferraro/MavensMate-SublimeText\n'
            msg += '[RESPONSE FROM MAVENSMATE]: '+result
            printer.panel.run_command('write_operation_status', {'text': msg, 'region': [status_region.end(), status_region.end()+10] })

#prints the result of the mm operation, can be a string or a dict
def print_result_message(operation, process_id, status_region, res, printer, thread):
    if 'State' in res and res['State'] == 'Failed' and 'CompilerErrors' in res:
        #here we're parsing a response from the tooling endpoint
        errors = json.loads(res['CompilerErrors'])
        if type(errors) is not list:
            errors = [errors]
        for e in errors:
            line_col = ""
            line, col = 1, 1
            if 'line' in e:
                line = int(e['line'])
                line_col = ' (Line: '+str(line)
                util.mark_line_numbers(thread.view, [line], "bookmark")
            if 'column' in e:
                col = int(e['column'])
                line_col += ', Column: '+str(col)
            if len(line_col):
                line_col += ')'

            #scroll to the line and column of the exception
            #if settings.get('mm_compile_scroll_to_error', True):
            #open file, if already open it will bring it to focus
            #view = sublime.active_window().open_file(thread.active_file)
            view = thread.view
            pt = view.text_point(line-1, col-1)
            view.sel().clear()
            view.sel().add(sublime.Region(pt))
            view.show(pt)

            printer.panel.run_command('write_operation_status', {'text': ' [COMPILE FAILED]: ' + e['problem'] + line_col, 'region': [status_region.end(), status_region.end()+10] })
        

    elif 'success' in res and util.to_bool(res['success']) == False and 'messages' in res:
        #here we're parsing a response from the metadata endpoint
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
        else:
            msg = res['messages']
        if msg != None:
            if 'lineNumber' in msg:
                line_col = ' (Line: '+msg['lineNumber']
                util.mark_line_numbers(thread.view, [int(float(msg['lineNumber']))], "bookmark")
            if 'columnNumber' in msg:
                line_col += ', Column: '+msg['columnNumber']
            if len(line_col) > 0:
                line_col += ')'
            printer.panel.run_command('write_operation_status', {'text': ' [DEPLOYMENT FAILED]: ' + msg['fileName'] + ': ' + msg['problem'] + line_col, 'region': [status_region.end(), status_region.end()+10] })
        elif failures != None:
            msg = ' [DEPLOYMENT FAILED]:'
            for f in failures: 
                msg += f['name'] + ', ' + f['methodName'] + ': ' + f['message'] + '\n'
            printer.panel.run_command('write_operation_status', {'text': msg, 'region': [status_region.end(), status_region.end()+10] })
    elif 'success' in res and res["success"] == False and 'line' in res:
        #this is a response from the apex compile api
        line_col = ""
        line, col = 1, 1
        if 'line' in res:
            line = int(res['line'])
            line_col = ' (Line: '+str(line)
            util.mark_line_numbers(thread.view, [line], "bookmark")
        if 'column' in res:
            col = int(res['column'])
            line_col += ', Column: '+str(col)
        if len(line_col):
            line_col += ')'

        #scroll to the line and column of the exception
        if settings.get('mm_compile_scroll_to_error', True):
            #open file, if already open it will bring it to focus
            #view = sublime.active_window().open_file(thread.active_file)
            view = thread.view
            pt = view.text_point(line-1, col-1)
            view.sel().clear()
            view.sel().add(sublime.Region(pt))
            view.show(pt)

        printer.panel.run_command('write_operation_status', {'text': ' [COMPILE FAILED]: ' + res['problem'] + line_col, 'region': [status_region.end(), status_region.end()+10] })
    elif 'success' in res and util.to_bool(res['success']) == True and 'Messages' in res and len(res['Messages']) > 0:
        msg = ' [Operation completed Successfully - With Compile Errors]\n'
        msg += '[COMPILE ERRORS] - Count:\n'
        for m in res['Messages']:
            msg += ' FileName: ' + m['fileName'] + ': ' + m['problem'] + 'Line: ' + m['lineNumber']
        printer.panel.run_command('write_operation_status', {'text': msg, 'region': [status_region.end(), status_region.end()+10] })
    elif 'success' in res and util.to_bool(res['success']) == True:
        printer.panel.run_command('write_operation_status', {'text': ' Success', 'region': [status_region.end(), status_region.end()+10] })
    elif 'success' in res and util.to_bool(res['success']) == False and 'body' in res:
        printer.panel.run_command('write_operation_status', {'text': ' [OPERATION FAILED]:' + res['body'], 'region': [status_region.end(), status_region.end()+10] })
    elif 'success' in res and util.to_bool(res['success']) == False:
        printer.panel.run_command('write_operation_status', {'text': ' [OPERATION FAILED]', 'region': [status_region.end(), status_region.end()+10] })
    else:
        printer.panel.run_command('write_operation_status', {'text': ' Success', 'region': [status_region.end(), status_region.end()+10] })

def compile_callback(thread, result):
    try:
        result = json.loads(result)
        if 'success' in result and result['success'] == True:
            util.clear_marked_line_numbers(thread.view)
            #if settings.get('mm_autocomplete') == True: 
            sublime.set_timeout(lambda: index_apex_code(thread.window), 100)
        elif 'State' in result and result['State'] == 'Completed':
            util.clear_marked_line_numbers(thread.view)
            #if settings.get('mm_autocomplete') == True: 
            sublime.set_timeout(lambda: index_apex_code(thread.window), 100)
    except BaseException as e:
        print('[MAVENSMATE] Issue handling compile result')
        print(e.message) 

def index_overlays(window):
    pending_threads = ThreadTracker.get_pending(window)
    run_index_thread = True
    for t in pending_threads:
        if t.operation == 'index_apex_overlays':
            run_index_thread = False
            break
    if run_index_thread:
        call('index_apex_overlays', False)

def index_apex_code(window):
    pending_threads = ThreadTracker.get_pending(window)
    run_index_thread = True
    for t in pending_threads:
        if t.operation == 'index_apex':
            run_index_thread = False
            break
    if run_index_thread:
        call('index_apex', False)   


