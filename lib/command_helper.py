try:
    import MavensMate.util as util
except:
    import util
    
dict = {
    'class'     : ['ApexClass',     'Apex Class'],
    'trigger'   : ['ApexTrigger',   'Apex Trigger'],
    'page'      : ['ApexPage',      'Visualforce Page'],
    'component' : ['ApexComponent', 'Visualforce Component']
}

def get_message(params, operation):
    message = 'Handling requested operation...'
    if operation == 'new_metadata':
        message = 'Creating New '+params['metadata_type']+': ' + params['params']['api_name']
    elif operation == 'synchronize':
        if 'files' in params and len(params['files'])>0:
            kind = params['files'][0]
        elif 'directories' in params and len(params['directories'])>0:
            kind = params['directories'][0]
        else:
            kind = '???'
        message = 'Synchronizing to Server: ' + kind
    elif operation == 'compile':
        if 'files' in params and len(params['files']) == 1:
            what = params['files'][0]
            if '/' in what:
                what = what.split('/')[-1]
            message = 'Compiling: ' + what
        else:
            message = 'Compiling Selected Metadata'
    elif operation == 'compile_project':
        message = 'Compiling Project' 
    elif operation == 'edit_project':
        message = 'Opening Edit Project dialog'  
    elif operation == 'unit_test':
        if 'selected' in params and len(params['selected']) == 1:
            message = "Running Apex Test for " + params['selected'][0]
        else:
            message = 'Opening Apex Test Runner'
    elif operation == 'clean_project':
        message = 'Cleaning Project'
    elif operation == 'deploy':
        message = 'Opening Deploy dialog'
    elif operation == 'execute_apex':
        message = 'Opening Execute Apex dialog'
    elif operation == 'upgrade_project':
        message = 'Your MavensMate project needs to be upgraded. Opening the upgrade UI.'    
    elif operation == 'index_apex_overlays':
        message = 'Indexing Apex Overlays'  
    elif operation == 'index_metadata':
        message = 'Indexing Metadata'  
    elif operation == 'delete':
        if 'files' in params and len(params['files']) == 1:
            what = params['files'][0]
            if '/' in what:
                what = what.split('/')[-1]
            message = 'Deleting: ' + what
        else:
            message = 'Deleting Selected Metadata'
    elif operation == 'refresh':
        if 'files' in params and len(params['files']) == 1:
            what = params['files'][0]
            if '/' in what:
                what = what.split('/')[-1]
            message = 'Refreshing: ' + what
        else:
            message = 'Refreshing Selected Metadata'
    elif operation == 'open_sfdc_url':
        message = 'Opening Selected Metadata'
    elif operation == 'new_apex_overlay':
        message = 'Creating Apex Overlay' 
    elif operation == 'debug_log':
        message = 'Opening trace flag UI (this could take a while...)'
    elif operation == 'delete_apex_overlay':
        message = 'Deleting Apex Overlay'  
    elif operation == 'fetch_logs':
        message = 'Fetching Apex Logs (will be placed in project/debug/logs)'  
    elif operation == 'fetch_checkpoints':
        message = 'Fetching Apex Logs (will be placed in project/debug/checkpoints)'  
    elif operation == 'project_from_existing_directory':
        message = 'Opening New Project Dialog'  
    elif operation == 'index_apex':
        message = 'Indexing Project Apex Metadata'
    elif operation == 'test_async':
        if 'classes' in params and len(params['classes']) == 1:
            what = params['classes'][0]
            if '/' in what:
                what = what.split('/')[-1]
            message = 'Running Apex unit tests for: ' + what
        else:
            message = 'Running Apex unit tests for this class...'
    elif operation == 'new_quick_log':
        message = 'Setting up trace flags for debug users (logs can be configured in project/config/.debug)'
    elif operation == 'run_apex_script':
        message = 'Running Apex script (logs can be found in project/apex-scripts/log)'
    elif operation == 'run_all_tests':
        message = 'Running all tests...'
    return message 