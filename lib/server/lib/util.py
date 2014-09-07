import os
import sys
import random
import string
import json
import threading
import subprocess
import pipes
import sublime
import MavensMate.lib.server.lib.config as global_config
import MavensMate.config as config

#this function is only used on async requests
def generate_request_id():
    return get_random_string()

def get_random_string(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def generate_error_response(message):
    res = {
        "success"   : False,
        "body_type" : "text",
        "body"      : message
    }
    return json.dumps(res)

#the main job of the backgroundworker is to submit a request for work to be done by mm
class BackgroundWorker(threading.Thread):
    def __init__(self, operation, params, async, request_id=None, payload=None, plugin_client='SUBLIME_TEXT_2'):
        self.operation          = operation
        self.params             = params
        self.request_id         = request_id
        self.async              = async
        self.payload            = payload
        self.plugin_client      = plugin_client
        self.response           = None
        self.settings           = sublime.load_settings('mavensmate.sublime-settings')
        threading.Thread.__init__(self)

    def run(self):
        mm_response = None
        args = self.get_arguments()
        global_config.debug('>>> running thread arguments on next line!')
        global_config.debug(args)
        mm_path = self.settings.get('mm_path')
        if self.settings.get('mm_developer_mode', False): #user wishes to run mm.py via python install
            python_path = self.settings.get('mm_python_location')
            mm_mm_py_location = self.settings.get('mm_mm_py_location')

            if 'linux' in sys.platform or 'darwin' in sys.platform:
                #osx, linux
                process = subprocess.Popen('\'{0}\' \'{1}\' {2}'.format(python_path, mm_mm_py_location, self.get_arguments()), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            else:
                #windows
                process = subprocess.Popen('"{0}" "{1}" {2}'.format(python_path, mm_mm_py_location, self.get_arguments()), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        else: #running mm executable normally
            if mm_path == 'default': #default location is in plugin root 'mm' directory
                if sys.platform == 'linux' or sys.platform == 'darwin':
                    mm_path = os.path.join(sublime.packages_path(),"User","MavensMate","mm","mm")
                else:
                    mm_path = os.path.join(sublime.packages_path(),"User","MavensMate","mm","mm.exe")
            
            if 'linux' in sys.platform or 'darwin' in sys.platform:
                global_config.debug('mm command: ')
                global_config.debug("{0} {1}".format(pipes.quote(mm_path), self.get_arguments()))
                process = subprocess.Popen("{0} {1}".format(pipes.quote(mm_path), self.get_arguments()), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            else: #windows
                global_config.debug('mm command: ')
                global_config.debug('"{0}" {1}'.format(mm_path, self.get_arguments()))
                process = subprocess.Popen('"{0}" {1}'.format(mm_path, self.get_arguments()), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        if self.payload != None and type(self.payload) is str:
            self.payload = self.payload.encode('utf-8')
        process.stdin.write(self.payload)
        process.stdin.close()
        if process.stdout is not None: 
            mm_response = process.stdout.readlines()
        elif process.stderr is not None:
            mm_response = process.stderr.readlines()
        
        #response_body = '\n'.join(mm_response.decode('utf-8'))
        strs = []
        for line in mm_response:
            strs.append(line.decode('utf-8'))   
        response_body = '\n'.join(strs)

        global_config.debug('>>> got a response body')
        global_config.debug(response_body)

        if '--html' not in args:
            try:
                valid_json = json.loads(response_body)
            except:
                response_body = generate_error_response(response_body)

        self.response = response_body
         
    def get_arguments(self):
        args = {}
        args['-o'] = self.operation #new_project, get_active_session
        args['-c'] = self.plugin_client

        if self.operation == 'new_project':
            pass
        elif self.operation == 'checkout_project':
            pass  
        elif self.operation == 'get_active_session':
            pass 
        elif self.operation == 'update_credentials':
            pass
        elif self.operation == 'execute_apex':
            pass
        elif self.operation == 'deploy':
            args['--html'] = None
        elif self.operation == 'unit_test' or self.operation == 'test_async':
            args['--html'] = None
        elif self.operation == 'project_health_check':
            args['--html'] = None    
        #elif self.operation == 'index_metadata':
        #    args['--html'] = None    
                
        arg_string = []
        for x in args.keys():
            if args[x] != None:
                arg_string.append(x + ' ' + args[x] + ' ')
            else:
                arg_string.append(x + ' ')
        stripped_string = ''.join(arg_string).strip()
        return stripped_string