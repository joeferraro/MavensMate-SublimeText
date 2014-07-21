import urllib.parse
from urllib.parse import urlparse
import sys
import json
sys.path.append('../')
import MavensMate.lib.server.lib.util as util
from MavensMate.lib.server.lib.util import BackgroundWorker
import MavensMate.lib.server.lib.config as gc

# async_request_queue holds list of active async requests
async_request_queue = {}

####################
## ASYNC REQUESTS ##
####################

def project_request(request_handler):
    '''
        POST /project
        {
            "project_name"  : "my project name"
            "username"      : "mm@force.com",
            "password"      : "force",
            "org_type"      : "developer",
            "package"       : {
                "ApexClass"     : "*",
                "ApexTrigger"   : ["Trigger1", "Trigger2"]
            }
        }
    '''
    run_async_operation(request_handler, 'new_project')

def project_existing_request(request_handler):
    '''
        POST /project/existing
        {
            "project_name"  : "my project name"
            "username"      : "mm@force.com",
            "password"      : "force",
            "org_type"      : "developer",
            "directory"     : "/path/to/project",
            "action"        : "existing"
        }
    '''
    run_async_operation(request_handler, 'new_project_from_existing_directory')

def project_edit_request(request_handler):
    '''
        POST /project/edit
        (body same as project_request)
    '''
    run_async_operation(request_handler, 'edit_project')

def project_upgrade_request(request_handler):
    '''
        POST /project/upgrade
        {
            "project_name"  : "my project name"
            "username"      : "mm@force.com",
            "password"      : "force",
            "org_type"      : "developer"
        }
    '''
    run_async_operation(request_handler, 'upgrade_project')

def execute_apex_request(request_handler):
    '''
        POST /apex/execute
        {
            "project_name"    : "my project name"
            "log_level"       : "DEBUG",
            "log_category"    : "APEX_CODE",
            "body"            : "String foo = 'bar';",
        }
    '''
    run_async_operation(request_handler, 'execute_apex')


def deploy_request(request_handler):
    '''
        POST /project/deploy
        call to deploy metadata to a server
        {
            "check_only"            : true,
            "rollback_on_error"     : true,
            "destinations"          : [
                {
                    "username"              : "username1@force.com",
                    "org_type"              : "developer"
                }
            ],
            "package"               : {
                "ApexClass" : "*"
            }
        }
    '''
    run_async_operation(request_handler, 'deploy')

def unit_test_request(request_handler):
    '''
        POST /project/unit_test
        {
            "classes" : [
                "UnitTestClass1", "UnitTestClass2"
            ],
            "run_all_tests" : false
        }
    '''
    gc.debug('in unit test method!')
    run_async_operation(request_handler, 'unit_test')
    
def metadata_index_request(request_handler):
    '''
        call to update the project .metadata index
    '''
    run_async_operation(request_handler, 'index_metadata')

def new_log_request(request_handler):
    '''
        call to create a new debug log
    '''
    run_async_operation(request_handler, 'new_log')

def metadata_list_request_async(request_handler):
    '''
        GET /metadata/list
        {
            "sid"             : "",
            "metadata_type"   : "",
            "murl"            : ""
        }
        call to get a list of metadata of a certain type
    '''
    run_async_operation(request_handler, 'list_metadata')

def generic_endpoint(request_handler):
    request_id = util.generate_request_id()
    params, json_body, plugin_client = get_request_params(request_handler)
    worker_thread = BackgroundWorker(params["command"], params, False, request_id, json_body, plugin_client)
    worker_thread.start()
    worker_thread.join()
    response = worker_thread.response
    respond(request_handler, response)

def generic_async_endpoint(request_handler):
    #params, raw_post_body, plugin_client = get_request_params(request_handler)
    run_async_operation(request_handler, None)


##########################
## SYNCHRONOUS REQUESTS ##
##########################

def get_active_session_request(request_handler):
    '''
        GET /session?username=mm@force.com&password=force&org_type=developer
    '''
    request_id = util.generate_request_id()
    params, json_body, plugin_client = get_request_params(request_handler)
    worker_thread = BackgroundWorker('get_active_session', params, False, request_id, json_body, plugin_client)
    worker_thread.start()
    worker_thread.join()
    response = worker_thread.response
    respond(request_handler, response)

def update_credentials_request(request_handler):
    '''
        POST /project/creds
        {
            "project_name"  : "my project name"
            "username"      : "mm@force.com",
            "password"      : "force",
            "org_type"      : "developer",
        }
        NOTE: project name should not be updated, as it is used to find the project in question
        TODO: maybe we assign a unique ID to each project which will give users the flexibility
              to change the project name??
        TODO: we may need to implement a "clean" flag which will clean the project after creds
              have been updated
    '''
    request_id = util.generate_request_id()
    params, raw_post_body, plugin_client = get_request_params(request_handler)
    worker_thread = BackgroundWorker('update_credentials', params, False, request_id, raw_post_body, plugin_client)
    worker_thread.start()
    worker_thread.join()
    response = worker_thread.response
    respond(request_handler, response)

