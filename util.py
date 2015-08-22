import sys
import os
import json
import re
import shutil
import codecs
import string
import random
import urllib.request
import MavensMate.config as config
import MavensMate.lib.apex.apex_extensions as apex_extensions
import sublime
from xml.dom.minidom import parse

settings = sublime.load_settings('mavensmate.sublime-settings')
packages_path = sublime.packages_path()
sublime_version = int(float(sublime.version()))

debug = config.debug

def standard_object_names():
    return [
        "Account", "Opportunity", "Contact", "Lead", "Pricebook2", "Product"
    ]

def mm_plugin_location():
    return os.path.join(packages_path,"MavensMate")

def package_check():
    #ensure user settings are installed
    try:
        if not os.path.isfile(os.path.join(sublime.packages_path(),"User","mavensmate.sublime-settings")):
            shutil.copyfile(os.path.join(sublime.packages_path(),"MavensMate","mavensmate.sublime-settings"), os.path.join(sublime.packages_path(),"User","mavensmate.sublime-settings"))
        elif os.path.isfile(os.path.join(sublime.packages_path(),"User","mavensmate.sublime-settings")):
            user_settings = get_file_as_string(os.path.join(sublime.packages_path(),"User","mavensmate.sublime-settings"))
            if 'mm_use_keyring' in user_settings or 'mm_workspace' in user_settings or 'mm_api_version' in user_settings:
                shutil.copyfile(os.path.join(sublime.packages_path(),"User","mavensmate.sublime-settings"), os.path.join(sublime.packages_path(),"User","mavensmate-deprecated.sublime-settings"))
                shutil.copyfile(os.path.join(sublime.packages_path(),"MavensMate","mavensmate.sublime-settings"), os.path.join(sublime.packages_path(),"User","mavensmate.sublime-settings"))

    except:
        debug('could not migrate default settings to user settings')
        pass

def parse_json_from_file(location):
    try:
        json_data = open(location)
        data = json.load(json_data)
        json_data.close()
        return data
    except:
        return {}

def parse_templates_package(mtype=None):
    try:
        settings = sublime.load_settings('mavensmate.sublime-settings')
        template_source = settings.get('mm_template_source', 'joeferraro/MavensMate-Templates/master')
        template_location = settings.get('mm_template_location', 'remote')
        if template_location == 'remote':
            if 'linux' in sys.platform:
                response = os.popen('wget https://raw.githubusercontent.com/{0}/{1} -q -O -'.format(template_source, "package.json")).read()
            else:
                response = urllib.request.urlopen('https://raw.githubusercontent.com/{0}/{1}'.format(template_source, "package.json")).read().decode('utf-8')
            j = json.loads(response)
        else:
            local_template_path = os.path.join(template_source,"package.json")
            debug(local_template_path)
            j = parse_json_from_file(local_template_path)
            if j == None or j == {}:
                raise Exception('Could not load local templates. Check your "mm_template_source" setting.')
    except Exception as e:
        debug('Failed to load templates, reverting to local template store.')
        debug(e)
        local_template_path = os.path.join(config.mm_dir,"lib","apex","metadata-templates","package.json")
        j = parse_json_from_file(local_template_path)
    if mtype != None:
        return j[mtype]
    else:
        return j


def get_number_of_lines_in_file(file_path):
    f = open(file_path)
    lines = f.readlines()
    f.close()
    return len(lines) + 1

def get_execution_overlays(file_path):
    try:
        response = []
        fileName, ext = os.path.splitext(os.path.basename(file_path))
        if ext == ".cls" or ext == ".trigger":
            api_name = fileName
            overlays = parse_json_from_file(mm_project_directory()+"/config/.overlays")
            for o in overlays:
                if o['API_Name'] == api_name:
                    response.append(o)
        return response
    except:
        return []

