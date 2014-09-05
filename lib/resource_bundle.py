import os
import sublime
import sys
import shutil
import zipfile

from .printer import PanelPrinter
import MavensMate.util as util
import MavensMate.lib.mm_interface as mm
import MavensMate.lib.community as community

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
                directories = fileinfo.filename.split('/')
                #directories = fileinfo.filename.split('\\')
                for directory in directories:
                    if directory.startswith('__MACOSX'):
                        continue
                    path = os.path.join(path, directory)
                    if directory == directories[-1]: break # the file
                    if not os.path.exists(path):
                        os.makedirs(path)
                try:
                    outputfile = open(path, "wb")
                    shutil.copyfileobj(fz.open(fileinfo.filename), outputfile)
                except:
                    pass
        else:
            cmd = 'unzip \''+f+'\' -d \''+util.mm_project_directory()+'/resource-bundles/'+baseFileName+fileExtension+'\''
            os.system(cmd)

    printer.write('[Resource bundle creation complete]\n')
    printer.hide()
    community.sync_activity('new_resource_bundle')

def deploy(bundle_name):
    if '.resource' not in bundle_name:
        bundle_name = bundle_name + '.resource'
    message = 'Bundling and deploying to server: ' + bundle_name
    # delete existing sr
    if os.path.exists(os.path.join(util.mm_project_directory(),"src","staticresources",bundle_name)):
        os.remove(os.path.join(util.mm_project_directory(),"src","staticresources",bundle_name))
    # zip bundle to static resource dir 
    os.chdir(os.path.join(util.mm_project_directory(),"resource-bundles",bundle_name))
    if 'darwin' in sys.platform or 'linux' in sys.platform:
        #cmd = "zip -r -X '"+util.mm_project_directory()+"/src/staticresources/"+bundle_name+"' *"      
        #os.system(cmd)
        zip_file = util.zip_directory(os.path.join(util.mm_project_directory(),"resource-bundles",bundle_name), os.path.join(util.mm_project_directory(),"src","staticresources",bundle_name))
    elif 'win32' in sys.platform:
        zip_file = util.zip_directory(os.path.join(util.mm_project_directory(),"resource-bundles",bundle_name), os.path.join(util.mm_project_directory(),"src","staticresources",bundle_name))
    print(zip_file)
    if zip_file.endswith(".zip"):
        os.rename(zip_file, zip_file[:-4])
    #compile
    file_path = os.path.join(util.mm_project_directory(),"src","staticresources",bundle_name)
    params = {
        "files" : [file_path]
    }
    mm.call('compile', params=params, message=message)
    community.sync_activity('deploy_resource_bundle')

def refresh(self, dirs):
    files = []
    for d in dirs:
        static_resource_location = os.path.join(util.mm_project_directory(), "src", "staticresources", os.path.basename(d))
        if os.path.isfile(static_resource_location):
            files.append(static_resource_location)
    create(self, files, True)

