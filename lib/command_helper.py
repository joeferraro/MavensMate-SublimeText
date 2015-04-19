def get_message(params, operation):
    message = 'Handling requested operation...'
    if operation == 'new-metadata':
        message = 'Opening New Metadata UI'
    elif operation == 'compile-metadata':
        if 'paths' in params and len(params['paths']) == 1:
            what = params['paths'][0]
            if '/' in what:
                what = what.split('/')[-1]
            message = 'Compiling: ' + what
        else:
            message = 'Compiling Selected Metadata'
    elif operation == 'compile-project':
        message = 'Compiling Project'
    elif operation == 'edit-project':
        message = 'Opening Edit Project dialog'
    elif operation == 'run-tests':
        if 'selected' in params and len(params['selected']) == 1:
            message = "Running Apex Test for " + params['selected'][0]
        else:
            message = 'Opening Apex Test Runner'
    elif operation == 'clean-project':
        message = 'Cleaning Project'
    elif operation == 'deploy':
        message = 'Opening Deploy dialog'
    elif operation == 'execute-apex':
        message = 'Opening Execute Apex dialog'
    elif operation == 'upgrade-project':
        message = 'Your MavensMate project needs to be upgraded. Opening the upgrade UI.'
    elif operation == 'index-metadata':
        message = 'Indexing Metadata'
    elif operation == 'delete-metadata':
        if 'paths' in params and len(params['paths']) == 1:
            what = params['paths'][0]
            if '/' in what:
                what = what.split('/')[-1]
            message = 'Deleting: ' + what
        else:
            message = 'Deleting Selected Metadata'
    elif operation == 'refresh-metadata':
        if 'paths' in params and len(params['paths']) == 1:
            what = params['paths'][0]
            if '/' in what:
                what = what.split('/')[-1]
            message = 'Refreshing: ' + what
        else:
            message = 'Refreshing Selected Metadata'
    elif operation == 'open-metadata':
        message = 'Opening Selected Metadata'
    elif operation == 'start-logging':
        message = 'Started logging for user ids specified in config/.debug'
    elif operation == 'stop-logging':
        message = 'Stopped logging for user ids specified in config/.debug'
    elif operation == 'fetch-logs':
        message = 'Fetching Apex Logs (will be placed in project/debug/logs)'
    elif operation == 'import-project':
        message = 'Opening New Project Dialog'
    elif operation == 'index-apex':
        message = 'Indexing Project Apex Metadata'
    elif operation == 'test-async':
        if 'classes' in params and len(params['classes']) == 1:
            what = params['classes'][0]
            if '/' in what:
                what = what.split('/')[-1]
            message = 'Running Apex unit tests for: ' + what
        else:
            message = 'Running Apex unit tests for this class...'
    elif operation == 'run-apex-script':
        message = 'Running Apex script (logs can be found in project/apex-scripts/log)'
    elif operation == 'new-apex-script':
        message = 'Creating new Apex script'
    elif operation == 'run-all-tests':
        message = 'Running all tests...'
    return message