def get_random_string(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def get_active_file():
    try:
        return sublime.active_window().active_view().file_name()
    except Exception:
        return ''

def get_file_name_no_extension(path):
    base=os.path.basename(path)
    return os.path.splitext(base)[0]

def get_project_name(context=None):
    if context != None:
        if isinstance(context, sublime.View):
            view = context
            window = view.window()
        elif isinstance(context, sublime.Window):
            window = context
            view = window.active_view()
        else:
            window = sublime.active_window()
            view = window.active_view()
    else:
        window = sublime.active_window()
        view = window.active_view()

    if is_mm_project(window):
        if context == None:
            try:
                return os.path.basename(sublime.active_window().folders()[0])
            except:
                return None
        else:
            try:
                return os.path.basename(window.folders()[0])
            except:
                return None
    else:
        return None

def sublime_project_file_path():
    project_directory = sublime.active_window().folders()[0]
    if os.path.isfile(os.path.join(project_directory,".sublime-project")):
        return os.path.join(project_directory,".sublime-project")
    elif os.path.isfile(os.path.join(project_directory,get_project_name(),".sublime-project")):
        return os.path.join(project_directory,get_project_name(),".sublime-project")
    else:
        return None

def get_project_settings(window=None):
    if window == None:
        window = sublime.active_window()
    try:
       return parse_json_from_file(os.path.join(window.folders()[0],"config",".settings"))
    except:
        raise BaseException("Could not load project settings")

# check for mavensmate .settings file
def is_mm_project(window=None):
    if window == None:
        window = sublime.active_window()
    try:
        if os.path.isfile(os.path.join(window.folders()[0],"config",".settings")):
            return True
        elif os.path.isfile(os.path.join(window.folders()[0],"config","settings.yaml")):
            return True
        else:
            return False
    except:
        return False

def get_file_extension(filename=None):
    try :
        if not filename: filename = get_active_file()
        fn, ext = os.path.splitext(filename)
        return ext
    except:
        pass
    return None

def get_apex_file_properties():
    return parse_json_from_file(os.path.join(mm_project_directory(),"config",".apex_file_properties"))

def is_mm_file(filename=None):
    try:
        if is_mm_project():
            if not filename:
                filename = get_active_file()
            project_directory = mm_project_directory(sublime.active_window())
            if os.path.join(project_directory,"src","documents") in filename:
                return True
            if os.path.exists(filename) and os.path.join(project_directory,"src") in filename:
                settings = sublime.load_settings('mavensmate.sublime-settings')
                valid_file_extensions = settings.get("mm_apex_file_extensions", [])
                if get_file_extension(filename) in valid_file_extensions and 'apex-scripts' not in get_active_file():
                    return True
                elif "-meta.xml" in filename:
                    return True
    except Exception as e:
        #traceback.print_exc()
        pass
    return False

def is_mm_dir(directory):
    if is_mm_project():
        if os.path.isdir(directory):
            if os.path.basename(directory) == "src" or os.path.basename(directory) == get_project_name() or os.path.basename(os.path.abspath(os.path.join(directory, os.pardir))) == "src":
                return True
    return False

def is_browsable_file(filename=None):
    try :
        if is_mm_project():
            if not filename:
                filename = get_active_file()
            if is_mm_file(filename):
                basename = os.path.basename(filename)
                data = get_apex_file_properties()
                if basename in data:
                    return True
                return os.path.isfile(filename+"-meta.xml")
    except:
        pass
    return False

def is_apex_class_file(filename=None):
    if not filename: filename = get_active_file()
    if is_mm_file(filename):
        f, ext = os.path.splitext(filename)
        if ext == ".cls":
            return True
    return False

def is_apex_test_file(filename=None):
    if not filename: filename = get_active_file()
    if not is_apex_class_file(filename): return False
    with codecs.open(filename, "r", "utf-8") as content_file:
        content = content_file.read()
        p = re.compile("@isTest\s", re.I + re.M)
        if p.search(content):
            return True
        p = re.compile("\sstatic testMethod\s", re.I + re.M)
        if p.search(content):
            return True
    return False

def mark_overlays(view, lines):
    mark_line_numbers(view, lines, "dot", "overlay")

def write_overlays(view, overlay_result):
    result = json.loads(overlay_result)
    if result["totalSize"] > 0:
        for r in result["records"]:
            sublime.set_timeout(lambda: mark_line_numbers(view, [int(r["Line"])], "dot", "overlay"), 100)

def mark_line_numbers(view, lines, icon="dot", mark_type="compile_issue"):
    try:
        view.add_regions(mark_type, [view.line(view.text_point(lines[0]-1, 0))], "invalid.illegal", icon, sublime.DRAW_EMPTY_AS_OVERWRITE)
    except:
        points = [view.text_point(l - 1, 0) for l in lines]
        regions = [sublime.Region(p, p) for p in points]
        view.add_regions(mark_type, regions, "operation.fail", icon, sublime.HIDDEN | sublime.DRAW_EMPTY)

def mark_uncovered_lines(view, lines, icon="bookmark", mark_type="no_apex_coverage"):
    regions = []
    for line in lines:
        regions.append(view.line(view.text_point(line-1, 0)))
    view.add_regions(mark_type, regions, "invalid.illegal", icon, sublime.DRAW_EMPTY_AS_OVERWRITE)

def get_template_params(github_template):
    return github_template["params"]

def get_new_metadata_input_label(github_template):
    if "params" in github_template:
        params = []
        for param in github_template["params"]:
            params.append(param["description"])
        label = ", ".join(params)
    else:
        label = ""
    return label

def get_new_metadata_input_placeholders(github_template):
    if "params" in github_template:
        placeholders = []
        for param in github_template["params"]:
            if "default" in param:
                placeholders.append(param["default"])
        label = ", ".join(placeholders)
    else:
        label = "Default"
    return label

def clear_marked_line_numbers(view, mark_type="compile_issue"):
    try:
        sublime.set_timeout(lambda: view.erase_regions(mark_type), 100)
    except Exception as e:
        debug(e.message)
        debug('no regions to clean up')

def get_window_and_view_based_on_context(context):
    if isinstance(context, sublime.View):
        view = context
        window = view.window()
    elif isinstance(context, sublime.Window):
        window = context
        view = window.active_view()
    else:
        window = sublime.active_window()
        view = window.active_view()
    return window, view

def is_apex_webservice_file(filename=None):
    if not filename: filename = get_active_file()
    if not is_apex_class_file(filename): return False
    with codecs.open(filename, "r", "utf-8") as content_file:
        content = content_file.read()
        p = re.compile("global\s+(abstract\s+)?class\s", re.I + re.M)
        if p.search(content):
            p = re.compile("\swebservice\s", re.I + re.M)
            if p.search(content): return True
    return False

def mm_project_directory(window=None):
    if window == None:
        window = sublime.active_window()
    folders = window.folders()
    if len(folders) > 0:
        return window.folders()[0]

def print_debug_panel_message(message):
    # printer = PanelPrinter.get(sublime.active_window().id())
    # printer.show()
    # printer.write(message)
    pass

#parses the input from sublime text
def parse_new_metadata_input(input):
    input = input.replace(" ", "")
    if "," in input:
        params = input.split(",")
        api_name = params[0]
        class_type_or_sobject_name = params[1]
        return api_name, class_type_or_sobject_name
    else:
        return input

def to_bool(value):
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if str(value).lower() in ("yes", "y", "true",  "t", "1"): return True
    if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))

