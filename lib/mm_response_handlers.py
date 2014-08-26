import sublime
import threading
import json
import pipes 
import subprocess
import os
import sys
import time
import html.parser
import re
import traceback
from .threads import ThreadTracker
from .threads import ThreadProgress
from .threads import PanelThreadProgress
from .printer import PanelPrinter
from .mm_merge import MavensMateDiffThread
import MavensMate.lib.command_helper as command_helper
import MavensMate.util as util
import MavensMate.config as config
sublime_version = int(float(sublime.version()))
settings = sublime.load_settings('mavensmate.sublime-settings')
html_parser = html.parser.HTMLParser()
debug = config.debug

class MMResultHandler(object):

    def __init__(self, context):
        self.operation           = context.get("operation", None)
        self.process_id          = context.get("process_id", None)
        self.printer             = context.get("printer", None)
        self.thread              = context.get("thread", None)
        self.result              = context.get("result", None)
        self.process_region      = self.printer.panel.find(self.process_id,0)
        self.status_region       = self.printer.panel.find('   Result: ',self.process_region.begin())

        self.isValidJSONResponse = True
        try:
            json_response = json.loads(self.result)
            self.result = json_response
        except:
            self.isValidJSONResponse = False

    def execute(self):
        #describe_object
        if self.result == None:
            self.__print_to_panel("[OPERATION FAILED]: No response from mm. Please enable logging (http://mavensmate.com/Plugins/Sublime_Text/Plugin_Logging) and post relevant log(s) to a new issue at https://github.com/joeferraro/MavensMate")
        else:
            try:
                if self.operation == 'compile' or self.operation == 'compile_project':
                    self.__handle_compile_response()
                elif self.operation == "test_async" or self.operation == "run_all_tests":
                    self.__handle_test_result()
                elif self.operation == "run_apex_script":
                    self.__handle_apex_script_result()
                elif self.operation == "new_metadata":
                    self.__handle_new_metadata()
                elif self.operation == "get_coverage":
                    self.__handle_coverage_result()
                elif self.operation == "coverage_report":
                    self.__handle_coverage_report_result()
                elif self.operation == "get_org_wide_test_coverage":
                    self.__handle_org_wide_coverage_result()
                elif self.operation == "delete":
                    self.__handle_delete_metadata_result()
                else:
                    self.__handle_generic_command_result()
            except:
                self.__print_result()

            self.__finish()

    def __handle_delete_metadata_result(self, **kwargs):
        debug("HANDLING DELETE!")
        debug(self.result)
        self.__handle_compile_response()

    def __handle_compile_response(self, **kwargs):  
        debug("HANDLING COMPILE!")
        debug(self.result)

        #diffing with server
        if 'actions' in self.result and util.to_bool(self.result['success']) == False:
            diff_merge_settings = config.settings.get('mm_diff_server_conflicts', False)
            if diff_merge_settings:
                if sublime.ok_cancel_dialog(self.result["body"], self.result["actions"][0].title()):
                    self.__print_to_panel("Diffing with server")
                    th = MavensMateDiffThread(self.thread.window, self.thread.view, self.result['tmp_file_path'])
                    th.start()
                else:
                    self.__print_to_panel(self.result["actions"][1].title())
            else:
                if sublime.ok_cancel_dialog(self.result["body"], "Overwrite Server Copy"):
                    self.__print_to_panel("Overwriting server copy")
                    self.thread.params['action'] = 'overwrite'
                    if kwargs.get("callback", None) != None:
                        sublime.set_timeout(lambda: self.callback('compile', params=self.thread.params), 100)   
                else:
                    self.__print_to_panel(self.result["actions"][1].title())
        else:
            try:
                if 'State' in self.result and self.result['State'] == 'Error' and 'ErrorMsg' in self.result:
                    self.__print_to_panel("[OPERATION FAILED]: {0}\n\n{1}".format(self.result['ErrorMsg'], 'If you are having difficulty compiling, try toggling the mm_compile_with_tooling_api setting to \'false\' or cleaning your project.'))
                elif 'State' in self.result and self.result['State'] == 'Failed' and ('CompilerErrors' in self.result or 'DeployDetails' in self.result):
                    #here we're parsing a response from the tooling endpoint
                    isLegacy = False #pre 30.0

                    if 'DeployDetails' in self.result: #31.0 and up
                        errors = self.result['DeployDetails']['componentFailures']
                        lineKey = 'lineNumber'
                        colKey = 'columnNumber'
                    else:
                        errors = json.loads(self.result['CompilerErrors'])
                        isLegacy = True
                        lineKey = 'line'
                        colKey = 'column'

                    if type(errors) is not list:
                        errors = [errors]
                    if len(errors) > 0:
                        for e in errors:
                            line_col = ""
                            line, col = 1, 1
                            if lineKey in e:
                                if type(e[lineKey]) is list:
                                    line = int(e[lineKey][0])
                                else:
                                    line = int(e[lineKey])
                                line_col = ' (Line: '+str(line)
                            if colKey in e:
                                if type(e[colKey]) is list:
                                    line = int(e[colKey][0])
                                else:
                                    col = int(e[colKey])
                                line_col += ', Column: '+str(col)
                            if len(line_col):
                                line_col += ')' 

                            #scroll to the line and column of the exception
                            #if settings.get('mm_compile_scroll_to_error', True):
                            #open file, if already open it will bring it to focus
                            #view = sublime.active_window().open_file(self.thread.active_file)
                            view = self.thread.view
                            pt = view.text_point(line-1, col-1)
                            view.sel().clear()
                            view.sel().add(sublime.Region(pt))
                            view.show(pt)
                            problem = e['problem']
                            if type(problem) is list:
                                problem = problem[0]
                            problem = html_parser.unescape(problem)
                            if isLegacy:
                                file_base_name = e['name']
                            else:
                                file_base_name = e['fileName']
                            if type(file_base_name) is list:
                                file_base_name = file_base_name[0]
                            #if self.thread.window.active_view().name():
                            current_active_view = sublime.active_window().active_view()
                            if current_active_view.file_name() != None:
                                current_active_view_file_name = os.path.basename(current_active_view.file_name())
                                if "." in current_active_view_file_name:
                                    current_active_view_file_name = current_active_view_file_name.split(".")[0]
                                debug(current_active_view_file_name)
                                debug(file_base_name)
                                if current_active_view_file_name != file_base_name:
                                    #this is the tooling api throwing a compile error against a different file
                                    msg = "[COMPILE FAILED]: ({0}) {1} {2}".format(file_base_name, problem, line_col)
                                    msg += "\n\nThe Tooling API has failed to compile a separate element of metadata in your current MetadataContainer. You can either:"
                                    msg += "\n1. Fix the compilation error on "+file_base_name
                                    msg += "\n2. Reset your MetadataContainer to clear this error: MavensMate > Utilities > Reset MetadataContainer"
                                    self.__print_to_panel(msg)
                                elif current_active_view_file_name == file_base_name:
                                    util.mark_line_numbers(self.thread.view, [line], "bookmark")
                                    self.__print_to_panel("[COMPILE FAILED]: ({0}) {1} {2}".format(file_base_name, problem, line_col))
                    elif "ErrorMsg" in self.result:
                        msg = ''
                        if 'object has been modified on server' in self.result['ErrorMsg']:
                            msg = self.result['ErrorMsg'] + '. You may try resetting your MetadataContainer to clear this error: MavensMate > Utilities > Reset MetadataContainer.'
                        else:
                            msg = self.result['ErrorMsg']
                        self.__print_to_panel("[COMPILE FAILED]: {0}".format(msg))

                elif 'success' in self.result and util.to_bool(self.result['success']) == False and (('messages' in self.result or 'Messages' in self.result) or 'details' in self.result):
                    if 'details' in self.result and 'componentFailures' in self.result['details']:
                        self.result['messages'] = self.result['details'].pop('componentFailures')
                    elif 'Messages' in self.result:
                        self.result['messages'] = self.result.pop('Messages')
                    
                    #here we're parsing a response from the metadata endpoint
                    failures = None
                    messages = self.result['messages']
                    if type( messages ) is not list:
                        messages = [messages]

                    problems = 0
                    for m in messages:
                        if 'problem' in m:
                            problems += 1
                            break

                    if problems == 0: #must not have been a compile error, must be a test run error
                        if 'runTestResult' in self.result:
                            if 'runTestResult' in self.result and 'failures' in self.result['runTestResult'] and type( self.result['runTestResult']['failures'] ) == list:
                                failures = self.result['runTestResult']['failures']
                            elif 'failures' in self.result['runTestResult']:
                                failures = [self.result['runTestResult']['failures']]
                            
                            if failures != None:
                                msg = ' [DEPLOYMENT FAILED]:'
                                for f in failures: 
                                    msg += f['name'] + ', ' + f['methodName'] + ': ' + f['message'] + '\n'
                                    self.__print_to_panel(msg)
                        elif 'run_test_result' in self.result:
                            if 'run_test_result' in self.result and 'failures' in self.result['run_test_result'] and type( self.result['run_test_result']['failures'] ) == list:
                                failures = self.result['run_test_result']['failures']
                            elif 'failures' in self.result['run_test_result']:
                                failures = [self.result['run_test_result']['failures']]
                            
                            if failures != None:
                                msg = ' [DEPLOYMENT FAILED]:'
                                for f in failures: 
                                    msg += f['name'] + ', ' + f['methodName'] + ': ' + f['message'] + '\n'
                                self.__print_to_panel(msg)
                    else: #compile error, build error message
                        msg = ""
                        for m in messages:
                            if "success" in m and m["success"] == False:
                                line_col = ""
                                if 'lineNumber' in m:
                                    line_col = ' (Line: '+m['lineNumber']
                                    util.mark_line_numbers(self.thread.view, [int(float(m['lineNumber']))], "bookmark")
                                if 'columnNumber' in m:
                                    line_col += ', Column: '+m['columnNumber']
                                if len(line_col) > 0:
                                    line_col += ')'
                                filename = m['fileName']
                                filename = re.sub(r'unpackaged/[A-Z,a-z]*/', '', filename)
                                msg += filename + ': ' + m['problem'] + line_col + "\n"

                        self.__print_to_panel('[DEPLOYMENT FAILED]: ' + msg)
                        
                elif 'success' in self.result and self.result["success"] == False and 'line' in self.result:
                    #this is a response from the apex compile api
                    line_col = ""
                    line, col = 1, 1
                    if 'line' in self.result:
                        line = int(self.result['line'])
                        line_col = ' (Line: '+str(line)
                        util.mark_line_numbers(self.thread.view, [line], "bookmark")
                    if 'column' in self.result:
                        col = int(self.result['column'])
                        line_col += ', Column: '+str(col)
                    if len(line_col):
                        line_col += ')'

                    #scroll to the line and column of the exception
                    if settings.get('mm_compile_scroll_to_error', True):
                        #open file, if already open it will bring it to focus
                        #view = sublime.active_window().open_file(self.thread.active_file)
                        view = self.thread.view
                        pt = view.text_point(line-1, col-1)
                        view.sel().clear()
                        view.sel().add(sublime.Region(pt))
                        view.show(pt)

                        self.__print_to_panel('[COMPILE FAILED]: ' + self.result['problem'] + line_col)
                elif 'success' in self.result and util.to_bool(self.result['success']) == True and 'Messages' in self.result and len(self.result['Messages']) > 0:
                    msg = ' [Operation completed Successfully - With Compile Errors]\n'
                    msg += '[COMPILE ERRORS] - Count:\n'
                    for m in self.result['Messages']:
                        msg += ' FileName: ' + m['fileName'] + ': ' + m['problem'] + 'Line: ' + m['lineNumber']
                    self.__print_to_panel(msg)
                elif 'success' in self.result and util.to_bool(self.result['success']) == True:
                    self.__print_to_panel("Success")
                elif 'success' in self.result and util.to_bool(self.result['success']) == False and 'body' in self.result:
                    self.__print_to_panel('[OPERATION FAILED]: ' + self.result['body'])
                elif 'success' in self.result and util.to_bool(self.result['success']) == False:
                    self.__print_to_panel('[OPERATION FAILED]')
                else:
                    self.__print_to_panel("Success")
            except Exception as e:
                debug(e)
                debug(traceback.print_exc())
                debug(type(self.result))
                msg = ""
                if type(self.result) is dict:
                    if 'body' in self.result:
                        msg = self.result["body"]
                    else:
                        msg = json.dumps(self.result)
                elif type(self.result) is str:
                    try:
                        m = json.loads(self.result)
                        msg = m["body"]
                    except:
                        msg = self.result
                else:
                    msg = "Check Sublime Text console for error and report issue to MavensMate-SublimeText GitHub project."
                self.__print_to_panel('[OPERATION FAILED]: ' + msg)

    def __handle_coverage_result(self):
        if self.result == []:
            self.__print_to_panel("No coverage information for the requested Apex Class")
        elif 'records' in self.result and self.result["records"] == []:
            self.__print_to_panel("No coverage information for the requested Apex Class")
        else:
            if 'records' in self.result:
                self.result = self.result['records']
            if type(self.result) is list:
                record = self.result[0]
            else:
                record = self.result
            msg = str(record["percentCovered"]) + "%"
            util.mark_uncovered_lines(self.thread.view, record["Coverage"]["uncoveredLines"])
            self.__print_to_panel('[PERCENT COVERED]: ' + msg)
 
    def __handle_org_wide_coverage_result(self):
        if 'PercentCovered' not in self.result:
            self.__print_to_panel("No coverage information available")
        else:
            msg = str(self.result["PercentCovered"]) + "%"
            self.__print_to_panel('[ORG-WIDE TEST COVERAGE]: ' + msg)

    def __handle_coverage_report_result(self):
        if self.result == []:
            self.__print_to_panel("No coverage information available")
        elif 'records' in self.result and self.result["records"] == []:
            self.__print_to_panel("No coverage information available")
        else:
            if 'records' in self.result:
                self.result = self.result['records']
            apex_names = []
            new_dict = {}
            for record in self.result:
                apex_names.append(record["ApexClassOrTriggerName"])
                new_dict[record["ApexClassOrTriggerName"]] = record
            apex_names.sort()
            cls_msg = "Apex Classes:\n"
            trg_msg = "Apex Triggers:\n"
            for apex_name in apex_names:
                msg = ''
                record = new_dict[apex_name]
                coverage_key = ''
                if record["percentCovered"] == 0:
                    coverage_key = ' !!'
                elif record["percentCovered"] < 75:
                    coverage_key = ' !'
                if record["ApexClassOrTrigger"] == "ApexClass":
                    apex_name += '.cls'
                else:
                    apex_name += '.trigger'
                coverage_bar = '[{0}{1}] {2}%'.format('='*(round(record["percentCovered"]/10)), ' '*(10-(round(record["percentCovered"]/10))), record["percentCovered"])
                msg += '   - '+apex_name+ ':'
                msg += '\n'
                msg += '      - coverage: '+coverage_bar + "\t("+str(record["NumLinesCovered"])+"/"+str(record["NumLinesCovered"]+record["NumLinesUncovered"])+")"+coverage_key 
                msg += '\n'
                if record["ApexClassOrTrigger"] == "ApexClass":
                    cls_msg += msg
                else:
                    trg_msg += msg
            self.__print_to_panel('Success')
            new_view = self.thread.window.new_file()
            new_view.set_scratch(True)
            new_view.set_name("Apex Code Coverage")
            if "linux" in sys.platform or "darwin" in sys.platform:
                new_view.set_syntax_file(os.path.join("Packages","YAML","YAML.tmLanguage"))
            else:
                new_view.set_syntax_file(os.path.join("Packages/YAML/YAML.tmLanguage"))
            sublime.set_timeout(new_view.run_command('generic_text', {'text': cls_msg+trg_msg }), 1)

    def __print_result(self):
        msg = ''
        if type(self.result) is dict and 'body' in self.result:
           msg += '[RESPONSE FROM MAVENSMATE]: '+self.result['body']
        elif self.result != None and self.result != "" and (type(self.result) is str or type(self.result) is bytes):
            msg += '[OPERATION FAILED]: Whoops, unable to parse the response. Please enable logging (http://mavensmate.com/Plugins/Sublime_Text/Plugin_Logging) and post relevant log(s) to a new issue at https://github.com/joeferraro/MavensMate-SublimeText\n'
            msg += '[RESPONSE FROM MAVENSMATE]: '+self.result
        else:
            msg += '[OPERATION FAILED]: Whoops, unable to parse the response. Please enable logging (http://mavensmate.com/Plugins/Sublime_Text/Plugin_Logging) and post relevant log(s) to a new issue at https://github.com/joeferraro/MavensMate-SublimeText\n'
            msg += '[RESPONSE FROM MAVENSMATE]: '+json.dumps(self.result, indent=4)
        #debug(self.result)
        self.__print_to_panel(msg)

    def __print_to_panel(self, msg):
        self.printer.panel.run_command('write_operation_status', {'text': msg, 'region': self.__get_print_region() })

    def __get_print_region(self):
        return [self.status_region.end(), self.status_region.end()+10]  

    def __finish(self):
        try:
            if 'success' in self.result and util.to_bool(self.result['success']) == True:
                if self.printer != None and len(ThreadTracker.get_pending_mm_panel_threads(self.thread.window)) == 0:
                    self.printer.hide() 
            elif 'State' in self.result and self.result['State'] == 'Completed' and len(ThreadTracker.get_pending_mm_panel_threads(self.thread.window)) == 0:
                if self.printer != None:
                    self.printer.hide()
            if self.operation == 'refresh':            
                sublime.set_timeout(lambda: sublime.active_window().active_view().run_command('revert'), 200)
                util.clear_marked_line_numbers()
        except:
            pass #TODO

    def __handle_new_metadata(self):
        self.__handle_compile_response()
        if 'success' in self.result and util.to_bool(self.result['success']) == True:
            if 'messages' in self.result or 'details' in self.result:
                if 'details' in self.result and 'componentSuccesses' in self.result['details']:
                    self.result['messages'] = self.result['details'].pop('componentSuccesses')
                if type(self.result['messages']) is not list:
                    self.result['messages'] = [self.result['messages']]
                for m in self.result['messages']:
                    if 'package.xml' not in m['fileName']:
                        file_name = m['fileName']
                        location = os.path.join(util.mm_project_directory(),file_name.replace('unpackaged/', 'src/'))
                        sublime.active_window().open_file(location)
                        break

    def __handle_generic_command_result(self):
        if self.result["success"] == True:
            self.__print_to_panel("Success")
        elif self.result["success"] == False:
            message = "[OPERATION FAILED]: "+self.result["body"]
            self.__print_to_panel(message)
        try:
            if self.thread.alt_callback != None:
                self.thread.alt_callback(self.result["body"])
        except:
            pass

    def __handle_apex_script_result(self):
        if self.result["success"] == True and self.result["compiled"] == True:
            self.__print_to_panel("Success")
            self.thread.window.open_file(self.result["log_location"], sublime.TRANSIENT)
        elif self.result["success"] == False:
            message = "[OPERATION FAILED]: "
            if "compileProblem" in self.result and self.result["compileProblem"] != None:
                message += "[Line: "+str(self.result["line"]) + ", Column: "+str(self.result["column"])+"] " + self.result["compileProblem"] + "\n"
            if "exceptionMessage" in self.result and self.result["exceptionMessage"] != None:
                message += self.result["exceptionMessage"] + "\n"
            if "exceptionStackTrace" in self.result and self.result["exceptionStackTrace"] != None:
                message += self.result["exceptionStackTrace"] + "\n"
            self.__print_to_panel(message)

    def __handle_test_result(self):
        responses = []
        if len(self.result) == 1:
            res = self.result[0]
            response_string = ""
            if 'detailed_results' in res:
                all_tests_passed = True
                for r in res['detailed_results']:
                    if r["Outcome"] != "Pass":
                        all_tests_passed = False
                        break

                if all_tests_passed:
                    response_string += '[TEST RESULT]: PASS'
                else:
                    response_string += '[TEST RESULT]: FAIL'
                
                for r in res['detailed_results']:
                    if r["Outcome"] == "Pass":
                        pass #dont need to write anything here...
                    else:
                        response_string += '\n\n'
                        rstring = " METHOD RESULT "
                        rstring += "\n"
                        rstring += "{0} : {1}".format(r["MethodName"], r["Outcome"])
                        
                        if "StackTrace" in r and r["StackTrace"] != None:
                            rstring += "\n\n"
                            rstring += " STACK TRACE "
                            rstring += "\n"
                            rstring += r["StackTrace"]
                        
                        if "Message" in r and r["Message"] != None:
                            rstring += "\n\n"
                            rstring += " MESSAGE "
                            rstring += "\n"
                            rstring += r["Message"]
                            rstring += "\n"
                        #responses.append("{0} | {1} | {2} | {3}\n".format(r["MethodName"], r["Outcome"], r["StackTrace"], r["Message"]))
                        responses.append(rstring)
                response_string += "\n\n".join(responses)
                self.__print_to_panel(response_string)
                self.printer.scroll_to_bottom()
            else:
                self.__print_to_panel(json.dumps(self.result))
        elif len(self.result) > 1:
            #run multiple tests
            response_string = ''
            for res in self.result:
                if 'detailed_results' in res:
                    all_tests_passed = True
                    for r in res['detailed_results']:
                        if r["Outcome"] != "Pass":
                            all_tests_passed = False
                            break

                    if all_tests_passed:
                        response_string += res['ApexClass']['Name']+':\n\tTEST RESULT: PASS'
                    else:
                        response_string += res['ApexClass']['Name']+':\n\tTEST RESULT: FAIL'
                    
                    for r in res['detailed_results']:
                        if r["Outcome"] == "Pass":
                            pass #dont need to write anything here...
                        else:
                            response_string += '\n\n'
                            response_string += "\t METHOD RESULT "
                            response_string += "\t\n"
                            response_string += "\t{0} : {1}".format(r["MethodName"], r["Outcome"])
                            
                            if "StackTrace" in r and r["StackTrace"] != None:
                                response_string += "\n\n"
                                response_string += "\t STACK TRACE "
                                response_string += "\t\n"
                                response_string += "\t"+r["StackTrace"].replace("\n","\t\n")
                            
                            if "Message" in r and r["Message"] != None:
                                response_string += "\n\n"
                                response_string += "\t MESSAGE "
                                response_string += "\t\n"
                                response_string += "\t"+r["Message"].replace("\n","\t\n")
                                response_string += "\n"
                response_string += "\n\n"
            #self.__print_to_panel(response_string)
            #self.printer.scroll_to_bottom()

            self.__print_to_panel('Success')
            new_view = self.thread.window.new_file()
            new_view.set_scratch(True)
            new_view.set_name("Run All Tests Result")
            if "linux" in sys.platform or "darwin" in sys.platform:
                new_view.set_syntax_file(os.path.join("Packages","YAML","YAML.tmLanguage"))
                new_view.set_syntax_file(os.path.join("Packages","MavensMate","sublime","panel","MavensMate.hidden-tmLanguage"))
            else:
                new_view.set_syntax_file(os.path.join("Packages/MavensMate/sublime/panel/MavensMate.hidden-tmLanguage"))

            sublime.set_timeout(new_view.run_command('generic_text', {'text': response_string }), 1)

        elif 'body' in self.result:
            self.__print_to_panel(json.dumps(self.result['body']))
