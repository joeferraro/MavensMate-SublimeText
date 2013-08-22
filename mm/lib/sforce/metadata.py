# This program is free software; you can redistribute it and/or modify
# it under the terms of the (LGPL) GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the 
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library Lesser General Public License for more details at
# ( http://www.gnu.org/licenses/lgpl.html ).
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# Written by: David Lanstein ( dlanstein gmail com )

from base import SforceBaseClient
import lib.xmltodict as xmltodict
import time
import lib.mm_util as mm_util

class SforceMetadataClient(SforceBaseClient):
  
    def __init__(self, wsdl, *args, **kwargs):
        kwargs['isMetadata'] = True
        super(SforceMetadataClient, self).__init__(wsdl, *args, **kwargs)
        header = self.generateHeader('SessionHeader')
        header.sessionId = kwargs['sid']
        self.setSessionHeader(header)
        self._setEndpoint(kwargs['url'])
        self._setHeaders('')

    def listMetadata(self, metadata_type, retXml=True, version=26.0):
        # obj = { 'type': 'ApexClass' }
        # response = mclient.service.listMetadata(obj, 25.0)
        self._sforce.set_options(retxml=retXml)
        if type(metadata_type) is not dict and type(metadata_type) is not list:
            obj = { 'type' : metadata_type }
        else:
            obj = metadata_type
        list_result = self._handleResultTyping(self._sforce.service.listMetadata(obj, version))
        self._sforce.set_options(retxml=False)
        if retXml == True:
            try:
                list_result_dict = xmltodict.parse(list_result,postprocessor=mm_util.xmltodict_postprocessor)
                return list_result_dict['soapenv:Envelope']["soapenv:Body"]["listMetadataResponse"]["result"]
            except:
                return []
        return list_result

    def retrieve(self, **kwargs):
        # request = {
        #   'RetrieveRequest': {
        #     'unpackaged': {
        #       'types': {
        #         'ApexTrigger': '*'
        #       }
        #     },
        #     'apiVersion': {
        #       25.0
        #     }
        #   }
        # }
        # package = {
        #     'unpackaged' : {
        #         'types' : [
        #             {
        #                 "members": "*", 
        #                 "name": "ApexClass"
        #             }
        #         ]
        #     }
        # }
        package_dict = None
        request_payload = None
        
        if 'package' in kwargs and type(kwargs['package']) is not dict: 
            #if package is location of package.xml, we'll parse the xml and create a request
            package_dict = xmltodict.parse(mm_util.get_file_as_string(kwargs['package']))
            api_version = package_dict['Package']['version']
            package_dict['unpackaged'] = package_dict.pop('Package')
            package_dict['unpackaged'].pop('version')
            package_dict['unpackaged'].pop("@xmlns", None)
            package_dict['unpackaged'].pop("#text", None)
            package_dict['apiVersion'] = api_version
            types = package_dict['unpackaged']['types']
            requested_types = []
            if 'type' in kwargs and kwargs['type'] != None and kwargs['type'] != '': #if the request is for a certain type, only request that type
                for i, val in enumerate(types):
                    if val['name'] == kwargs['type']:
                        requested_types.append(val)
                package_dict['unpackaged']['types'] = requested_types
                types = requested_types
            for i, val in enumerate(types):
                try:
                    package_dict['unpackaged']['types'][i].pop("#text", None)
                except:
                    package_dict['unpackaged']['types'].pop("#text", None)

            #if custom object is asterisked, we need to explictly retrieve standard objects
            for t in package_dict['unpackaged']['types']:
                if 'name' in t and t['name'] == 'CustomObject':
                    if 'members' in t and type(t['members']) is not list:
                        if t['members'] == "*":
                            mlist = self.listMetadata('CustomObject', False)
                            objs = []
                            for obj in mlist:
                                if ('__c') not in mlist:
                                    objs.append(obj['fullName'])
                            objs.append("*")
                            objs.sort()
                            t['members'] = objs

            request_payload = package_dict

        elif 'package' in kwargs and type(kwargs['package']) is dict:
            package = kwargs['package']
            if 'unpackaged' not in package:
                #{ "ApexClass"    : ["MultiselectControllerTest","MultiselectController"] }
                type_array = []
                for i, metadata_type in enumerate(package):
                    member_value = package[metadata_type]
                    type_array.append({ "name" : metadata_type, "members" : member_value })

                package = {
                    'unpackaged' : {
                        'types' : type_array
                    },
                    'apiVersion' : mm_util.SFDC_API_VERSION
                }
            
            #if custom object is asterisked, we need to explictly retrieve standard objects
            for t in package['unpackaged']['types']:
                if 'name' in t and t['name'] == 'CustomObject':
                    if 'members' in t and type(t['members']) is not list:
                        if t['members'] == "*":
                            mlist = self.listMetadata('CustomObject', False)
                            objs = []
                            for obj in mlist:
                                if ('__c') not in mlist:
                                    objs.append(obj['fullName'])
                            objs.append("*")
                            objs.sort()
                            t['members'] = objs
            
            request_payload = package
        
        result = self._handleResultTyping(self._sforce.service.retrieve(request_payload))
        if result.done == False:
            self._waitForRequest(result.id)
            return self._getRetrieveBody(result.id)
        else:
            return result

    def deploy(self, params={}, **kwargs):
        if 'debug_categories' in params:
            self._setHeaders('deploy', debug_categories=params['debug_categories'])  
        
        deploy_options = {}

        is_test = kwargs.get('is_test', False)
        if is_test:
            deploy_options['checkOnly']         = True
            deploy_options['runAllTests']       = False
            deploy_options['runTests']          = params.get('classes', [])
        else:
            deploy_options['checkOnly']         = params.get('check_only', False)
            deploy_options['rollbackOnError']   = params.get('rollback_on_error', True)
            deploy_options['runAllTests']       = params.get('run_tests', False)
            deploy_options['runTests']          = params.get('classes', [])

        result = self._handleResultTyping(self._sforce.service.deploy(params['zip_file'], deploy_options))
        #config.logger.debug('deploy request')
        #config.logger.debug(self.getLastRequest())

        if result.done == False:
            self._waitForRequest(result.id)
            if 'ret_xml' in params and params['ret_xml'] == True:
                self._sforce.set_options(retxml=True)
            #self._setHeaders('deploy_response', debug_category='Apex_code', debug_level='DEBUG')
            deploy_result = self._getDeployResponse(result.id)
            #print deploy_result
            #if 'debug_categories' in params and 'ret_xml' in params and params['ret_xml'] == True:
            #    deploy_result['log'] = self.getDebugLog()
            self._sforce.set_options(retxml=False)  
            return deploy_result
        else:
            if 'debug_categories' in params and 'ret_xml' in params and params['ret_xml'] == True:
                result['log'] = self.getDebugLog()
            return result

    def getOrgNamespace(self):
        describe_result = self.describeMetadata(retXml=False)
        return describe_result.organizationNamespace or ''

    def describeMetadata(self, **kwargs):
        retXml = kwargs.get('retXml', True)
        self._sforce.set_options(retxml=retXml)
        api_version = kwargs.get('api_version', mm_util.SFDC_API_VERSION)
        metadata_result = self._sforce.service.describeMetadata(api_version)
        self._sforce.set_options(retxml=False)
        return metadata_result

    def _getDeployResponse(self, id):
        return self._handleResultTyping(self._sforce.service.checkDeployStatus(id))

    def _getRetrieveBody(self, id):
        return self._handleResultTyping(self._sforce.service.checkRetrieveStatus(id))

    def _waitForRequest(self, id):
        finished = False
        checkStatusResponse = None
        while finished == False:
            time.sleep(1)
            checkStatusResponse = self._sforce.service.checkStatus(id)
            finished = checkStatusResponse[0].done

    # SOAP header-related calls (debug options?)
    def setCallOptions(self, header):
        '''
        This header is only applicable to the Partner WSDL
        '''
        self._callOptions = header