def get_tab_file_names():
    tabs = []
    win = sublime.active_window()
    for vw in win.views():
        if vw.file_name() is not None:
            try:
                extension = os.path.splitext(vw.file_name())[1]
                extension = extension.replace(".","")
                if extension in apex_extensions.valid_extensions:
                    tabs.append(vw.file_name())
            except:
                pass
        else:
            pass      # leave new/untitled files (for the moment)
    return tabs

def get_file_as_string(file_path):
    #debug(file_path)
    try:
        f = codecs.open(file_path, "r", "utf8")
        file_body = f.read()
        f.close()
        return file_body
    except Exception:
        #print "Couldn't open "+str(file_path)+" because: "+e.message
        pass
    return ""

def refresh_active_view():
    sublime.set_timeout(sublime.active_window().active_view().run_command('revert'), 100)

def check_for_updates():
    settings = sublime.load_settings('mavensmate.sublime-settings')
    if settings.get('mm_check_for_updates') == True:
        sublime.set_timeout(lambda: MmInstaller().start(), 1000)

def get_field_completions(object_name):
    _completions = []
    if os.path.isfile(os.path.join(mm_project_directory(),"src","objects",object_name+".object")): #=> object fields from src directory (more info on field metadata, so is primary)
        object_dom = parse(os.path.join(mm_project_directory(),"src","objects",object_name+".object"))
        for node in object_dom.getElementsByTagName('fields'):
            field_name = ''
            field_type = ''
            for child in node.childNodes:
                if child.nodeName != 'fullName' and child.nodeName != 'type': continue
                if child.nodeName == 'fullName':
                    field_name = child.firstChild.nodeValue
                elif child.nodeName == 'type':
                    field_type = child.firstChild.nodeValue
            _completions.append((field_name+" \t"+field_type, field_name))
        return sorted(_completions)
    elif os.path.isfile(os.path.join(mm_project_directory(),"config",".org_metadata")): #=> parse org metadata, looking for object fields
        jsonData = parse_json_from_file(os.path.join(mm_project_directory(),"config",".org_metadata"))
        for metadata_type in jsonData:
            if 'xmlName' in metadata_type and metadata_type['xmlName'] == 'CustomObject':
                for object_type in metadata_type['children']:
                    if 'text' in object_type and object_type['text'].lower() == object_name.lower():
                        for attr in object_type['children']:
                            if 'text' in attr and attr['text'] == 'fields':
                                for field in attr['children']:
                                    _completions.append((field['text'], field['text']))
    return _completions

