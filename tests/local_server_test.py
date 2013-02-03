import mavensmate

import unittest
import subprocess
import time
import sys

# Note: This test can only be run from within Sublime Text 2
#       because it needs the Sublime Text 2 Plugin Context 'mavensmate'


class LocalServerTest(unittest.TestCase):

    def test_start_stop(self):
        mavensmate.start_local_server()
        time.sleep(1)
        mavensmate.stop_local_server()

    def test_mm_dir(self):
        self.assertNotEqual(None, mavensmate.mm_dir)
        self.assertNotEqual('', mavensmate.mm_dir)

    def test_mm_workspace(self):
        workspace = mavensmate.mm_workspace()
        self.assertNotEqual(None, workspace)
        self.assertNotEqual('', workspace)
        self.assertFalse(' ' in workspace)
        self.assertFalse('%' in workspace)
        self.assertFalse('!' in workspace)

    def test_binaries(self):
        binaries_os = {"osx": [mavensmate.ruby],
                        "windows_linux": [mavensmate.ruby, mavensmate.doxygen, mavensmate.chrome]
                    }
        binaries = binaries_os['osx'] if sys.platform.startswith('darwin') else binaries_os['windows_linux']
        for binary in binaries:
            p = subprocess.Popen([binary, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = p.communicate()
            self.assertEqual(0, p.returncode, msg=stdout)
