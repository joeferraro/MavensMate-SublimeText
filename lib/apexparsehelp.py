import os
import MavensMate.config as config
import subprocess
import json
import threading

class ApexParser(threading.Thread):

    def __init__(self, files):
        self.files          = files
        self.result         = {}
        threading.Thread.__init__(self)

    def run(self):
        for f in self.files:
            parser_command = 'java -jar "{0}" "{1}"'.format(
                os.path.join(config.mm_dir,"lib","bin","apex-completion-parser.jar"),
                f)
            result_string = ""
            parser_response = None
            process = subprocess.Popen(parser_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            
            if process.stdout is not None: 
                parser_response = process.stdout.readlines()
            elif process.stderr is not None:
                parser_response = process.stderr.readlines()
            try:
                result_string = '\n'.join(parser_response)
            except:
                strs = []
                for line in parser_response:
                    strs.append(line.decode('utf-8'))   
                result_string = '\n'.join(strs)

            print('response from parser: ' + result_string)

            try:    
                self.result[f] = json.loads(result_string)
            except Exception as e:
                print('oops: ',e)
                this_result = {
                    "success"           : False,
                    "file_location"     : f
                }
                self.result[f] = this_result