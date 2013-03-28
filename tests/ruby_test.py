import mavensmate

import unittest
import subprocess
import os
import glob

# Note: This test can only be run from within Sublime Text 2
#       because it needs the Sublime Text 2 Plugin Context 'mavensmate'


class RubyTest(unittest.TestCase):

    def test_all(self):
        cwd = os.getcwd()
        try:
            os.chdir(mavensmate.mm_dir)
            for ruby_test in glob.glob('support/test/*test.rb'):
                p = subprocess.Popen([mavensmate.ruby], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                (stdout, stderr) = p.communicate()
                self.assertEqual(0, p.returncode, msg=stdout)

        finally:
            os.chdir(cwd)
