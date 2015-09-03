import sublime
import json
import os
import sys
import html.parser
import time
import traceback
from .merge import MavensMateDiffThread
import MavensMate.util as util
import MavensMate.config as config
sublime_version = int(float(sublime.version()))
settings = sublime.load_settings('mavensmate.sublime-settings')
html_parser = html.parser.HTMLParser()
debug = config.debug

class MavensMateResponseHandler(object):

    def __init__(self, context):
        self.operation           = context.get('operation', None)
        self.process_id          = context.get('process_id', None)
        self.start_time           = context.get('start_time', None)
        self.duration            = 0
        self.printer             = context.get('printer', None)
        self.thread              = context.get('thread', None)
        self.response            = context.get('response', None)
        self.process_region      = self.printer.panel.find(self.process_id,0)
        self.status_region       = self.printer.panel.find('   Result: ',self.process_region.begin())
        if self.start_time is not None:
            self.duration = time.time() - self.start_time

        try:
            self.response = json.loads(self.response)
            self.result = self.response['result']
        except:
            debug('Could not load json response from mavensmate')
            debug(self.response)
            pass

    def has_error(self):
        return 'error' in self.response

    def execute(self):
        if self.response is None:
            self.__print_to_panel('[OPERATION FAILED]: No response from mavensmate executable. Please enable logging (http://mavensmate.com/Plugins/Sublime_Text/Plugin_Logging) and post relevant log(s) to a new issue at https://github.com/joeferraro/MavensMate-SublimeText')
        elif self.has_error():
            self.__print_error()
        else:
            try:
                if self.operation == 'compile-metadata' or self.operation == 'compile-project':
                    self.__handle_compile_response()
                elif self.operation == 'run-tests' or self.operation == 'run-all-tests':
                    self.__handle_test_result()
                elif self.operation == 'run-apex-script':
                    self.__handle_apex_script_result()
                elif self.operation == 'get-coverage':
                    self.__handle_coverage_result()
                elif self.operation == 'coverage-report':
                    self.__handle_coverage_report_result()
                elif self.operation == 'delete-metadata':
                    self.__handle_delete_metadata_result()
                else:
                    self.__handle_generic_command_result()
            except Exception as e:
                try:
                    self.__handle_generic_command_result()
                except:
                    debug(e)
                    debug(traceback.print_exc())
                    self.__print_result()

            self.__finish()

    def __finish(self):
        try:
            if self.operation == 'refresh':
                sublime.set_timeout(lambda: sublime.active_window().active_view().run_command('revert'), 200)
                util.clear_marked_line_numbers()
        except:
            pass #TODO

    def __print_error(self):
        msg = '[ERROR]: '+self.response['error']
        # if 'stack' in self.response:
        #     msg += '\n\n' + self.response.stack
        self.__print_to_panel(msg)

    def __print_to_panel(self, msg):
        self.printer.panel.run_command('write_operation_status', {'text': msg, 'region': self.__get_print_region() })

    def __get_print_region(self):
        return [self.status_region.end(), self.status_region.end()+10]

    def __print_result(self):
        msg = ''
        if type(self.response) is dict and 'body' in self.response:
           msg += '[RESPONSE FROM MAVENSMATE]: '+self.response['body']
        elif self.response != None and self.response != "" and (type(self.response) is str or type(self.response) is bytes):
            msg += '[OPERATION FAILED]: Whoops, unable to parse the response. Please enable logging (http://mavensmate.com/Plugins/Sublime_Text/Plugin_Logging) and post relevant log(s) to a new issue at https://github.com/joeferraro/MavensMate-SublimeText\n'
            msg += '[RESPONSE FROM MAVENSMATE]: '+self.response
        else:
            msg += '[OPERATION FAILED]: Whoops, unable to parse the response. Please enable logging (http://mavensmate.com/Plugins/Sublime_Text/Plugin_Logging) and post relevant log(s) to a new issue at https://github.com/joeferraro/MavensMate-SublimeText\n'
            msg += '[RESPONSE FROM MAVENSMATE]: '+json.dumps(self.response, indent=4)
        self.__print_to_panel(msg)

    def __handle_generic_command_result(self):
        '''
            {'success': True, 'result': 'Started logging for debug users'}
        '''
        msg = ''
        if 'result' in self.response:
            msg = 'Success'
            msg += ': '+self.response['result']['message']
        elif 'error' in self.response:
            msg = '[OPERATION FAILED]'
            if 'error' in self.response:
                msg += ': '+self.response['error']
        self.__print_to_panel(msg)

    def __handle_delete_metadata_result(self, **kwargs):
        debug('HANDLING DELETE!')
        debug(self.response)
        self.__handle_compile_response()

    def __handle_compile_response(self, **kwargs):
        debug('HANDLING COMPILE!')
        debug(self.response)

        '''
            LIGHTNING:
            {
              "result": "markup:\/\/mm2:bar:3,19: ParseError at [row,col]:[4,19]\nMessage: XML document structures must start and end within the same entity.: Source",
              "success": false,
              "stack": "FIELD_INTEGRITY_EXCEPTION: markup:\/\/mm2:bar:3,19: ParseError at [row,col]:[4,19]\nMessage: XML document structures must start and end within the same entity.: Source\n    at onResponse (\/Users\/josephferraro\/Development\/Github\/MavensMate\/node_modules\/jsforce\/lib\/connection.js:368:13)\n    at _fulfilled (\/Users\/josephferraro\/Development\/Github\/MavensMate\/node_modules\/jsforce\/node_modules\/q\/q.js:798:54)\n    at self.promiseDispatch.done (\/Users\/josephferraro\/Development\/Github\/MavensMate\/node_modules\/jsforce\/node_modules\/q\/q.js:827:30)\n    at Promise.promise.promiseDispatch (\/Users\/josephferraro\/Development\/Github\/MavensMate\/node_modules\/jsforce\/node_modules\/q\/q.js:760:13)\n    at \/Users\/josephferraro\/Development\/Github\/MavensMate\/node_modules\/jsforce\/node_modules\/q\/q.js:574:44\n    at flush (\/Users\/josephferraro\/Development\/Github\/MavensMate\/node_modules\/jsforce\/node_modules\/q\/q.js:108:17)\n    at process._tickCallback (node.js:419:13)"
            }

            TOOLING/METADATA:
            {
              "result": {
                "checkOnly": false,
                "completedDate": "",
                "createdBy": "",
                "createdByName": "",
                "createdDate": "",
                "details": {
                  "componentSuccesses": [

                  ],
                  "runTestResult": {
                    "numFailures": "0",
                    "numTestsRun": "0",
                    "totalTime": "0.0"
                  },
                  "componentFailures": [
                    {
                      "attributes": {
                        "type": "ContainerAsyncRequest",
                        "url": "\/services\/data\/v32.0\/tooling\/sobjects\/ContainerAsyncRequest\/1dro0000000mhNbAAI"
                      },
                      "Id": "1dro0000000mhNbAAI",
                      "MetadataContainerId": "1dco0000000JuxBAAS",
                      "MetadataContainerMemberId": null,
                      "State": "Failed",
                      "IsCheckOnly": false,
                      "DeployDetails": {
                        "allComponentMessages": [
                          {
                            "changed": false,
                            "columnNumber": -1,
                            "componentType": "ApexClass",
                            "created": false,
                            "createdDate": "2015-02-12T02:59:21.986+0000",
                            "deleted": false,
                            "fileName": "ChangePasswordController",
                            "forPackageManifestFile": false,
                            "fullName": "ChangePasswordController",
                            "id": "01po0000001iVdVAAU",
                            "knownPackagingProblem": false,
                            "lineNumber": 16,
                            "problem": "expecting right curly bracket, found '&lt;EOF&gt;'",
                            "problemType": "Error",
                            "requiresProductionTestRun": false,
                            "success": false,
                            "warning": false
                          }
                        ],
                        "componentFailures": [
                          {
                            "changed": false,
                            "columnNumber": -1,
                            "componentType": "ApexClass",
                            "created": false,
                            "createdDate": "2015-02-12T02:59:21.986+0000",
                            "deleted": false,
                            "fileName": "ChangePasswordController",
                            "forPackageManifestFile": false,
                            "fullName": "ChangePasswordController",
                            "id": "01po0000001iVdVAAU",
                            "knownPackagingProblem": false,
                            "lineNumber": 16,
                            "problem": "expecting right curly bracket, found '&lt;EOF&gt;'",
                            "problemType": "Error",
                            "requiresProductionTestRun": false,
                            "success": false,
                            "warning": false
                          }
                        ],
                        "componentSuccesses": [

                        ],
                        "runTestResult": null
                      },
                      "ErrorMsg": null
                    }
                  ]
                },
                "done": false,
                "id": "",
                "ignoreWarnings": false,
                "lastModifiedDate": "",
                "numberComponentErrors": 1,
                "numberComponentsDeployed": 0,
                "numberComponentsTotal": 0,
                "numberTestErrors": 0,
                "numberTestsCompleted": 0,
                "numberTestsTotal": 0,
                "rollbackOnError": false,
                "runTestsEnabled": "false",
                "startDate": "",
                "status": "",
                "success": false
              }
            }
        '''

        #diffing with server
        if 'status' in self.response['result'] and self.response['result']['status'] == 'Conflict':
            conflicts = self.result['details']['conflicts']
            first_conflict_file_name = list(conflicts.keys())[0]
            first_conflict_data = conflicts[first_conflict_file_name]
            diff_merge_settings = config.settings.get('mm_diff_server_conflicts', False)
            conflict_message = 'A conflict has been detected. '+first_conflict_file_name+' was last modified by '+first_conflict_data['remote']['LastModifiedBy']['Name']+' on '+first_conflict_data['remote']['LastModifiedDate']
            if diff_merge_settings:
                if sublime.ok_cancel_dialog(conflict_message, 'Diff with server'):
                    self.__print_to_panel(conflict_message + ". Diffing with server.")
                    th = MavensMateDiffThread(self.thread.window, self.thread.view, first_conflict_data['remote']['tempPath'])
                    th.start()
                else:
                    self.__print_to_panel('Operation canceled.')
            else:
                if sublime.ok_cancel_dialog(conflict_message, "Overwrite Server Copy"):
                    self.__print_to_panel(conflict_message + ". Overwriting server copy.")
                    args = {
                        "paths" : [self.thread.view.file_name()]
                    }
                    sublime.set_timeout(lambda: self.thread.window.run_command('force_compile_file', args), 100)
                else:
                    self.__print_to_panel('Operation canceled.')
        else:
            try:
                success = self.response['result']['success']
                if success:
                    util.clear_marked_line_numbers(self.thread.view)
                    msg = "Success, %.1fs" % self.duration
                    self.__print_to_panel(msg)
                    self.printer.hide()
                    return

                msg = '[OPERATION FAILED]: '

                if type(self.response['result']['details']['componentFailures']) is not list:
                    self.response['result']['details']['componentFailures'] = [self.response['result']['details']['componentFailures']]

                for res in self.response['result']['details']['componentFailures']:
                    if 'DeployDetails' in res:
                        for detail in res['DeployDetails']['componentFailures']:
                            debug(detail)
                            line_col = ''
                            line, col = 1, 1
                            if 'lineNumber' in detail:
                                line = int(detail['lineNumber'])
                                line_col = ' (Line: '+str(line)
                                util.mark_line_numbers(self.thread.view, [line], 'bookmark')
                            if 'columnNumber' in detail:
                                col = int(detail['columnNumber'])
                                line_col += ', Column: '+str(col)
                            if len(line_col):
                                line_col += ')'

                            #scroll to the line and column of the exception
                            if settings.get('mm_compile_scroll_to_error', True):
                                view = self.thread.view
                                pt = view.text_point(line-1, col-1)
                                view.sel().clear()
                                view.sel().add(sublime.Region(pt))
                                view.show(pt)

                            msg += detail['fileName']+': '+ detail['problem'] + line_col + '\n'
                    else: # metadata api?
                        msg += res['fullName']+': '+ res['problem'] + '\n'

                self.__print_to_panel(msg)

            except Exception as e:
                debug(e)
                debug(traceback.print_exc())
                debug(type(self.response))
                msg = ""
                if type(self.response) is dict:
                    if 'body' in self.response:
                        msg = self.response["body"]
                    else:
                        msg = json.dumps(self.response)
                elif type(self.response) is str:
                    try:
                        m = json.loads(self.response)
                        msg = m["body"]
                    except:
                        msg = self.response
                else:
                    msg = "Check Sublime Text console for error and report issue to MavensMate-SublimeText GitHub project."
                self.__print_to_panel('[OPERATION FAILED]: ' + msg)

    def __handle_coverage_result(self):
        if isinstance( self.result, int ):
            msg = str(self.result) + "%"
            self.__print_to_panel('[ORG-WIDE TEST COVERAGE]: ' + msg)
        else:
            if self.response == []:
                self.__print_to_panel("No coverage information for the requested Apex Class")
            elif 'records' in self.response and self.response["records"] == []:
                self.__print_to_panel("No coverage information for the requested Apex Class")
            else:
                if 'records' in self.response:
                    self.response = self.response['records']
                if type(self.response) is list:
                    record = self.response[0]
                else:
                    record = self.response
                msg = str(record["percentCovered"]) + "%"
                util.mark_uncovered_lines(self.thread.view, record["Coverage"]["uncoveredLines"])
                self.__print_to_panel('[PERCENT COVERED]: ' + msg)

    def __handle_coverage_report_result(self):
        if self.response == []:
            self.__print_to_panel("No coverage information available")
        elif 'records' in self.response and self.response["records"] == []:
            self.__print_to_panel("No coverage information available")
        else:
            if 'records' in self.response:
                self.response = self.response['records']
            apex_names = []
            new_dict = {}
            for record in self.response:
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

    def __handle_apex_script_result(self):
        '''
            {
              "result": {
                "coolscript.cls": {
                  "line": -1,
                  "column": -1,
                  "compiled": true,
                  "success": true,
                  "compileProblem": null,
                  "exceptionStackTrace": null,
                  "exceptionMessage": null
                }
              },
              "success": true
            }
        '''
        msg = ''
        for script_name in self.result:
            script_res = self.result[script_name]
            debug(script_res)
            if script_res['success'] and script_res['compiled']:
                self.__print_to_panel("Success")
                msg += 'Success '+script_name+'\n'
            elif not script_res['success']:
                msg = "[OPERATION FAILED]: "
                if "compileProblem" in script_res and script_res["compileProblem"] != None:
                    msg += "[Line: "+str(script_res["line"]) + ", Column: "+str(script_res["column"])+"] " + script_res["compileProblem"] + "\n"
                if "exceptionMessage" in script_res and script_res["exceptionMessage"] != None:
                    msg += script_res["exceptionMessage"] + "\n"
                if "exceptionStackTrace" in script_res and script_res["exceptionStackTrace"] != None:
                    msg += script_res["exceptionStackTrace"] + "\n"
        self.__print_to_panel(msg)

    def __handle_test_result(self):
        '''
            {
              "result": {
                "testResults": {
                  "ChangePasswordControllerTest": {
                    "attributes": {
                      "type": "ApexTestQueueItem",
                      "url": "\/services\/data\/v32.0\/tooling\/sobjects\/ApexTestQueueItem\/709o0000000DUTXAA4"
                    },
                    "ApexClassId": "01po0000001iVdWAAU",
                    "ApexClass": {
                      "attributes": {
                        "type": "ApexClass",
                        "url": "\/services\/data\/v32.0\/tooling\/sobjects\/ApexClass\/01po0000001iVdWAAU"
                      },
                      "Name": "ChangePasswordControllerTest"
                    },
                    "Status": "Completed",
                    "ExtendedStatus": "(0\/1)",
                    "results": [
                      {
                        "attributes": {
                          "type": "ApexTestResult",
                          "url": "\/services\/data\/v32.0\/tooling\/sobjects\/ApexTestResult\/07Mo0000002IOAdEAO"
                        },
                        "Outcome": "Fail",
                        "ApexClassId": "01po0000001iVdWAAU",
                        "ApexClass": {
                          "attributes": {
                            "type": "ApexClass",
                            "url": "\/services\/data\/v32.0\/tooling\/sobjects\/ApexClass\/01po0000001iVdWAAU"
                          },
                          "Name": "ChangePasswordControllerTest"
                        },
                        "MethodName": "testChangePasswordController",
                        "Message": "System.AssertException: Assertion Failed",
                        "StackTrace": "Class.mm2.ChangePasswordControllerTest.testChangePasswordController: line 13, column 1",
                        "ApexLogId": "07Lo000000SpsbJEAR"
                      }
                    ]
                  }
                },
                "coverageResults": {
                  "classes": {
                    "ChangePasswordController": {
                      "coveredLines": [
                        5,
                        6,
                        7,
                        9,
                        10,
                        11,
                        14
                      ],
                      "uncoveredLines": [

                      ],
                      "totalLines": 7,
                      "percentCovered": 100
                    }
                  },
                  "triggers": {

                  }
                }
              },
              "success": true
            }
        '''
        msg = ''

        debug(self.response['result']['testResults'])

        for test_class_name in self.response['result']['testResults'].keys():

            debug(test_class_name)
            debug(self.response['result']['testResults'][test_class_name])

            test_result = self.response['result']['testResults'][test_class_name]
            tests_passed_vs_failed = test_result['ExtendedStatus']

            tests_passed_vs_failed = tests_passed_vs_failed.replace('(', '').replace(')','')
            if tests_passed_vs_failed.split('/')[0] != tests_passed_vs_failed.split('/')[1]:
                msg += '[TEST RESULT]: FAIL'
            else:
                msg += '[TEST RESULT]: PASS'

            msg += '\n\n' + test_class_name + ': ' + test_result['ExtendedStatus'] + ' Passed'

            for r in test_result['results']:
                msg += '\n\n METHOD RESULT \n'
                msg += "{0} : {1}".format(r['MethodName'], r['Outcome'])

                if "StackTrace" in r and r["StackTrace"] != None:
                    msg += "\n\n"
                    msg += " STACK TRACE "
                    msg += "\n"
                    msg += r["StackTrace"]

                if "Message" in r and r["Message"] != None:
                    msg += "\n\n"
                    msg += " MESSAGE "
                    msg += "\n"
                    msg += r["Message"]
                    msg += "\n"

        self.__print_to_panel(msg)
