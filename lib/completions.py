import os
import threading
import pipes 
import subprocess
import json
try:
    import MavensMate.config as config
except:
    import config
try:
    from .threads import ThreadTracker
    from .threads import ThreadProgress
    from .threads import PanelThreadProgress
    from .printer import PanelPrinter
    import MavensMate.lib.command_helper as command_helper
    import MavensMate.util as util
except:
    from lib.threads import ThreadTracker
    from lib.threads import ThreadProgress
    from lib.threads import PanelThreadProgress
    from lib.printer import PanelPrinter
    import lib.command_helper as command_helper
    import util

#preps code completion object for search
def prep_for_search(name): 
    #s1 = re.sub('(.)([A-Z]+)', r'\1_\2', name).strip()
    #return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    #return re.sub('([A-Z])', r'\1_', name)
    return name.replace('_', '')

#returns suggestions based on tooling api symbol table
def get_apex_completions(search_name):
    completions = []
    if not os.path.exists(os.path.join(util.mm_project_directory(), 'config', '.apex_file_properties')):
        return []

    apex_props = util.parse_json_from_file(os.path.join(util.mm_project_directory(), "config", ".apex_file_properties"))

    for p in apex_props.keys():
        if p == search_name+".cls" and 'symbolTable' in apex_props[p]:
            symbol_table = apex_props[p]['symbolTable']
            if 'constructors' in symbol_table:
                for c in symbol_table['constructors']:
                    completions.append((c["visibility"] + " " + c["name"], c["name"]))
            if 'properties' in symbol_table:
                for c in symbol_table['properties']:
                    completions.append((c["visibility"] + " " + c["name"], c["name"]))
            if 'methods' in symbol_table:
                for c in symbol_table['methods']:
                    params = ''
                    if 'parameters' in c and type(c['parameters']) is list and len(c['parameters']) > 0:
                        for p in c['parameters']:
                            params += p['name'] + " (" + p["type"] + ")"
                    completions.append((c["visibility"] + " " + c["name"]+"("+params+") "+c['returnType'], c["name"]))
    return sorted(completions) 

#returns suggestions based on parse.jar binary response
def get_variable_list(view):
    #print(view.substr(sublime.Region(0,10000000)))
    thread = ApexSourceParser(
        view=view,
        file_path=view.file_name(),
        is_dirty=view.is_dirty()
    )
    thread.start()
    thread.join()
    return thread.result

class ApexSourceParser(threading.Thread):
    def __init__(self, **kwargs):
        self.view           = kwargs.get('view', None)
        self.file_path      = kwargs.get('file_path', None)
        self.is_dirty       = kwargs.get('is_dirty', True)
        self.result         = None

        threading.Thread.__init__(self)

    def submit_payload(self, process):
        payload = util.get_file_as_string(self.file_path)   
        #payload = payload.replace('\n', ' ').replace('\r', '')    
        #print(payload)
        try:
            process.stdin.write(payload)
        except:
            process.stdin.write(payload.encode('utf-8'))
        process.stdin.close()

    def run(self):
        #if self.is_dirty:
        #   print("java -jar {0}".format(pipes.quote(config.mm_dir+"/bin/parser.jar")))
        #   p = subprocess.Popen("java -jar {0}".format(pipes.quote(config.mm_dir+"/bin/parser.jar")), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True) 
        #   self.submit_payload(p)
        #else:
        p = subprocess.Popen("java -jar {0} {1}".format(pipes.quote(config.mm_dir+"/bin/parser.jar"), pipes.quote(self.file_path)), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True) 

        msg = None
        if p.stdout is not None: 
            msg = p.stdout.readlines()
        elif p.stderr is not None:
            msg = p.stdout.readlines() 
        if msg == '' or len(msg) == 0:
            return_dict = {
                "result" : []
            }
            result = json.dumps(return_dict)
        else:
            result = msg[0].decode("utf-8")
            result = result.replace(",]}","]}")
        print(result)
        self.result = json.loads(result)