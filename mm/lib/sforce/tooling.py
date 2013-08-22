from base import SforceBaseClient

import re

class SforceToolingClient(SforceBaseClient):
    def __init__(self, wsdl, *args, **kwargs):
        super(SforceToolingClient, self).__init__(wsdl, *args, **kwargs)
        header = self.generateHeader('SessionHeader')
        header.sessionId = kwargs['sid']
        self.setSessionHeader(header)
        msurl = kwargs['metadata_server_url']
        msurl = re.sub('/m/', '/T/', msurl)
        self._setEndpoint(msurl)
        self._setHeaders('')

    def addOverlayAction(self, payload, **kwargs):
        result = self._handleResultTyping(self._sforce.service.compileClasses(payload))
        return result

    def getOverlayActions(self, class_or_trigger_id):
        query_string = "Select Id, Line, Iteration, ExpirationDate, IsDumpingHeap from ApexExecutionOverlayAction Where ExecutableEntityId = '{0}'".format(class_or_trigger_id)
        result = self._handleResultTyping(self._sforce.service.query(query_string))
        return result

    def createOverlayAction(self, payload):
        #print self._sforce
        # result = self._sforce.service.create(payload)
        # return result
        payload = {'key1': 'value1', 'key2': 'value2'}
        r = requests.post("http://na1.salesforce.com/services/data/v26.0/tooling/sobjects/TraceFlag/.", data=payload)


    def describe(self):
        result = None
        try:
            result = self._handleResultTyping(self.describeGlobal())
            print 'result is: ', result
        except Exception, e:
            print e.message
        print self.getLastRequest()
        return result