def project_edit_subscription(request_handler):
    '''
        POST /project/subscription
        {
            "project_name"  : "my project name"
            "subscription"  : ["ApexClass", "ApexPage"]
        }
    '''
    request_id = util.generate_request_id()
    params, raw_post_body, plugin_client = get_request_params(request_handler)
    worker_thread = BackgroundWorker('update_subscription', params, False, request_id, raw_post_body, plugin_client)
    worker_thread.start()
    worker_thread.join()
    response = worker_thread.response
    respond(request_handler, response)


def connections_list_request(request_handler):
    request_id = util.generate_request_id()
    params, raw_post_body, plugin_client = get_request_params(request_handler)
    worker_thread = BackgroundWorker('list_connections', params, False, request_id, raw_post_body, plugin_client)
    worker_thread.start()
    worker_thread.join()
    response = worker_thread.response
    respond(request_handler, response)

def connections_new_request(request_handler):
    request_id = util.generate_request_id()
    params, raw_post_body, plugin_client = get_request_params(request_handler)
    worker_thread = BackgroundWorker('new_connection', params, False, request_id, raw_post_body, plugin_client)
    worker_thread.start()
    worker_thread.join()
    response = worker_thread.response
    respond(request_handler, response)

def connections_delete_request(request_handler):
    request_id = util.generate_request_id()
    params, raw_post_body, plugin_client = get_request_params(request_handler)
    worker_thread = BackgroundWorker('delete_connection', params, False, request_id, raw_post_body, plugin_client)
    worker_thread.start()
    worker_thread.join()
    response = worker_thread.response
    respond(request_handler, response)

def metadata_list_request(request_handler):
    '''
        GET /metadata/list
        {
            "sid"             : "",
            "metadata_type"   : "",
            "murl"            : ""
        }
        call to get a list of metadata of a certain type
    '''
    request_id = util.generate_request_id()
    params, json_body, plugin_client = get_request_params(request_handler)
    worker_thread = BackgroundWorker('list_metadata', params, False, request_id, json_body, plugin_client)
    worker_thread.start()
    worker_thread.join()
    response = worker_thread.response
    respond(request_handler, response)

def get_metadata_index(request_handler):
    '''
        GET /project/get_index
        {
            "project_name"  : "my project name",
            "keyword"       : "mykeyword" //optional
        }
        call to get the metadata index for a project
    '''
    request_id = util.generate_request_id()
    params, json_body, plugin_client = get_request_params(request_handler)
    worker_thread = BackgroundWorker('get_indexed_metadata', params, False, request_id, json_body, plugin_client)
    worker_thread.start()
    worker_thread.join()
    response = worker_thread.response
    respond(request_handler, response) 

def refresh_metadata_index(request_handler):
    '''
        GET /project/get_index/refresh
        {
            "project_name"      : "my project name",
            "metadata_types"    : ["ApexClass"]
        }
        call to refresh a certain type of metadata
    '''
    request_id = util.generate_request_id()
    params, json_body, plugin_client = get_request_params(request_handler)
    worker_thread = BackgroundWorker('refresh_metadata_index', params, False, request_id, json_body, plugin_client)
    worker_thread.start()
    worker_thread.join()
    response = worker_thread.response
    respond(request_handler, response) 

def connect_to_github(request_handler):
    '''
        POST /github/connect
        {
            "username"      : "myusername",
            "password"      : "mypassword"
        }
    '''
    request_id = util.generate_request_id()
    params, json_body, plugin_client = get_request_params(request_handler)
    worker_thread = BackgroundWorker('sign_in_with_github', params, False, request_id, json_body, plugin_client)
    worker_thread.start()
    worker_thread.join()
    response = worker_thread.response
    respond(request_handler, response) 

##########################
## END REQUEST HANDLERS ##
##########################


def run_async_operation(request_handler, operation_name):
    gc.debug('>>> running an async operation')
    request_id = util.generate_request_id()
    params, raw_post_body, plugin_client = get_request_params(request_handler)
    if operation_name == None and "command" in params:
        operation_name = params["command"]
    gc.debug(request_id)
    gc.debug(params)
    gc.debug(raw_post_body)
    
    worker_thread = BackgroundWorker(operation_name, params, True, request_id, raw_post_body, plugin_client)
    gc.debug('worker created')
    worker_thread.start()
    gc.debug('worker thread started')
    async_request_queue[request_id] = worker_thread
    gc.debug('placed into queue')

    return respond_with_async_request_id(request_handler, request_id)