def get_symbol_table(class_name):
    try:
        if os.path.exists(os.path.join(mm_project_directory(), 'config', '.symbols')):
            class_name_json = os.path.basename(class_name).replace(".cls","json")
            if os.path.exists(os.path.join(mm_project_directory(), 'config', '.symbols', class_name_json+".json")):
                return parse_json_from_file(os.path.join(mm_project_directory(), "config", ".symbols", class_name_json+".json"))

        if not os.path.exists(os.path.join(mm_project_directory(), 'config', '.apex_file_properties')):
            return None

        apex_props = parse_json_from_file(os.path.join(mm_project_directory(), "config", ".apex_file_properties"))
        for p in apex_props.keys():
            if p == class_name+".cls" and 'symbolTable' in apex_props[p]:
                return apex_props[p]['symbolTable']
        return None
    except:
        return None

def get_completions_for_inner_class(symbol_table):
    return get_symbol_table_completions(symbol_table)

def get_symbol_table_completions(symbol_table):
    completions = []
    if 'constructors' in symbol_table:
        for c in symbol_table['constructors']:
            params = []
            if not 'visibility' in c:
                c['visibility'] = 'PUBLIC'
            if 'parameters' in c and type(c['parameters']) is list and len(c['parameters']) > 0:
                for p in c['parameters']:
                    params.append(p["type"] + " " + p["name"])
                paramStrings = []
                for i, p in enumerate(params):
                    paramStrings.append("${"+str(i+1)+":"+params[i]+"}")
                paramString = ", ".join(paramStrings)
                completions.append((c["visibility"] + " " + c["name"]+"("+", ".join(params)+")", c["name"]+"("+paramString+")"))
            else:
                completions.append((c["visibility"] + " " + c["name"]+"()", c["name"]+"()${1:}"))
    if 'properties' in symbol_table:
        for c in symbol_table['properties']:
            if not 'visibility' in c:
                c['visibility'] = 'PUBLIC'
            if "type" in c and c["type"] != None and c["type"] != "null":
                completions.append((c["visibility"] + " " + c["name"] + "\t" + c["type"], c["name"]))
            else:
                completions.append((c["visibility"] + " " + c["name"], c["name"]))
    if 'methods' in symbol_table:
        for c in symbol_table['methods']:
            params = []
            if not 'visibility' in c:
                c['visibility'] = 'PUBLIC'
            if 'parameters' in c and type(c['parameters']) is list and len(c['parameters']) > 0:
                for p in c['parameters']:
                    params.append(p["type"] + " " + p["name"])
            if len(params) == 1:
                completions.append((c["visibility"] + " " + c["name"]+"("+", ".join(params)+") \t"+c['returnType'], c["name"]+"(${1:"+", ".join(params)+"})"))
            elif len(params) > 1:
                paramStrings = []
                for i, p in enumerate(params):
                    paramStrings.append("${"+str(i+1)+":"+params[i]+"}")
                paramString = ", ".join(paramStrings)
                completions.append((c["visibility"] + " " + c["name"]+"("+", ".join(params)+") \t"+c['returnType'], c["name"]+"("+paramString+")"))
            else:
                completions.append((c["visibility"] + " " + c["name"]+"("+", ".join(params)+") \t"+c['returnType'], c["name"]+"()${1:}"))
    if 'innerClasses' in symbol_table:
        for c in symbol_table["innerClasses"]:
            if 'constructors' in c and len(c['constructors']) > 0:
                for con in c['constructors']:
                    if not 'visibility' in con:
                        con['visibility'] = 'PUBLIC'
                    params = []
                    if 'parameters' in con and type(con['parameters']) is list and len(con['parameters']) > 0:
                        for p in con['parameters']:
                            params.append(p["type"] + " " + p["name"])
                        paramStrings = []
                        for i, p in enumerate(params):
                            paramStrings.append("${"+str(i+1)+":"+params[i]+"}")
                        paramString = ", ".join(paramStrings)
                        completions.append((con["visibility"] + " " + con["name"]+"("+", ".join(params)+")", c["name"]+"("+paramString+")"))
                    else:
                        completions.append((con["visibility"] + " " + con["name"]+"()", c["name"]+"()${1:}"))
            else:
                completions.append(("INNER CLASS " + c["name"]+"() \t", c["name"]+"()${1:}"))
    return sorted(completions)

