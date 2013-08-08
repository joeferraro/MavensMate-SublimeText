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
import re

__DEBUG = False
if __DEBUG:
    __indent = ""
    def debug(func):
        import time
        def __wrapped(*args):
            global __indent
            s = time.time()
            __indent += "\t"
            ret = func(*args)
            e = time.time()
            __indent = __indent[:-1]
            print("%s%s took %f ms" % (__indent, func.__name__, 1000*(e-s)))
            return ret
        return __wrapped
else:
    def debug(func):
        return func

@debug
def count_brackets(data):
    even = 0
    for i in range(len(data)):
        if data[i] == '{':
            even += 1
        elif data[i] == '}':
            even -= 1
    return even


@debug
def collapse_generic(before, open, close):
    i = len(before)
    count = 0
    end = -1
    min = 0
    while i >= 0:
        a = before.rfind(open, 0, i)
        b = before.rfind(close, 0, i)
        i = max(a, b)
        if i == -1:
            break
        if before[i] == close:
            count += 1
            if end == -1:
                end = i
        elif before[i] == open:
            count -= 1
            if count < min:
                min = count

        if count == min and end != -1:
            before = "%s%s" % (before[:i+1], before[end:])
            end = -1
    return before


@debug
def collapse_brackets(before):
    return collapse_generic(before, "{", "}")


@debug
def collapse_parenthesis(before):
    return collapse_generic(before, '(', ')')


@debug
def collapse_square_brackets(before):
    return collapse_generic(before, '[', ']')


@debug
def collapse_ltgt(before):
    i = len(before)
    count = 0
    end = -1
    min = 0
    while i >= 0:
        a = before.rfind(">", 0, i)
        b = before.rfind("<", 0, i)
        i = max(a, b)
        if i == -1:
            break
        if before[i] == '>':
            collapse = True
            if i > 0 and before[i-1] == '>':
                # Don't want to collapse a statement such as 'std::cout << "hello world!!" << std::endl;
                data = before[:i-1]
                match = re.search(r"([\w\s,.:<]+)$", data)
                if match:
                    if match.group(1).count("<") < 2:
                        collapse = False
                else:
                    collapse = False

            if not collapse or before[i-1] == '-' or \
                    (before[i-1] == ' ' and i >=2 and before[i-2] != '>'):
                i -= 1
            else:
                count += 1
                if end == -1:
                    end = i
        elif before[i] == '<':
            if i > 0 and (before[i-1] == '<' or before[i-1] == ' '):
                i -= 1
            else:
                count -= 1
                if count == min and end != -1:
                    before = "%s%s" % (before[:i+1], before[end:])
                    end = -1
                if count < min:
                    min = count
    return before


@debug
def collapse_strings(before):
    i = len(before)
    count = 0
    end = -1
    while i >= 0:
        i = before.rfind("\"", 0, i)
        if i == -1:
            break
        if before[i] == '\"':
            if i > 0 and before[i-1] == '\\':
                i -= 1
            elif count > 0:
                before = "%s%s" % (before[:i+1], before[end:])
                count = 0
            else:
                count += 1
                end = i
    return before


@debug
def extract_completion(before):
    before = collapse_parenthesis(before)
    before = collapse_square_brackets(before)
    before = collapse_ltgt(before)
    before = before.split("\n")[-1]
    before = before.split(";")[-1]
    before = re.sub(r"^\s+", r"", before)
    ret = ""
    while True:
        match = re.search(r"((\.|\->)?([^|.,\ \[\]\(\)\t]+(\(\)|\[\])*)(\.|\->))$", before)
        if not match:
            break
        ret = match.group(3) + match.group(5) + ret
        before = before[:-len(match.group(3))-len(match.group(5))].strip()

    return ret

@debug
def extract_completion_objc(before):
    before = collapse_parenthesis(before)
    before = before.split("\n")[-1]
    before = before.split(";")[-1]
    before = re.sub(r"^\s+", r"", before)
    ret = ""
    while True:
        match = re.search(r"([\w\[\]\.\-> ]+([ \t]+|->|.))$", before)
        if not match:
            match = re.search(r"([\w\[\]]+\s+)$", before)
        if not match:
            break
        ret = match.group(1) + ret
        before = before[:-len(match.group(1))]
    return ret