#client polls this servlet to determine whether the request is done
#if the request IS done, it will respond with the body of the request
def status_request(request_handler):
    gc.debug('>>> status request')
    params, json_string, plugin_client = get_request_params(request_handler)
    gc.debug('>>> params: ')
    gc.debug(params)
    try:
        request_id = params['id']
    except:
        request_id = params['id'][0]
    gc.debug('>>> request id: ' + request_id)
    gc.debug('>>> async queue: ')
    gc.debug(async_request_queue)

    if request_id not in async_request_queue:
        response = { 'status' : 'error', 'id' : request_id, 'body' : 'Request ID was not found in async request queue.' }
        response_body = json.dumps(response)
        respond(request_handler, response_body, 'text/json')
    else:
        async_thread = async_request_queue[request_id]
        gc.debug('found thread in request queue, checking if alive')
        gc.debug(async_thread.is_alive())
        if async_thread.is_alive():
            gc.debug('>>> request is not ready')
            respond_with_async_request_id(request_handler, request_id)
        elif async_thread.is_alive() == False:
            gc.debug('>>> request is ready, returning response')
            async_request_queue.pop(request_id, None)
            respond(request_handler, async_thread.response, 'text/json')

def add_to_request_queue(request_id, p, q):
    async_request_queue[request_id] = { 'process' : p, 'queue' : q }

def get_request_params(request_handler):
    #print ('>>>>>> ', request_handler.path)
    #print ('>>>>>> ', request_handler.command)
    #print ('>>>>>> ', request_handler.headers)
    plugin_client = request_handler.headers.get('mm_plugin_client', 'SUBLIME_TEXT_2')
    if request_handler.command == 'POST':
        data_string = request_handler.rfile.read(int(request_handler.headers['Content-Length']))
        #print('>>>>>>> ', data_string)
        postvars = json.loads(data_string.decode('utf-8'))
        if 'package' in postvars:
            postvars['package'] = json.dumps(postvars['package'])
        return postvars, data_string, plugin_client
    elif request_handler.command == 'GET':
        params = urllib.parse.parse_qs(urlparse(request_handler.path).query) 
        #parse_qs(urlparse(request_handler.path).query)
        for key in params:
            if '[]' in key:
                params[key] = params[key]
            else:
                params[key] = params[key][0]
        return_params = {}
        for key in params:
            if '[]' in key:
                return_params[key.replace('[]','')] = params[key]
            else:
                return_params[key] = params[key]       
        json_string = json.dumps(return_params)
        return params, json_string, plugin_client

def process_request_in_background(worker):
    worker.run()




######################
## RESPONSE METHODS ##
######################

#this returns the request id after an initial async request
def respond_with_async_request_id(request_handler, request_id):
    response = { 'status' : 'pending', 'id' : request_id }
    json_response_body = json.dumps(response)
    gc.debug(json_response_body)
    respond(request_handler, json_response_body, 'text/json')

def respond(request_handler, body, type='text/json'):
    request_handler.send_response(200)
    request_handler.send_header('Content-type', type)
    request_handler.send_header('Access-Control-Allow-Origin', '*')
    request_handler.end_headers()
    request_handler.wfile.write(body.encode('utf-8'))
    return



##################
## PATH MAPPING ##
##################

mappings = {
    '/status'                   : { 'GET'   : status_request },     
    '/project'                  : { 'POST'  : project_request }, 
    '/project/edit'             : { 'POST'  : project_edit_request }, 
    '/project/subscription'     : { 'POST'  : project_edit_subscription }, 
    '/project/creds'            : { 'POST'  : update_credentials_request },
    '/project/deploy'           : { 'POST'  : deploy_request },
    '/project/unit_test'        : { 'POST'  : unit_test_request },
    '/project/get_index'        : { 'POST'  : get_metadata_index },
    '/project/refresh_index'    : { 'POST'  : refresh_metadata_index },    
    '/project/index'            : { 'POST'  : metadata_index_request },
    '/project/conns/list'       : { 'GET'   : connections_list_request },
    '/project/conns/new'        : { 'POST'  : connections_new_request },
    '/project/conns/delete'     : { 'POST'  : connections_delete_request },
    '/project/upgrade'          : { 'POST'  : project_upgrade_request },
    '/project/existing'         : { 'POST'  : project_existing_request },
    '/project/new_log'          : { 'POST'  : new_log_request },
    '/session'                  : { 'GET'   : get_active_session_request },
    '/apex/execute'             : { 'POST'  : execute_apex_request },
    '/metadata/list'            : { 'GET'   : metadata_list_request },
    '/metadata/list/async'      : { 'GET'   : metadata_list_request_async },
    '/github/connect'           : { 'POST'  : connect_to_github },
    '/generic'                  : { 'GET'   : generic_endpoint, 'POST' : generic_endpoint },
    '/generic/async'            : { 'GET'   : generic_async_endpoint, 'POST' : generic_async_endpoint }

}
