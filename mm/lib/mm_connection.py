#when mavensmate binary is executed, a plugin connection should be created immediately
#plugin connection should have a single instance of a mm_client associated
import os
import json
import mm_util
import mm_github
import sys
import config
import logging
from enum import enum
from mm_project import MavensMateProject
from mm_exceptions import MMException

class MavensMatePluginConnection(object):

    currently_supported_clients = ['SUBLIME_TEXT_2', 'SUBLIME_TEXT_3']
    PluginClients = enum(SUBLIME_TEXT_2='SUBLIME_TEXT_2', SUBLIME_TEXT_3='SUBLIME_TEXT_3', NOTEPAD_PLUS_PLUS='NOTEPAD_PLUS_PLUS', TEXTMATE='TEXTMATE')
    
    def __init__(self, params={}, **kwargs):
        config.connection = self
        params = dict(params.items() + kwargs.items())
        self.operation              = params.get('operation', None)
        self.platform               = sys.platform
        self.plugin_client          = params.get('client', 'SUBLIME_TEXT_3') #=> "Sublime Text", "Notepad++", "TextMate"
        if self.plugin_client not in self.currently_supported_clients:
            self.plugin_client = 'SUBLIME_TEXT_3'
        self.plugin_client_version  = params.get('client_version', '2.0.1') #=> "1.0", "1.1.1", "v1"
        self.plugin_client_settings = self.get_plugin_client_settings()
        self.workspace              = self.get_workspace()
        self.project_name           = params.get('project_name', None)
        self.project_location       = None
        if self.project_name != None:
            self.project_location = os.path.join(self.workspace,self.project_name)
        self.project_id             = params.get('project_id', None)
        self.project                = None
        self.sfdc_api_version       = self.get_sfdc_api_version()
        self.ui                     = params.get('ui', False) #=> whether this connection was created for the purposes of generating a UI
        if 'wsdl_path' in params:
            mm_util.WSDL_PATH = params.get('wsdl_path')

        self.setup_logging()

        if self.sfdc_api_version != None:
            mm_util.SFDC_API_VERSION = self.sfdc_api_version #setting api version based on plugin settings

        if self.operation != 'new_project' and self.operation != 'upgrade_project' and self.operation != 'new_project_from_existing_directory' and self.project_location != None:
            if not os.path.exists(os.path.join(self.project_location)):
                raise MMException('Could not find project in workspace: '+self.workspace)
            if not os.path.exists(os.path.join(self.project_location,"config",".settings")):
                raise MMException('This does not seem to be a valid MavensMate project, missing config/.settings')
            if not os.path.exists(os.path.join(self.project_location,"src","package.xml")):
                raise MMException('This does not seem to be a valid MavensMate project, missing package.xml')

        if self.project_name != None and self.project_name != '' and not os.path.exists(self.project_location) and self.operation != 'new_project_from_existing_directory' and self.operation != 'new_project':
            raise MMException('The project could not be found')
        elif self.project_name != None and self.project_name != '' and os.path.exists(os.path.join(self.workspace,self.project_name)) and self.operation != 'new_project_from_existing_directory':
            params['location'] = self.project_location
            params['ui'] = self.ui
            self.project = MavensMateProject(params)

    def setup_logging(self):
        if self.get_log_level() != None:
            if self.get_log_location() != None:
                try:
                    config.logger.handlers = []
                    config.suds_logger.handlers = []
                    handler = logging.FileHandler(os.path.join(self.get_log_location(),"mm.log"))
                    config.logger.addHandler(handler)
                    config.suds_logger.addHandler(handler)
                except:
                    pass
            log_level = self.get_log_level()
            if log_level == 'CRITICAL':
                config.logger.setLevel(logging.CRITICAL)
                config.suds_logger.setLevel(logging.CRITICAL)
            elif log_level == 'ERROR':
                config.logger.setLevel(logging.ERROR)
                config.suds_logger.setLevel(logging.ERROR)
            elif log_level == 'WARNING':
                config.logger.setLevel(logging.WARNING)
                config.suds_logger.setLevel(logging.WARNING)
            elif log_level == 'DEBUG':
                config.logger.setLevel(logging.DEBUG)
                config.suds_logger.setLevel(logging.DEBUG)
            elif log_level == 'INFO':
                config.logger.setLevel(logging.INFO) 
                config.suds_logger.setLevel(logging.INFO)

    #returns the workspace for the current connection (/Users/username/Workspaces/MavensMate)
    def get_workspace(self):
        mm_workspace_setting = self.get_plugin_client_setting('mm_workspace')
        if mm_workspace_setting == None or mm_workspace_setting == '':
            raise MMException("Please set mm_workspace to the location where you'd like your mavensmate projects to reside")
        elif not os.path.exists(mm_workspace_setting):
            try:
                os.makedirs(mm_workspace_setting)
            except:
                raise MMException("Unable to create mm_workspace location")
        return self.get_plugin_client_setting('mm_workspace')

    #returns the MavensMate settings as a dict for the current plugin
    def get_plugin_client_settings(self):
        user_path = self.get_plugin_settings_path("User")
        def_path = self.get_plugin_settings_path("MavensMate")

        settings = {}
        if not user_path == None:
            try:
                settings['user'] = mm_util.parse_json_from_file(user_path)
            except:
                config.logger.debug('User settings could not be loaded')
        if not def_path == None:
            try:
                settings['default'] = mm_util.parse_json_from_file(def_path)
            except:
                raise MMException('Could not load default MavensMate settings.')
        return settings

    def get_plugin_settings_path(self, type="User", obj="mavensmate.sublime-settings"):
        if self.plugin_client == self.PluginClients.SUBLIME_TEXT_3:
            sublime_ver = "Sublime Text 3"
        elif self.plugin_client == self.PluginClients.SUBLIME_TEXT_2:
            sublime_ver = "Sublime Text 2"
        else:
            return None

        if self.platform == 'darwin':
            if sublime_ver == "Sublime Text 3":
                if os.path.exists(os.path.join(os.path.expanduser('~'),"Library","Application Support",sublime_ver,"Packages",type,obj)):
                    return os.path.join(os.path.expanduser('~'),"Library","Application Support",sublime_ver,"Packages",type,obj)
                else:
                    return os.path.join(os.path.expanduser('~'),"Library","Application Support","Sublime Text","Packages",type,obj)
            else:
                return os.path.join(os.path.expanduser('~'),"Library","Application Support",sublime_ver,"Packages",type,obj)
        elif self.platform == 'win32' or self.platform == 'cygwin':
            return os.path.join(os.environ['APPDATA'], sublime_ver, 'Packages', 'MavensMate', obj)
        elif self.platform == 'linux2':
            return os.path.join(os.path.expanduser('~'),".config","sublime-text-3","Packages",type,obj)
        else:
            return None

    def get_plugin_client_setting(self, key, default=None):
        if self.plugin_client_settings != None:
            if 'user' in self.plugin_client_settings and key in self.plugin_client_settings["user"]:
                return self.plugin_client_settings["user"][key]
            if 'default' in self.plugin_client_settings and key in self.plugin_client_settings["default"]:
                return self.plugin_client_settings["default"][key]
        return default

    #retrieves metadata from server, creates local project
    def new_project(self, params, **kwargs):
        try:
            if 'username' not in params or params['username'] == '':
                return mm_util.generate_error_response('Please specify a username')
            if 'password' not in params or params['password'] == '':
                return mm_util.generate_error_response('Please specify a password')
            if 'project_name' not in params or params['project_name'] == '':
                return mm_util.generate_error_response('Please specify a project name')

            if ('action' in kwargs and kwargs['action'] == 'new') or 'action' not in kwargs:
                if 'package' not in params or params['package'] == []:
                    params['package'] = {
                        'ApexClass'         : '*',
                        'ApexComponent'     : '*',
                        'ApexPage'          : '*',
                        'ApexTrigger'       : '*',
                        'StaticResource'    : '*'
                    }
                self.project = MavensMateProject(params)
                result = self.project.retrieve_and_write_to_disk()
            elif 'action' in kwargs and kwargs['action'] == 'existing':
                self.project = MavensMateProject(params)
                result = self.project.retrieve_and_write_to_disk('existing')

            if json.loads(result)['success'] == True:
                #opens project based on the client
                client_location = self.get_plugin_client_setting('mm_plugin_client_location')
                if client_location == None:
                    client_location = '/Applications'
                if self.plugin_client == self.PluginClients.SUBLIME_TEXT_2:
                    if self.platform == 'darwin':
                        os.system("'{0}/Sublime Text 2.app/Contents/SharedSupport/bin/subl' --project '{1}'".format(client_location,self.project.location+"/"+self.project.project_name+".sublime-project"))
                elif self.plugin_client == self.PluginClients.SUBLIME_TEXT_3:
                    if self.platform == 'darwin':
                        if os.path.exists(os.path.join('{0}/Sublime Text 3.app'.format(client_location))):
                            os.system("'{0}/Sublime Text 3.app/Contents/SharedSupport/bin/subl' --project '{1}'".format(client_location,self.project.location+"/"+self.project.project_name+".sublime-project"))
                        else:
                            os.system("'{0}/Sublime Text.app/Contents/SharedSupport/bin/subl' --project '{1}'".format(client_location,self.project.location+"/"+self.project.project_name+".sublime-project"))

            return result
        except BaseException, e:
            return mm_util.generate_error_response(e.message)

    def get_log_level(self):
        try:
            return self.get_plugin_client_setting('mm_log_level')
        except:
            return None

    def get_log_location(self):
        try:
            return self.get_plugin_client_setting('mm_log_location')
        except:
            return None

    def get_sfdc_api_version(self):
        try:
            return self.get_plugin_client_setting('mm_api_version')
        except:
            return None

    def sign_in_with_github(self, creds):
        try:
            response = mm_github.sign_in(creds)
            if 'message' in response:
                return mm_util.generate_error_response(response['message'])
            elif 'authentication' in response:
                if self.platform == 'darwin':
                    if not os.path.exists(os.path.join(os.path.expanduser('~'),'Library','Application Support','MavensMate')):
                        os.makedirs(os.path.join(os.path.expanduser('~'),'Library','Application Support','MavensMate'))

                    src = open(os.path.join(os.path.expanduser('~'),'Library','Application Support','MavensMate','.github.json'), "w")
                    src.write(json.dumps(response, sort_keys=False, indent=4))
                    src.close() 
                    return mm_util.generate_success_response('Connected to GitHub successfully!')
            else:
                return mm_util.generate_error_response(response)
        except Exception, e:
            return mm_util.generate_error_response("Error connecting to GitHub: "+e.message)