_keywords = ["return", "new", "delete", "class", "define", "using", "void", "template", "public:", "protected:", "private:", "public", "private", "protected", "typename", "in", "case", "default", "goto", "typedef", "struct", "else"]


@debug
def extract_package(data):
    data = remove_preprocessing(data)
    match = re.search(r"package\s([\w.]+);", data)
    if match:
        return match.group(1)
    return None


@debug
def extract_used_namespaces(data):
    regex = re.compile(r"\s*using\s+(namespace\s+)?([^;]+)", re.MULTILINE)
    ret = []
    for match in regex.finditer(data):
        toadd = match.group(2)
        if match.group(1) == None:
            toadd = toadd[:toadd.rfind("::")]
        ret.append(toadd)
    return ret


@debug
def extract_namespace(data):
    data = remove_preprocessing(data)
    data = collapse_brackets(data)
    data = remove_namespaces(data)
    regex = re.compile(r"namespace\s+([^{\s]+)\s*\{", re.MULTILINE)
    ret = ""
    for match in regex.finditer(data):
        if len(ret):
            ret += "::"
        ret += match.group(1)
    if len(ret.strip()) == 0:
        ret = None
    if ret == None:
        data = remove_functions(data)
        regex = re.compile(r"(\w+)::(\w+)::")
        match = regex.search(data)
        if match:
            ret = match.group(1)
    return ret

@debug
def extract_class_from_function(data):
    data = remove_preprocessing(data)
    data = collapse_brackets(data)
    data = collapse_parenthesis(data)
    data = remove_functions(data)
    ret = None
    for match in re.finditer(r"(.*?)(\w+)::~?(\w+)\s*\(\)(\s+const)?[^{};]*\{", data, re.MULTILINE):
        ret = match.group(2)

    return ret


@debug
def extract_class(data):
    data = remove_preprocessing(data)
    data = collapse_brackets(data)
    data = collapse_strings(data)
    data = remove_classes(data)
    regex = re.compile(r"class\s+([^;{\s:]+)\s*(:|;|\{|extends|implements)", re.MULTILINE)
    ret = None
    for match in regex.finditer(data):
        ret = match.group(1)
    if ret == None and "@implementation" in data:
        regex = re.compile(r"@implementation\s+(\w+)", re.MULTILINE)
        for match in regex.finditer(data):
            ret = match.group(1)
    return ret


@debug
def extract_inheritance(data, classname):
    data = remove_preprocessing(data)
    data = collapse_brackets(data)
    data = remove_classes(data)
    regex = re.compile(r"class\s+%s\s*(:|extends)\s+([^\s,{]+)" % classname, re.MULTILINE)
    match = regex.search(data)
    if match != None:
        return match.group(2)
    return None


@debug
def remove_classes(data):
    regex = re.compile(r"class\s+[^{]+{\}\s*;?", re.MULTILINE)
    return regex.sub("", data)


@debug
def remove_functions(data):
    # First remove for-loops
    data = sub(r"""(?:\s|^)for\s*\([^;{}]*;[^;{}]*;[^{}]*\)\s*\{\}""", data)
    regex = sub(r"""(?x)
            (?:[^\s,{};()]+\s+)?            # Possible return type. Optional because it will then
                                            # remove # while loops, preprocessor macros, constructors,
                                            # destructors, etc
            [^\s,;{}]+\s*\([^{};]*\)        # function name + possible space + parenthesis
            [^;{]*                          # Any extras like initializers, const, etc
            \{\}""", data)
    return regex


@debug
def remove_namespaces(data):
    regex = re.compile(r"\s*namespace\s+[^{]+\s*\{\}\s*", re.MULTILINE)
    return regex.sub("", data)


@debug
def sub(exp, data):
    regex = re.compile(exp, re.MULTILINE|re.DOTALL)
    while True:
        olddata = data
        data = regex.sub("", data)
        if olddata == data:
            break
    return data


@debug
def remove_preprocessing(data):
    data = data.replace("\\\n", " ")
    data = sub(r"\#\s*define[^\n]+\n", data)
    data = sub(r"\#\s*(ifndef|ifdef|if|endif|else|elif|pragma|include)[^\n]*\n", data)
    data = sub(r"//[^\n]+\n", data)
    data = sub(r"/\*.*?\*/", data)
    return data