#returns suggestions based on tooling api symbol table
def get_apex_completions(search_name, search_name_extra=None):
    debug('Attempting to get completions')
    debug('search_name: ',search_name)
    debug('search_name_extra: ',search_name_extra)

    if os.path.exists(os.path.join(mm_project_directory(), 'config', '.symbols')):
        #class_name_json = os.path.basename(class_name).replace(".cls","json")
        if os.path.exists(os.path.join(mm_project_directory(), 'config', '.symbols', search_name+".json")):
            symbol_table = parse_json_from_file(os.path.join(mm_project_directory(), "config", ".symbols", search_name+".json"))
            if search_name_extra == None or search_name_extra == '':
                return get_symbol_table_completions(symbol_table)
            elif 'innerClasses' in symbol_table and len(symbol_table['innerClasses']) > 0:
                for inner in symbol_table['innerClasses']:
                    if inner["name"] == search_name_extra:
                        return get_completions_for_inner_class(inner)

    if not os.path.exists(os.path.join(mm_project_directory(), 'config', '.apex_file_properties')):
        return []

    apex_props = parse_json_from_file(os.path.join(mm_project_directory(), "config", ".apex_file_properties"))

    for p in apex_props.keys():
        if p == search_name+".cls" and 'symbolTable' in apex_props[p] and apex_props[p]["symbolTable"] != None:
            symbol_table = apex_props[p]['symbolTable']
            if search_name_extra == None or search_name_extra == '':
                return get_symbol_table_completions(symbol_table)
            elif 'innerClasses' in symbol_table and len(symbol_table['innerClasses']) > 0:
                for inner in symbol_table['innerClasses']:
                    if inner["name"] == search_name_extra:
                        return get_completions_for_inner_class(inner)

    debug('no symbol table found for '+search_name)

def get_version_number():
    try:
        json_data = open(os.path.join(config.mm_dir,"packages.json"))
        data = json.load(json_data)
        json_data.close()
        version = data["packages"][0]["platforms"]["osx"][0]["version"]
        return version
    except:
        return ''
