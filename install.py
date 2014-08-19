try:
    import os
    import sys
    import shutil
    import pipes

    install_paths = {
        "darwin" : os.path.expanduser("~/Library/Application Support/Sublime Text 3/Packages/MavensMate"),
        "win32"  : os.path.join(os.environ.get('APPDATA',''), 'Sublime Text 3', 'Packages', 'MavensMate'),
        "cygwin"  : os.path.join(os.environ.get('APPDATA',''), 'Sublime Text 3', 'Packages', 'MavensMate'),
        "linux2" : os.path.expanduser("~/.config/sublime-text-3/Packages/MavensMate")
    }

    user_settings_path = {
        "darwin" : os.path.expanduser("~/Library/Application Support/Sublime Text 3/Packages/User"),
        "win32"  : os.path.join(os.environ.get('APPDATA',''), 'Sublime Text 3', 'Packages', 'User'),
        "cygwin"  : os.path.join(os.environ.get('APPDATA',''), 'Sublime Text 3', 'Packages', 'User'),
        "linux2" : os.path.expanduser("~/.config/sublime-text-3/Packages/User")
    }

    platform            = sys.platform
    install_path        = install_paths[platform]
    user_settings_path  = user_settings_path[platform]
    branch              = 'master'
    git_url             = pipes.quote('http://github.com/joeferraro/MavensMate-SublimeText.git')

    def install_from_source():
        if 'linux' in sys.platform or 'darwin' in sys.platform:
            os.system("git clone --recursive {0} {1}".format(git_url, pipes.quote(install_path)))
            os.chdir(install_path)
            os.system("git checkout -B {0} origin/{0}".format(pipes.quote(branch)))
            os.system("git submodule init")
            os.system("git submodule update")
        else:
            os.system('git clone --recursive {0} "{1}"'.format(git_url, install_path))
            os.chdir(install_path)
            os.system("git checkout -B {0} origin/{0}".format(branch))
            os.system("git submodule init")
            os.system("git submodule update")

    def install_user_settings():
        if os.path.isfile(user_settings_path+"/mavensmate.sublime-settings") == False:
            if 'linux' in sys.platform or 'darwin' in sys.platform:
                os.system("cp {0} {1}".format(
                    pipes.quote(install_path+"/mavensmate.sublime-settings"), 
                    pipes.quote(user_settings_path)
                ))
            else:
                shutil.copyfile(install_path+"/mavensmate.sublime-settings", user_settings_path)

    def uninstall():
        if 'linux' in sys.platform or 'darwin' in sys.platform:
            os.system("rm -rf {0}".format(pipes.quote(install_path)))
        else:
            os.system('rmdir /S /Q \"{}\"'.format(install_path))

    def install():
        uninstall()
        install_from_source()
        install_user_settings()

    if __name__ == '__main__':
        install()
        
except Exception as e:
    print(e)