@debug
def remove_includes(data):
    regex = re.compile(r"""\#\s*include\s+(<|")[^>"]+(>|")""")
    while True:
        old = data
        data = regex.sub("", data)
        if old == data:
            break
    return data

_invalid = r"""\(\s\{,\*\&\-\+\/;=%\)\"!"""
_endpattern = r"\;|,|\)|=|\[|\(\)\s*\;|:\s+"


@debug
def patch_up_variable(origdata, data, origtype, var, ret):
    type = origtype
    var = re.sub(r"\s*=\s*[^;,\)]+", "", var)
    curlybracere = re.compile(r"\s*(\S+)\s*({})\s*(\S*)", re.MULTILINE)
    for var in var.split(","):
        var = var.strip()
        pat = r"%s\s*([^;{]*)%s\s*(%s)" % (re.escape(origtype), re.escape(var), _endpattern)
        end = re.search(pat, data)
        if end.group(2) == "[":
            type += re.search(r"([\[\]]+)", data[end.start():]).group(1)
        i = var.find("[]")
        if i != -1:
            type += var[i:]
            var = var[:i]
        if "<" in type and ">" in type:
            s = r"(%s.+%s)(const)?[^{};]*(%s)" % (type[:type.find("<")+1], type[type.find(">"):], var)
            regex = re.compile(s)
            match = None
            for m in regex.finditer(origdata):
                match = m
            type = match.group(1)
        match = curlybracere.search(var)
        if match:
            if match.group(3):
                var = match.group(3)
                type += " %s" % match.group(1)
            else:
                var = match.group(1)
        ret.append((type, var))

@debug
def extract_variables(data):
    origdata = data

    data = remove_preprocessing(data)
    data = remove_includes(data)
    data = collapse_brackets(data)
    data = collapse_square_brackets(data)
    data = collapse_ltgt(data)
    data = remove_functions(data)
    data = remove_namespaces(data)
    data = remove_classes(data)
    data = re.sub(r"\([^)]*?\)\s*(?=;)", "()", data, re.MULTILINE)
    data = re.sub(r"\s*case\s+[\w:]*[^:]:[^:]", "", data, re.MULTILINE)
    data = re.sub(r"\s*default:\s*", "", data, re.MULTILINE)
    data = re.sub(r"template\s*<>", "", data, re.MULTILINE)
    data = re.sub(r"\s{2,}", " ", data, re.MULTILINE)

    # first get any variables inside of the function declaration
    funcdata = ";".join(re.findall(r"\(([^)]+\))", data, re.MULTILINE))
    pattern = r"\s*((static\s*)?(struct\s*)?\b(const\s*)?[^%s]+[\s*&]+(const)?[\s*&]*)(\b[^%s]+)\s*(?=,|\)|=)" % (_invalid, _invalid)
    funcvars = re.findall(pattern, funcdata, re.MULTILINE)
    ret = []
    for m in funcvars:
        type = get_base_type(m[0])
        if type in _keywords:
            continue
        patch_up_variable(origdata, data, m[0].strip(), m[5].strip(), ret)

    # Next, take care of all other variables
    data = collapse_parenthesis(data)

    pattern = r"""(?x)
        (^|,|\(|;|\{)\s*
            (
                (static\s*)?
                (struct\s*)?
                \b(const\s*)?\b
                [^%s]+
                [\s*&]+
                (const)?
                [\s*&]*
            )                   # type name
            (\b[^;()]+)\s*      # variable name
            (?=%s)""" % (_invalid, _endpattern)
    regex = re.compile(pattern, re.MULTILINE)

    for m in regex.finditer(data):
        if m.group(2) == None:
            continue
        type = get_base_type(m.group(2))
        if type in _keywords:
            continue
        type = m.group(2).strip()
        var = m.group(7).strip()
        patch_up_variable(origdata, data, type, var, ret)
    return ret


@debug
def dereference(typename):
    if "*" in typename:
        return typename.replace("*", "", 1)
    elif "[]" in typename:
        return typename.replace("[]", "", 1)
    return typename


@debug
def is_pointer(typename):
    return "*" in typename or "[]" in typename


