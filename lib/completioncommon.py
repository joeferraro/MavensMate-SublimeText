"""
Copyright (c) 2012 Fredrik Ehnbom

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.

   2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.

   3. This notice may not be removed or altered from any source
   distribution.
"""
import sublime
import sublime_plugin
import re
import subprocess
import time
try:
    import Queue
except:
    import queue as Queue
import threading
import os
import os.path
import imp
import sys

def reload(mod):
    n = mod.__file__
    if n[-1] == 'c':
        n = n[:-1]
    globals()[mod.__name__] = imp.load_source(mod.__name__, n)

parsehelp = imp.load_source("parsehelp", os.path.join(os.path.dirname(os.path.abspath(__file__)), "parsehelp.py"))
reload(parsehelp)
language_regex = re.compile("(?<=source\.)[\w+\-#]+")
member_regex = re.compile("(([a-zA-Z_]+[0-9_]*)|([\)\]])+)(\.)$")


class CompletionCommonDotComplete(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            self.view.insert(edit, region.end(), ".")
        caret = self.view.sel()[0].begin()
        line = self.view.substr(sublime.Region(self.view.word(caret-1).a, caret))
        if member_regex.search(line) != None:
            self.view.run_command("hide_auto_complete")
            sublime.set_timeout(self.delayed_complete, 1)

    def delayed_complete(self):
        self.view.run_command("auto_complete")


class CompletionCommon(object):

    def __init__(self, settingsfile, workingdir):
        self.settingsfile = settingsfile
        self.completion_proc = None
        self.completion_cmd = None
        self.data_queue = Queue.Queue()
        self.workingdir = workingdir
        self.debug = False

    def get_settings(self):
        return sublime.load_settings(self.settingsfile)

    def get_setting(self, key, default=None):
        try:
            s = sublime.active_window().active_view().settings()
            if s.has(key):
                return s.get(key)
        except:
            pass
        return self.get_settings().get(key, default)

    def expand_path(self, value, window=None, checkExists=True):
        if window == None:
            # Views can apparently be window less, in most instances getting
            # the active_window will be the right choice (for example when
            # previewing a file), but the one instance this is incorrect
            # is during Sublime Text 2 session restore. Apparently it's
            # possible for views to be windowless then too and since it's
            # possible that multiple windows are to be restored, the
            # "wrong" one for this view might be the active one and thus
            # ${project_path} will not be expanded correctly.
            #
            # This will have to remain a known documented issue unless
            # someone can think of something that should be done plugin
            # side to fix this.
            window = sublime.active_window()

        get_existing_files = \
            lambda m: [path \
                for f in window.folders() \
                for path in [os.path.join(f, m.group('file'))] \
                if checkExists and os.path.exists(path) or not checkExists
            ]
        value = re.sub(r'\${project_path:(?P<file>[^}]+)}', lambda m: len(get_existing_files(m)) > 0 and get_existing_files(m)[0] or m.group('file'), value)
        value = re.sub(r'\${env:(?P<variable>[^}]+)}', lambda m: os.getenv(m.group('variable')) if os.getenv(m.group('variable')) else "%s_NOT_SET" % m.group('variable'), value)
        value = re.sub(r'\${home}', os.getenv('HOME') if os.getenv('HOME') else "HOME_NOT_SET", value)
        value = re.sub(r'\${folder:(?P<file>[^}]+)}', lambda m: os.path.dirname(m.group('file')), value)
        value = value.replace('\\', '/')

        return value

    def get_cmd(self):
        return None

    def show_error(self, msg):
        sublime.error_message(msg)

    def __err_func(self):
        exc = self.__curr_exception
        sublime.set_timeout(lambda: self.show_error(exc), 0)
        self.__curr_exception = None

    def error_thread(self):
        try:
            err_re = re.compile(r"^(Error|Exception)(\s+caught)?:\s+")
            stack_re = re.compile(r".*\(.*\)$")
            self.__curr_exception = None
            while True:
                if self.completion_proc.poll() != None:
                    break
                line = self.completion_proc.stderr.readline().decode(sys.getdefaultencoding())
                if line:
                    line = line.strip()
                else:
                    line = ""
                if err_re.search(line):
                    self.__curr_exception = line
                elif self.__curr_exception:
                    if line != ";;--;;":
                        self.__curr_exception += "\n\t" + line
                    else:
                        self.__err_func()
                if self.debug:
                    print("stderr: %s" % (line))
        finally:
            pass

    def completion_thread(self):
        try:
            while True:
                if self.completion_proc.poll() != None:
                    break
                read = self.completion_proc.stdout.readline().strip().decode(sys.getdefaultencoding())
                if read:
                    self.data_queue.put(read)
                    if self.debug:
                        print("stdout: %s" % read)
        finally:
            #print("completion_proc: %d" % (completion_proc.poll()))
            self.data_queue.put(";;--;;")
            self.data_queue.put(";;--;;exit;;--;;")
            self.completion_cmd = None
            #print("no longer running")

    def run_completion(self, cmd, stdin=None):
        self.debug = self.get_setting("completioncommon_debug", False)
        realcmd = self.get_cmd()
        if not self.completion_proc or realcmd != self.completion_cmd or self.completion_proc.poll() != None:
            if self.completion_proc:
                if self.completion_proc.poll() == None:
                    self.completion_proc.stdin.write("-quit\n")
                while self.data_queue.get() != ";;--;;exit;;--;;":
                    continue

            self.completion_cmd = realcmd
            self.completion_proc = subprocess.Popen(
                realcmd,
                cwd=self.workingdir,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
                )
            t = threading.Thread(target=self.completion_thread)
            t.start()
            t = threading.Thread(target=self.error_thread)
            t.start()
        towrite = cmd + "\n"
        if stdin:
            towrite += stdin + "\n"
        if self.debug:
            for line in towrite.split("\n"):
                print("stdin: %s" % line)
        self.completion_proc.stdin.write(towrite.encode(sys.getdefaultencoding()))
        stdout = ""
        while True:
            try:
                read = self.data_queue.get(timeout=5.0)
                if read == None:
                    # We timed out... Try forcing the process to restart
                    # which might possibly help with out of sync issues
                    self.completion_cmd = None

                if read == ";;--;;" or read == None:
                    break
                stdout += read+"\n"
            except:
                break
        return stdout

    def get_language(self, view=None):
        if view == None:
            view = sublime.active_window().active_view()
        caret = view.sel()[0].a
        scope = view.scope_name(caret).strip()
        language = language_regex.search(scope)
        if language == None:
            if scope.endswith("jsp"):
                return "jsp"
            return None
        return language.group(0)

    def is_supported_language(self, view):
        return False

    def get_packages(self, data, thispackage, type):
        return []

    def find_absolute_of_type(self, data, full_data, type, template_args=[]):
        thispackage = re.search("[ \t]*package (.*);", data)
        if thispackage is None:
            thispackage = ""
        else:
            thispackage = thispackage.group(1)
        sepchar = "$"
        if self.get_language() == "cs":
            sepchar = "+"
            thispackage = re.findall(r"\s*namespace\s+([\w\.]+)\s*{", parsehelp.remove_preprocessing(data), re.MULTILINE)
            thispackage = ".".join(thispackage)

        match = re.search(r"class %s(\s|$)" % type, full_data)
        if not match is None:
            # This type is defined in this file so figure out the nesting
            full_data = parsehelp.remove_empty_classes(parsehelp.collapse_brackets(parsehelp.remove_preprocessing(full_data[:match.start()])))
            regex = re.compile(r"\s*class\s+([^\s{]+)(?:\s|$)")
            add = ""
            for m in re.finditer(regex, full_data):
                if len(add):
                    add = "%s%s%s" % (add, sepchar, m.group(1))
                else:
                    add = m.group(1)

            if len(add):
                type = "%s%s%s" % (add, sepchar, type)
            # Class is defined in this file, return package of the file
            if len(thispackage) == 0:
                return type
            return "%s.%s" % (thispackage, type)

        packages = self.get_packages(data, thispackage, type)
        packages.append(";;--;;")

        output = self.run_completion("-findclass;;--;;%s" % (type), "\n".join(packages)).strip()
        if len(output) == 0 and "." in type:
            return self.find_absolute_of_type(data, full_data, type.replace(".", sepchar), template_args)
        return output

    def complete_class(self, absolute_classname, prefix, template_args=""):
        stdout = self.run_completion("-complete;;--;;%s;;--;;%s%s%s" % (absolute_classname, prefix, ";;--;;" if len(template_args) else "", template_args))
        stdout = stdout.split("\n")[:-1]
        members = [tuple(line.split(";;--;;")) for line in stdout]
        ret = []
        for member in members:
            if len(member) == 3:
                member = (member[0], member[1], int(member[2]))
            if member not in ret:
                ret.append(member)
        return sorted(ret, key=lambda a: a[0])

    def get_return_type(self, absolute_classname, prefix, template_args=""):
        #print(absolute_classname)
        #print(prefix)
        #print(template_args)
        stdout = self.run_completion("-returntype;;--;;%s;;--;;%s%s%s" % (absolute_classname, prefix, ";;--;;" if len(template_args) else "", template_args))
        ret = stdout.strip()
        match = re.search("(\[L)?([^;]+)", ret)
        if match:
            return match.group(2)
        return ret

    def patch_up_template(self, data, full_data, template):
        if template == None:
            return None
        ret = []
        for param in template:
            name = self.find_absolute_of_type(data, full_data, param[0], param[1])
            ret.append((name, self.patch_up_template(data, full_data, param[1])))
        return ret

    def return_completions(self, comp):
        if self.get_setting("completioncommon_inhibit_sublime_completions", True):
            return (comp, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
        return comp

    def is_static(self, mod):
        return (mod&(1<<0)) != 0

    def is_private(self, mod):
        return (mod&(1<<1)) != 0

    def is_protected(self, mod):
        return (mod&(1<<2)) != 0

    def is_public(self, mod):
        return (mod&(1<<3)) != 0

    def filter(self, typename, var, isstatic, data, indata):
        ret = []
        if len(indata) > 0 and len(indata[0]) == 2:
            # Filtering info not available
            return indata

        mypackage = None
        lang = self.get_language()
        if lang == "java" or lang == "jsp":
            mypackage = parsehelp.extract_package(data)
        else:
            mypackage = parsehelp.extract_namespace(data)
            if mypackage != None:
                mypackage = mypackage.replace("::", ".")
        if mypackage == None:
            mypackage = ""
        idx = typename.rfind(".")
        if idx == -1:
            idx = 0
        typepackage = typename[:idx]
        samepackage = mypackage == typepackage

        for disp, ins, mod in indata:
            public = self.is_public(mod)
            static = self.is_static(mod)
            accessible = public or (samepackage and not self.is_private(mod))

            if var == "this":
                ret.append((disp, ins))
            elif isstatic and static and accessible:
                ret.append((disp, ins))
            elif not isstatic and accessible:
                ret.append((disp, ins))
        return ret

    def on_query_completions(self, view, prefix, locations):
        bs = time.time()
        start = time.time()
        #if not self.is_supported_language(view):
        #    return []
        line = view.substr(sublime.Region(view.full_line(locations[0]).begin(), locations[0]))
        before = line
        if len(prefix) > 0:
            before = line[:-len(prefix)]
        if re.search("[ \t]+$", before):
            before = ""
        elif re.search("\.$", before):
            # Member completion
            data = view.substr(sublime.Region(0, locations[0]-len(prefix)))
            full_data = view.substr(sublime.Region(0, view.size()))
            typedef = parsehelp.get_type_definition(data)
            if typedef == None:
                return self.return_completions([])
            line, column, typename, var, tocomplete = typedef
            print('typedef: ', typedef)
            # TODO: doesn't understand arrays at the moment
            tocomplete = tocomplete.replace("[]", "")

            if typename is None:
                # This is for completing for example "System."
                # or "String." or other static calls/variables
                typename = var
                var = None
            start = time.time()
            template = parsehelp.solve_template(typename)
            if template[1]:
                template = template[1]
            else:
                template = ""
            template = self.patch_up_template(data, full_data, template)
            typename = re.sub("(<.*>)|(\[.*\])", "", typename)
            oldtypename = typename
            typename = self.find_absolute_of_type(data, full_data, typename, template)
            if typename == "":
                # Possibly a member of the current class
                clazz = parsehelp.extract_class(data)
                if clazz != None:
                    var = "this"
                    typename = self.find_absolute_of_type(data, full_data, clazz, template)
                    tocomplete = "." + oldtypename + tocomplete

            end = time.time()
            print("absolute is %s (%f ms)" % (typename, (end-start)*1000))
            if typename == "":
                return self.return_completions([])

            tocomplete = tocomplete[1:]  # skip initial .
            if len(tocomplete):
                # Just to make sure that the var isn't "this"
                # because in the end it isn't "this" we are
                # completing, but something else
                var = None

            isstatic = False
            if len(tocomplete) == 0 and var == None:
                isstatic = True
            start = time.time()
            idx = tocomplete.find(".")
            while idx != -1:
                sub = tocomplete[:idx]
                idx2 = sub.find("(")
                if idx2 >= 0:
                    sub = sub[:idx2]
                    count = 1
                    for i in range(idx+1, len(tocomplete)):
                        if tocomplete[i] == '(':
                            count += 1
                        elif tocomplete[i] == ')':
                            count -= 1
                            if count == 0:
                                idx = tocomplete.find(".", i)
                                break
                tempstring = ""
                if template:
                    for param in template:
                        if len(tempstring):
                            tempstring += ";;--;;"
                        tempstring += parsehelp.make_template(param)
                if "<" in sub and ">" in sub:
                    temp = parsehelp.solve_template(sub)
                    temp2 = self.patch_up_template(data, full_data, temp[1])
                    temp = (temp[0], temp2)
                    temp = parsehelp.make_template(temp)
                    sub = "%s%s" % (temp, sub[sub.rfind(">")+1:])

                n = self.get_return_type(typename, sub, tempstring)
                print("%s%s.%s = %s" % (typename, "<%s>" % tempstring if len(tempstring) else "", sub, n))
                if len(n) == 0:
                    return self.return_completions([])
                n = parsehelp.get_base_type(n)
                template = parsehelp.solve_template(n)
                typename = template[0]
                if self.get_language() == "cs" and len(template) == 3:
                    typename += "`%d+%s" % (len(template[1]), parsehelp.make_template(template[2]))
                template = template[1]
                tocomplete = tocomplete[idx+1:]
                idx = tocomplete.find(".")
            end = time.time()
            print("finding what to complete took %f ms" % ((end-start) * 1000))

            template_args = ""
            if template:
                for param in template:
                    if len(template_args):
                        template_args += ";;--;;"
                    template_args += parsehelp.make_template(param)

            print("completing %s%s.%s" % (typename, "<%s>" % template_args if len(template_args) else "", prefix))
            start = time.time()
            ret = self.complete_class(typename, prefix, template_args)
            ret = self.filter(typename, var, isstatic, data, ret)
            end = time.time()
            print("completion took %f ms" % ((end-start)*1000))
            be = time.time()
            print("total %f ms" % ((be-bs)*1000))
            if self.get_setting("completioncommon_shorten_names", True):
                old = ret
                ret = []
                regex = re.compile("([\\w\\.]+\\.)*")
                for display, insert in old:
                    olddisplay = display
                    display = regex.sub("", display)
                    while olddisplay != display:
                        olddisplay = display
                        display = regex.sub("", display)
                    ret.append((display, insert))
            return self.return_completions(ret)
        return []

    def on_query_context(self, view, key, operator, operand, match_all):
        print('context')
        if key == "completion_common.is_code":
            caret = view.sel()[0].a
            scope = view.scope_name(caret).strip()
            return re.search("(string.)|(comment.)", scope) == None
