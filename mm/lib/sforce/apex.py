from base import SforceBaseClient

import re
import string
import suds.sudsobject
import lib.xmltodict as xmltodict
import lib.mm_util as mm_util

class SforceApexClient(SforceBaseClient):
    def __init__(self, wsdl, *args, **kwargs):
        super(SforceApexClient, self).__init__(wsdl, *args, **kwargs)
        header = self.generateHeader('SessionHeader')
        header.sessionId = kwargs['sid']
        self.setSessionHeader(header)
        msurl = kwargs['metadata_server_url']
        msurl = re.sub('/m/', '/s/', msurl)
        self._setEndpoint(msurl)
        self._setHeaders('')

    def compileClasses(self, payload, **kwargs):
        retXml = kwargs.get('retXml', True)
        self._sforce.set_options(retxml=retXml)
        result = self._handleResultTyping(self._sforce.service.compileClasses(payload))
        self._sforce.set_options(retxml=False)
        return result

    def compileTriggers(self, payload, **kwargs):
        retXml = kwargs.get('retXml', True)
        self._sforce.set_options(retxml=retXml)
        result = self._handleResultTyping(self._sforce.service.compileTriggers(payload))
        self._sforce.set_options(retxml=False)
        return result

    def executeAnonymous(self, params):
        if 'debug_categories' in params:
            self._setHeaders('execute_anonymous', debug_categories=params['debug_categories'])  
        execute_response = self._handleResultTyping(self._sforce.service.executeAnonymous(params['body']))
        execute_response['log'] = self.getDebugLog()
        return execute_response

    def runTests(self, params):
        #ERROR, WARN, INFO, DEBUG, FINE, FINER, FINEST
        #Db, Workflow, Validation, Callout, Apex_code, Apex_profiling, All
        retXml = params.get('retXml', True)
        self._sforce.set_options(retxml=retXml)
        if 'debug_categories' in params:
            self._setHeaders('runTests', debug_categories=params['debug_categories'])
        payload = {
            'namespace' : params.get('namespace', None),
            'allTests'  : params.get('run_all_tests', False),
            'classes'   : params.get('classes', [])
        }
        test_result = self._handleResultTyping(self._sforce.service.runTests(payload))
        self._sforce.set_options(retxml=False)
        if retXml == True:
            return xmltodict.parse(test_result,postprocessor=mm_util.xmltodict_postprocessor)
        else:
            test_result['log'] = self.getDebugLog()
        return test_result