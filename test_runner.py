import sublime
import sublime_plugin

import os
import sys
import unittest
import StringIO

# Note: This test can only be run from within Sublime Text 2
#       because it needs the Sublime Text 2 Context

MM_DIR = os.path.join(sublime.packages_path(), 'MavensMate')
sys.path.append(MM_DIR)

TEST_CASES = ['tests.ruby_test', 'tests.local_server_test']


def print_to_view(view, obtain_content):
    edit = view.begin_edit()
    view.insert(edit, 0, obtain_content())
    view.end_edit(edit)
    view.set_scratch(True)
    return view


class RunSelfTestCommand(sublime_plugin.WindowCommand):
    def run(self):
        cwd = os.getcwd()
        try:
            os.chdir(MM_DIR)
            bucket = StringIO.StringIO()
            suite = unittest.defaultTestLoader.loadTestsFromNames(TEST_CASES)
            unittest.TextTestRunner(stream=bucket, verbosity=1).run(suite)
            print_to_view(self.window.new_file(), bucket.getvalue)
        finally:
            os.chdir(cwd)
