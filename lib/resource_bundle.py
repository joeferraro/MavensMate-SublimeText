import os
import sublime
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
def create(self, files):
    for file in files:
        fileName, fileExtension = os.path.splitext(file)
        if fileExtension != '.resource':
            sublime.message_dialog("You can only create resource bundles for static resources")
            return
    printer = PanelPrinter.get(self.window.id())
    printer.show()
    printer.write('\nCreating Resource Bundle(s)\n')

    if not os.path.exists(util.mm_project_directory()+'/resource-bundles'):
        os.makedirs(util.mm_project_directory()+'/resource-bundles')

    for file in files:
        fileName, fileExtension = os.path.splitext(file)
        baseFileName = fileName.split("/")[-1]
        if os.path.exists(util.mm_project_directory()+'/resource-bundles/'+baseFileName+fileExtension):
            printer.write('[OPERATION FAILED]: The resource bundle already exists\n')
            return
        cmd = 'unzip \''+file+'\' -d \''+util.mm_project_directory()+'/resource-bundles/'+baseFileName+fileExtension+'\''
        os.system(cmd)

    printer.write('[Resource bundle creation complete]\n')
    printer.hide()
    util.send_usage_statistics('Create Resource Bundle') 