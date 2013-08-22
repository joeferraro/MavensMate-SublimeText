#!/usr/bin/env python

import os.path
import argparse
import inspect
import json
import lib.config as config
import lib.mm_util as util
import urllib
from lib.mm_connection import MavensMatePluginConnection
from lib.mm_client import MavensMateClient
from lib.mm_exceptions import MMException

request_payload = util.get_request_payload()
#config.logger.debug('\n\n\n>>>>>>>>\nhandling request with payload >>>>>')
#config.logger.debug(request_payload)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--operation') #name of the operation being requested
    parser.add_argument('-c', '--client') #name of the plugin client ("SUBLIME_TEXT_2", "SUBLIME_TEXT_3", "TEXTMATE", "NOTEPAD_PLUS_PLUS", "BB_EDIT", etc.)
    parser.add_argument('-p', '--projectname') #name of the project
    parser.add_argument('-d', '--projectdirectory') #name of the project
    parser.add_argument('--callback') #some terminal script to run upon completion of a command
    parser.add_argument('--ui', action='store_true', default=False, 
        dest='ui_switch', help='Include flag to launch the default UI for the operation')
    parser.add_argument('--html', action='store_true', default=False, 
        dest='respond_with_html', help='Include flag if you want the response in HTML')
    args = parser.parse_args()
    operation = args.operation
    
    try:
        setup_connection(args)
    except Exception as e:
        print util.generate_error_response(e.message)
        return

    #if the arg switch argument is included, the request is to launch the out of box
    #MavensMate UI, so we generate the HTML for the UI and launch the process
    #example: mm -o new_project --ui
    if args.ui_switch == True:
        #os.system('killAll MavensMateWindowServer') #TODO: try/except?
        tmp_html_file = util.generate_ui(operation,request_payload)
        util.launch_ui(tmp_html_file)
        print util.generate_success_response('UI Generated Successfully')
    else:        
        requested_function = operation_dict[operation]
        fspec = inspect.getargspec(requested_function)
        if type(fspec.args) is list and len(fspec.args) == 1 and fspec.args[0] == 'args':
            requested_function(eval(fspec.args[0]))
        elif type(fspec.args) is list and len(fspec.args) > 0:
            print util.generate_error_response('Invalid operation requested')
        else:
            requested_function()
        
    if args.callback != None:
        os.system(args.callback)

# each operation sets up a single connection
# the connection holds information about the plugin running it
# and establishes a project object
def setup_connection(args):
    if 'project_name' in request_payload or 'project_directory' in request_payload:
        #project_name        = request_payload.get('project_name', args.projectname)
        #project_directory   = request_payload.get('project_directory', args.projectdirectory)
        config.connection = MavensMatePluginConnection(
            client=args.client or 'SUBLIME_TEXT_3',
            ui=args.ui_switch,
            params=request_payload,
            operation=args.operation)
    else:
        config.connection = MavensMatePluginConnection(
            client=args.client or 'SUBLIME_TEXT_3',
            params=request_payload,
            operation=args.operation)

# echo '{ "username" : "", "password" : "", "metadata_type" : "ApexClass" ' | joey2 mavensmate.py -o 'list_metadata'
def list_metadata():
    if 'sid' in request_payload:
        client = MavensMateClient(credentials={
            "sid"                   : request_payload.get('sid', None),
            "metadata_server_url"   : urllib.unquote(request_payload.get('metadata_server_url', None)),
            "server_url"            : urllib.unquote(request_payload.get('server_url', None)),
        }) 
    elif 'username' in request_payload:
        client = MavensMateClient(credentials={
            "username"              : request_payload.get('username', None),
            "password"              : request_payload.get('password', None)
        })
    print json.dumps(client.list_metadata(request_payload['metadata_type']))

def open_sfdc_url():
    print config.connection.project.open_selected_metadata(request_payload);

def list_connections():
    print config.connection.project.get_org_connections()

