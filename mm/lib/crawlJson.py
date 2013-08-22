import types
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

def crawlDict(jsonData, depth, query, parentVisiblity):	
	depth += 1
	visibility = 0
	childVisibility = 0
	for key, value in jsonData.items():
		if isinstance(value, basestring) and query in value.lower():			
			visibility = 1
		elif not isinstance(value, types.DictType) and not isinstance(value, types.ListType) and query in str(value).lower():
			visibility = 1
	for key, value in jsonData.items():
		if crawl(value, depth, query, visibility) > 0:
			childVisibility = 1			
		visibility = visibility if visibility > childVisibility else childVisibility
	jsonData["visibility"] = visibility
	if visibility == 0:
		jsonData["cls"] = "hidden"
		jsonData["addClass"] = "dynatree-hidden"
	return visibility

def crawlArray(jsonData, depth, query, parentVisiblity):
	depth += 1
	elementsToRemove = []
	index = 0
	for value in jsonData:
		if isinstance(value, basestring):
			childVisibility = query in value.lower()
		elif isinstance(value, types.DictType):
			childVisibility = crawl(value, depth, query, parentVisiblity)
			value["index"] = index
		else:
			childVisibility = query in str(value).lower()
		if childVisibility == 0 and parentVisiblity == 0:
			elementsToRemove.append(value)
			try:
				value["cls"] = "hidden"
				value["addClass"] = "dynatree-hidden"
			except:
				pass
		else:
			try:
				value["expanded"] = True
			except:
				pass
		index += 1

def crawl(jsonData, depth, query, parentVisiblity):
	if(isinstance(jsonData,types.DictType)):
		return crawlDict(jsonData, depth, query, parentVisiblity)
	elif(isinstance(jsonData, types.ListType)):
		crawlArray(jsonData, depth, query, parentVisiblity)		
		for jd in jsonData:
			if 'visibility' in jd and jd['visibility'] == 1:
				return True
		return False
		# if 'cls' in jsonData and jsonData['cls'] == 'hidden':
		# 	return False
		# else:
		# 	return True
	else:	
		return 0

def setVisibility(jsonData, query):
	crawl(jsonData, 0, query.lower(), 0)

def setChecked(src, ids=[], dpth = 0, key = ''):
    """ Recursively find checked item."""
    #tabs = lambda n: ' ' * n * 4 # or 2 or 8 or...
    #brace = lambda s, n: '%s%s%s' % ('['*n, s, ']'*n)

    if isinstance(src, dict):
        for key, value in src.iteritems():
            setChecked(value, ids, dpth + 1, key)
    elif isinstance(src, list):
        for litem in src:
            if isinstance(litem, types.DictType):
	            if "id" in litem and litem["id"] in ids:
	            	litem["checked"] = True
	            	litem["select"] = True
            setChecked(litem, ids, dpth + 2)

def fun(d, tokens):
    print tokens
    if 'id' in d and d['id'] in tokens:
        d['cls'] = 'x-tree-checkbox-checked-disabled'
    for k in d:
        if isinstance(d[k], list):
            for i in d[k]:
                print i
                #for j in fun(i, tokens):
                    #yield j
                #    pass

def setThirdStateChecked(src, ids=[], dpth = 0, key = ''):
    """ Recursively find checked item."""
    #tabs = lambda n: ' ' * n * 4 # or 2 or 8 or...
    #brace = lambda s, n: '%s%s%s' % ('['*n, s, ']'*n)
    #print('third state nodes: ', third_state_nodes)
    if isinstance(src, dict):
        #print "DICT: ", src
        if 'children' in src and type(src['children']) is list and len(src['children']) > 0:
        	children = src['children']
        	number_of_possible_checked = len(children)
        	number_of_checked = 0
        	for c in children:
        		if 'checked' in c and c['checked']:
        			number_of_checked += 1
        	if number_of_possible_checked == number_of_checked:
        		src['checked'] = True
        	elif number_of_checked > 0:
        		#print('>>>>> APPENDING: ', src['id'])
        		lineage = src['id'].split('.')
        		#fun(src, lineage)
        		src['cls'] = 'x-tree-checkbox-checked-disabled'

        for key, value in src.iteritems():
            setThirdStateChecked(value, ids, dpth + 1, key)
    elif isinstance(src, list):
        for litem in src:
            if isinstance(litem, types.DictType):
	            #print litem["id"]
	            #print third_state_nodes
	            #if "id" in litem and litem["id"] in third_state_nodes:
	            #	litem["cls"] = 'x-tree-checkbox-checked-disabled'
	            pass
            setThirdStateChecked(litem, ids, dpth + 2)