@debug
def get_pointer_level(typename):
    return typename.count("*") + typename.count("[]")


@debug
def get_base_type(data):
    data = re.sub(r"(\s+|^)const(\s|$)", " ", data)
    data = re.sub(r"(\s|^)static(\s|$)", " ", data)
    data = re.sub(r"(\s+|^)struct(\s|$)", " ", data)
    data = data.strip()
    data = data.replace("&", "").replace("*", "").replace("[]", "")
    data = data.strip()
    return data


@debug
def get_var_type(data, var):
    regex = re.compile(r"(const\s*)?\b([^%s]+[ \s\*\&]+)(\s*[^%s]+\,\s*)*(%s)\s*(\[|\(|\;|,|\)|=|:|in\s+)" % (_invalid, _invalid, re.escape(var)), re.MULTILINE)
    origdata = data
    data = remove_preprocessing(data)
    data = collapse_ltgt(data)
    data = collapse_brackets(data)
    data = remove_functions(data)

    match = None

    for m in regex.finditer(data):
        t = m.group(2).strip()
        if t in _keywords:
            continue
        match = m
    if match and match.group(2):
        type = match.group(2)
        if match.group(1):
            type = match.group(1) + type
        pat = r"(%s)([^%s]+,\s*)*(%s)" % (re.escape(type), _invalid, re.escape(match.group(4)))
        regex = re.compile(pat)
        for m in regex.finditer(data):
            match = m
        key = get_base_type(match.group(1))
        if "<>" in key:
            key = match.group(1)
            name = key[:key.find("<")]
            end = key[key.find(">")+1:]
            regex = re.compile(r"(%s<.+>%s\s*)([^%s]+,\s*)*(%s)" % (name, end, _invalid, var))
            match = None
            for m in regex.finditer(origdata):
                key = get_base_type(m.group(1))
                if key in _keywords:
                    continue
                match = m
            if match:
                data = origdata[match.start(1):match.end(1)]
                i = len(data)-1
                count = 0
                while i > 0:
                    a = data.rfind(">", 0, i)
                    b = data.rfind("<", 0, i)
                    i = max(a, b)
                    if i == -1:
                        break
                    if data[i] == ">":
                        count += 1
                    elif data[i] == "<":
                        count -= 1
                        if count == 0:
                            data = data[i:]
                            break
                regex = re.compile(r"(%s%s)([^%s]+,\s*)*(%s)" % (name, data, _invalid, var))
                for m in regex.finditer(origdata):
                    match = m
    else:
        match = None

    if match and match.group(1):
        # Just so that it reports the correct location in the file
        pat = r"(%s)([^%s],)*(%s)\s*(\[|\(|\;|,|\)|=)" % (re.escape(match.group(1)), _invalid, re.escape(match.group(3)))
        regex = re.compile(pat)
        for m in regex.finditer(origdata):
            match = m
    return match


@debug
def remove_empty_classes(data):
    data = sub(r"\s*class\s+[^\{]+\s*\{\}", data)
    return data


@debug
def get_var_tocomplete(iter, data):
    var = None
    end = None
    tocomplete = ""
    for m in iter:
        if var != None and m.start(0) != end:
            var = None
            tocomplete = ""

        if len(tocomplete):
            tocomplete += m.group(1)
        tocomplete += m.group(2)
        if var == None:
            var = m.group(1)
        end = m.end(2)
    if "<>" in tocomplete:
        before = re.escape(tocomplete[:tocomplete.find("<")]).replace("\(\)", "\(.*?\)")
        after = re.escape(tocomplete[tocomplete.rfind(">")+1:]).replace("\(\)", "\(.*?\)")
        regex = re.compile(r"(%s<.+>%s)" % (before, after), re.MULTILINE)
        match = None
        for m in regex.finditer(data):
            match = m
        tocomplete = collapse_brackets(collapse_parenthesis(match.group(1)))
    return var, tocomplete