def new_connection():
    print config.connection.project.new_org_connection(request_payload)

def delete_connection():
    print config.connection.project.delete_org_connection(request_payload)

def compile_selected_metadata():
    print config.connection.project.compile_selected_metadata(request_payload)

def delete_selected_metadata():
    print config.connection.project.delete_selected_metadata(request_payload)

def index_metadata(args):
    if 'metadata_type' in request_payload:
        index_result = config.connection.project.index_metadata(request_payload['metadata_type'])
    else:
        index_result = config.connection.project.index_metadata()
    if args.respond_with_html == True:
        html = util.generate_html_response(args.operation, index_result, request_payload)
        print util.generate_success_response(html, "html")
    else:
        print util.generate_success_response("Project metadata indexed successfully")

def refresh_metadata_index():
    config.connection.project.index_metadata(request_payload['metadata_types'])
    print util.generate_success_response("Metadata refreshed successfully.")

def get_metadata_index():
    if 'keyword' in request_payload or 'ids' in request_payload:
        print config.connection.project.filter_indexed_metadata(request_payload)
    else:
        #print config.connection.project.get_org_metadata(True, True)
        print config.connection.project.get_org_metadata(True, True)

def new_project():
    print config.connection.new_project(request_payload,action='new')

def new_project_from_existing_directory():
    print config.connection.new_project(request_payload,action='existing')

def edit_project():
    print config.connection.project.edit(request_payload)

def update_subscription():
    print config.connection.project.update_subscription(request_payload)

def upgrade_project():
    print config.connection.project.upgrade()
    
def checkout_project():
    print config.connection.new_project(request_payload,action='checkout')

def compile_project():
    print config.connection.project.compile()

def clean_project():
    print config.connection.project.clean()

def refresh():
    print config.connection.project.refresh_selected_metadata(request_payload)

def refresh_properties():
    config.connection.project.refresh_selected_properties(request_payload)
    print util.generate_success_response("Refreshed Apex file properties.")

def new_metadata():
    print config.connection.project.new_metadata(request_payload)

def execute_apex():
    print config.connection.project.execute_apex(request_payload)

def fetch_checkpoints():
    print config.connection.project.fetch_checkpoints(request_payload)

def fetch_logs():
    print config.connection.project.fetch_logs(request_payload)

def new_trace_flag():
    print config.connection.project.new_trace_flag(request_payload)

def new_quick_trace_flag():
    print config.connection.project.new_quick_trace_flag()

# echo '{ "project_name" : "bloat", "classes" : [ "MyTester" ] }' | joey2 mavensmate.py -o 'test'
def run_unit_tests(args):
    test_result = config.connection.project.run_unit_tests(request_payload)
    if args.respond_with_html ==  True:
        html = util.generate_html_response(args.operation, test_result, request_payload)
        print util.generate_success_response(html, "html")
    else:
        print test_result

def run_async_tests():
    print config.connection.project.sfdc_client.run_async_apex_tests(request_payload)

def deploy_to_server(args):
    deploy_result = config.connection.project.deploy_to_server(request_payload)
    if args.respond_with_html == True:
        html = util.generate_html_response(args.operation, deploy_result, request_payload)
        response = json.loads(util.generate_success_response(html, "html"))
        response['deploy_success'] = True
        # if deployment to one org fails, the entire deploy was not successful
        for result in deploy_result:
            if result['success'] == False:
                response['deploy_success'] = False
                break
        print json.dumps(response)
    else:
        print deploy_result

