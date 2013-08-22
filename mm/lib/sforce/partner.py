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
import suds.sudsobject

class SforcePartnerClient(SforceBaseClient):
  def __init__(self, wsdl, *args, **kwargs):
    super(SforcePartnerClient, self).__init__(wsdl, *args, **kwargs)

  # Toolkit-specific calls

  def _stringifyResultRecords(self, struct):
    '''
    The Partner WSDL defines result element not defined in the "SObject"
    section of the Partner WSDL as <any/> elements, which get unmarshalled by
    suds into single-element lists.  We prefer that they are strings, so we'll 
    convert structures like

[(records){
   type = "Contact"
   Id = "003000000000000000"
   Account[] = 
      (Account){
         type = "Account"
         Id = "001000000000000000"
         Name[] = 
            "Acme",
      },
   FirstName[] = 
      "Wile E.",
   LastName[] = 
      "Coyote",
 }]

    to

[(records){
   type = "Contact"
   Id = "003000000000000000"
   Account = 
      (Account){
         type = "Account"
         Id = "001000000000000000"
         Name = "Acme"
      }
   FirstName = "Wile E."
   LastName = "Coyote"
 }]

    and

searchRecords[] = 
      (searchRecords){
         record = 
            (record){
               type = "Lead"
               Id = None
               Name[] = 
                  "Single User",
               Phone[] = 
                  "(617) 555-1212",
            }
      },

    to

searchRecords[] = 
      (searchRecords){
         record = 
            (record){
               type = "Lead"
               Id = None
               Name = "Single User",
               Phone = "(617) 555-1212",
            }
      },
    '''
    if not isinstance(struct, list):
      struct = [struct]
      originallyList = False
    else:
      originallyList = True

    for record in struct:
      for k, v in record:
        if isinstance(v, list):
          # At this point, we don't know whether a value of [] corresponds to '' or None
          # However, anecdotally I've been unable to find a field type whose 'empty' value
          # returns anything other that <sf:FieldNameHere xsi:nil="true"/>
          # so, for now, we'll set it to None
          if v == []:
            setattr(record, k, None)
          else:
            # Note that without strong typing there's no way to tell the difference between the 
            # string 'false' and the bool false.  We get <sf:DoNotCall>false</sf:DoNotCall>.
            # We have to assume strings for everything other than 'Id' and 'type', which are
            # defined types in the Partner WSDL.
	
            # values that are objects may (query()) or may not (search()) be wrapped in a list
            # so, remove from nested list first before calling ourselves recursively (if necessary)
            setattr(record, k, v[0])
        
        # refresh v
        v = getattr(record, k)

        if isinstance(v, suds.sudsobject.Object):
          v = self._stringifyResultRecords(v)
          setattr(record, k, v)
    if originallyList:
      return struct
    else:
      return struct[0]

  # Core calls

  def convertLead(self, leadConverts):
    xml = self._marshallSObjects(leadConverts)
    return super(SforcePartnerClient, self).convertLead(xml)

  def merge(self, sObjects):
    xml = self._marshallSObjects(sObjects)
    return super(SforcePartnerClient, self).merge(xml)

  def process(self, sObjects):
    xml = self._marshallSObjects(sObjects)
    return super(SforcePartnerClient, self).process(xml)

  def query(self, queryString):
    queryResult = super(SforcePartnerClient, self).query(queryString)
    if queryResult.size > 0 and 'records' in queryResult:
      queryResult.records = self._stringifyResultRecords(queryResult.records)
    return queryResult

  def queryAll(self, queryString):
    queryResult = super(SforcePartnerClient, self).queryAll(queryString)
    if queryResult.size > 0:
      queryResult.records = self._stringifyResultRecords(queryResult.records)
    return queryResult
  
  def queryMore(self, queryLocator):
    queryResult = super(SforcePartnerClient, self).queryMore(queryLocator)
    if queryResult.size > 0:
      queryResult.records = self._stringifyResultRecords(queryResult.records)
    return queryResult
  
  def retrieve(self, fieldList, sObjectType, ids):
    sObjects = super(SforcePartnerClient, self).retrieve(fieldList, sObjectType, ids)
    sObjects = self._stringifyResultRecords(sObjects)
    return sObjects
  
  def search(self, searchString):
    searchResult = super(SforcePartnerClient, self).search(searchString)

    # HACK <result/> gets unmarshalled as '' instead of an empty SearchResult
    # return an empty SearchResult instead
    if searchResult == '':
      return self._sforce.factory.create('SearchResult')

    searchResult.searchRecords = self._stringifyResultRecords(searchResult.searchRecords)
    return searchResult

  # Utility calls

  def sendEmail(self, sObjects):
    xml = self._marshallSObjects(sObjects)
    return super(SforcePartnerClient, self).sendEmail(xml)

  # SOAP header-related calls

  def setCallOptions(self, header):
    '''
    This header is only applicable to the Partner WSDL
    '''
    self._callOptions = header