@debug
def get_type_definition(data):
    before = extract_completion(data)
    var, tocomplete = None, None
    objc = False
    if len(before) == 0 and "[" in data:
        before = extract_completion_objc(data)
        objc = True

    if not objc:
        var, tocomplete = get_var_tocomplete(re.finditer(r"(\w+(?:[^\.\-,+*/:]*))(\.|->|::|[ \t])", before), data)

    if var == None or objc:
        var, tocomplete = get_var_tocomplete(re.finditer(r"\[?([^ \.\-:]+)((?:[ \t]|\.|->|::).*)", before), data)
        var = re.sub(r"^\[*", "", var)

    extra = ""
    if var.endswith("[]"):
        extra = var[var.find("["):]
        var = var[:var.find("[")]

    if var == "this" or var == "self":
        clazz = extract_class(data)
        if clazz == None:
            clazz = extract_class_from_function(data)
        line = column = -1  # TODO
        return line, column, clazz, var, tocomplete
    elif var == "super":
        clazz = extract_class(data)
        if clazz:
            sup = extract_inheritance(data, clazz)
            return -1, -1, sup, var, tocomplete
    elif tocomplete.startswith("::"):
        return -1, -1, var, None, tocomplete
    else:
        match = get_var_type(data, var)
    if match == None:
        return -1, -1, var, None, extra+tocomplete

    line = data[:match.start(3)].count("\n") + 1
    column = len(data[:match.start(3)].split("\n")[-1])+1
    typename = match.group(1).strip()

    end = re.search(r"^\s*([^;,=\(\):]*)(;|,|=|\(|\)|:)", data[match.end(3):])
    if end and end.group(1).startswith("["):
        end = collapse_square_brackets(data[match.end(3)+end.start(1):match.end(3)+end.end(1)]).strip()
        typename += end

    return line, column, typename, var, extra+tocomplete


@debug
def template_split(data):
    if data == None:
        return None
    ret = []
    origdata = data
    data = collapse_ltgt(data)
    data = [a.strip() for a in data.split(",")]
    exp = ""
    for var in data:
        exp += r"(%s)\s*,?\s*" % (re.escape(var).replace("\\<\\>", "<.*>").strip())

    match = re.search(exp, origdata)
    ret = list(match.groups())

    return ret


@debug
def solve_template(typename):
    args = []
    template = re.search(r"([^<]+)(<(.+)>)?((::|.)(.+))?$", typename)
    args = template_split(template.group(3))
    if args:
        for i in range(len(args)):
            if "<" in args[i]:
                args[i] = solve_template(args[i])
            else:
                args[i] = (args[i], None)
    if template.group(6):
        return template.group(1), args, solve_template(template.group(6))
    return template.group(1), args


@debug
def make_template(data, concat="."):
    if data[1] != None:
        ret = ""
        for param in data[1]:
            sub = make_template(param, concat)
            if len(ret):
                ret += ", "
            ret += sub
        temp = "%s<%s%s>" % (data[0], ret, ' ' if ret[-1] == '>' else '')
        if len(data) == 3:
            temp += concat + make_template(data[2], concat)
        return temp
    return data[0]


@debug
def extract_line_until_offset(data, offset):
    return data[:offset+1].split("\n")[-1]


@debug
def extract_line_at_offset(data, offset):
    if offset < 0 or offset >= len(data) or data[offset] == "\n":
        return ""
    line = data[:offset+1].count("\n")
    return data.split("\n")[line]


@debug
def extract_word_at_offset(data, offset):
    line, column = get_line_and_column_from_offset(data, offset)
    line = extract_line_at_offset(data, offset)
    begin = 0
    end = 0
    match = re.search(r"\b\w*$", line[0:column])
    if match:
        begin = match.start()
    else:
        return ""
    match = re.search(r"^\w*", line[begin:])
    if match:
        end = begin+match.end()
    word = line[begin:end]
    return word


@debug
def extract_extended_word_at_offset(data, offset):
    line, column = get_line_and_column_from_offset(data, offset)
    line = extract_line_at_offset(data, offset)
    match = re.search(r"^\w*", line[column:])
    if match:
        column = column + match.end()
    extword = line[0:column]
    return extword


@debug
def get_line_and_column_from_offset(data, offset):
    data = data[:offset].split("\n")
    line = len(data)
    column = len(data[-1]) + 1
    return line, column


@debug
def get_offset_from_line_and_column(data, line, column):
    data = data.split("\n")
    if line == 1:
        column -= 1
    offset = len("\n".join(data[:line-1])) + column
    return offset