# echo '{ "username" : "mm@force.com", "password" : "force", "org_type" : "developer" }' | joey2 mavensmate.py -o 'get_active_session'
def get_active_session():
    try:
        if 'username' not in request_payload or request_payload['username'] == None or request_payload['username'] == '':
            raise MMException('Please enter a Salesforce.com username')
        if 'password' not in request_payload or request_payload['password'] == None or request_payload['password'] == '':
            raise MMException('Please enter a Salesforce.com password')
        if 'org_type' not in request_payload or request_payload['org_type'] == None or request_payload['org_type'] == '':
            raise MMException('Please select an org type')

        client = MavensMateClient(credentials={
            "username" : request_payload['username'],
            "password" : request_payload['password'],
            "org_type" : request_payload['org_type']
        }) 
        
        response = {
            "sid"                   : client.sid,
            "user_id"               : client.user_id,
            "metadata_server_url"   : client.metadata_server_url,
            "server_url"            : client.server_url,
            "metadata"              : client.get_org_metadata(subscription=request_payload.get('subscription', None)),
            "success"               : True
        }
        print util.generate_response(response)
    except BaseException, e:
        print util.generate_error_response(e.message)

def index_apex_overlays():
    print config.connection.project.index_apex_overlays(request_payload)

def new_apex_overlay():
    print config.connection.project.new_apex_overlay(request_payload)

def delete_apex_overlay():
    print config.connection.project.delete_apex_overlay(request_payload)

def update_credentials():
    try:
        config.connection.project.username = request_payload['username']
        config.connection.project.password = request_payload['password']
        config.connection.project.org_type = request_payload['org_type']
        config.connection.project.update_credentials()
        print util.generate_success_response('Your credentials were updated successfully')
    except BaseException, e:
        print util.generate_error_response(e.message)

def get_symbol_table():
    print config.connection.project.get_symbol_table(request_payload)

def index_apex_file_properties():
    #print util.generate_error_response("Operation not currently supported")
    print config.connection.project.index_apex_file_properties()

def eval_function():
    python_request = request_payload['python']
    print eval(python_request)

def sign_in_with_github():
    print config.connection.sign_in_with_github(request_payload)

operation_dict = {
    'new_project'                           : new_project,
    'edit_project'                          : edit_project,
    'upgrade_project'                       : upgrade_project,
    'checkout_project'                      : checkout_project,
    'compile_project'                       : compile_project,
    'new_metadata'                          : new_metadata,
    'refresh'                               : refresh,
    'clean_project'                         : clean_project,
    'refresh_properties'                    : refresh_properties,
    'compile'                               : compile_selected_metadata,
    'delete'                                : delete_selected_metadata,
    'get_active_session'                    : get_active_session,
    'update_credentials'                    : update_credentials,
    'execute_apex'                          : execute_apex,
    'deploy_to_server'                      : deploy_to_server,
    'deploy'                                : deploy_to_server,
    'unit_test'                             : run_unit_tests,
    'test'                                  : run_unit_tests,
    'test_async'                            : run_async_tests,
    'list_metadata'                         : list_metadata,
    'index_metadata'                        : index_metadata,
    'refresh_metadata_index'                : refresh_metadata_index,
    'get_indexed_metadata'                  : get_metadata_index,
    'list_connections'                      : list_connections,
    'new_connection'                        : new_connection,
    'delete_connection'                     : delete_connection,
    'index_apex_overlays'                   : index_apex_overlays,
    'new_apex_overlay'                      : new_apex_overlay,
    'delete_apex_overlay'                   : delete_apex_overlay,
    'fetch_logs'                            : fetch_logs,
    'fetch_checkpoints'                     : fetch_checkpoints,
    'new_project_from_existing_directory'   : new_project_from_existing_directory,
    'open_sfdc_url'                         : open_sfdc_url,
    'get_symbols'                           : get_symbol_table,
    'index_apex_file_properties'            : index_apex_file_properties,
    'index_apex'                            : index_apex_file_properties,
    'update_subscription'                   : update_subscription,
    'new_log'                               : new_trace_flag,
    'new_quick_log'                         : new_quick_trace_flag,
    'eval'                                  : eval_function,
    'sign_in_with_github'                   : sign_in_with_github
}

if  __name__ == '__main__':
    main()