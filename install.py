try:
    import os
    import sys
    import shutil
    import argparse
    import pipes

    install_paths = {
        "darwin" : os.path.expanduser("~/Library/Application Support/Sublime Text 2/Packages/MavensMate"),
        "win32"  : "",
        "cygwin" : "",
        "linux2" : ""
    }

    user_settings_path = {
        "darwin" : os.path.expanduser("~/Library/Application Support/Sublime Text 2/Packages/User"),
        "win32"  : "",
        "cygwin" : "",
        "linux2" : ""
    }

    platform            = sys.platform
    install_path        = install_paths[platform]
    user_settings_path  = user_settings_path[platform]
    branch              = None
    git_url             = pipes.quote('git://github.com/joeferraro/MavensMate-SublimeText.git')

    def install_from_source():
        os.system("git clone {0} {1}".format(git_url, pipes.quote(install_path)))
        if branch != None and branch != '':
            #2.0 is beta
            os.chdir(install_path)
            os.system("git checkout -b {0} origin/{0}".format(pipes.quote(branch)))

    def install_user_settings():
        if os.path.isfile(user_settings_path+"/mavensmate.sublime-settings") == False:
            os.system("cp {0} {1}".format(
                pipes.quote(install_path+"/mavensmate.sublime-settings"), 
                pipes.quote(user_settings_path)
            ))

    def uninstall():
        os.system("rm -rf {0}".format(pipes.quote(install_path)))

    def install():
        uninstall()
        install_from_source()
        install_user_settings()

    if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('-b', '--branch') #name of the branch being requested
        args = parser.parse_args()
        if args.branch != None and args.branch != '':
            branch = args.branch
        install()
except Exception as e:
    print('install.py issue')
    print(e.message)