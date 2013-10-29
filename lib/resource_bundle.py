import os
import sublime
import sys
import shutil
import zipfile

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

#creates resource-bundles for the static resource(s) selected        
def create(self, files, refresh=False):
    for file in files:
        fileName, fileExtension = os.path.splitext(file)
        if fileExtension != '.resource':
            sublime.message_dialog("You can only create resource bundles for static resources")
            return
    
    printer = PanelPrinter.get(self.window.id())
    printer.show()
    if refresh:
        printer.write('\nRefreshing Resource Bundle(s)\n')
    else:
        printer.write('\nCreating Resource Bundle(s)\n')

    if not os.path.exists(os.path.join(util.mm_project_directory(),'resource-bundles')):
        os.makedirs(os.path.join(util.mm_project_directory(),'resource-bundles'))

    for f in files:
        fileName, fileExtension = os.path.splitext(f)
        if sys.platform == "win32":
            baseFileName = fileName.split("\\")[-1]
        else:
            baseFileName = fileName.split("/")[-1]
        if not refresh:
            if os.path.exists(os.path.join(util.mm_project_directory(),'resource-bundles',baseFileName+fileExtension)):
                printer.write('[OPERATION FAILED]: The resource bundle already exists\n')
                return
        if sys.platform == "win32":
            fz = zipfile.ZipFile(f, 'r')
            for fileinfo in fz.infolist():
                path = os.path.join(util.mm_project_directory(),'resource-bundles',baseFileName+fileExtension)
                directories = fileinfo.filename.decode('utf8').split('\\')
                for directory in directories:
                    path = os.path.join(path, directory)
                    if directory == directories[-1]: break # the file
                    if not os.path.exists(path):
                        os.makedirs(path)
                outputfile = open(path, "wb")
                shutil.copyfileobj(f.open(fileinfo.filename), outputfile)
        else:
            cmd = 'unzip \''+f+'\' -d \''+util.mm_project_directory()+'/resource-bundles/'+baseFileName+fileExtension+'\''
            os.system(cmd)

    printer.write('[Resource bundle creation complete]\n')
    printer.hide()
    util.send_usage_statistics('Create Resource Bundle') 

def refresh(self, dirs):
    files = []
    for d in dirs:
        static_resource_location = os.path.join(util.mm_project_directory(), "src", "staticresources", os.path.basename(d))
        if os.path.isfile(static_resource_location):
            files.append(static_resource_location)
    create(self, files, True)

