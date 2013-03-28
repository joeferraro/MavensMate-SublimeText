import mavensmate

import unittest
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
        binaries_os = {"osx":      [mavensmate.ruby, mavensmate.sublime_bin, mavensmate.doxygen],
                        "windows": [mavensmate.ruby, mavensmate.sublime_bin, mavensmate.doxygen, mavensmate.chrome],
                        "linux":   [mavensmate.ruby, mavensmate.sublime_bin, mavensmate.doxygen, mavensmate.chrome]
                    }
        binaries = []
        if (sys.platform.startswith('darwin')):
            binaries = binaries_os['osx']
        elif sys.platform.startswith('win'):
            binaries = binaries_os['windows']
        else:
            binaries = binaries_os['linux']

        for binary in binaries:
            self.assertTrue(mavensmate.binary_exists(binary), msg="binary '%s' does not exist or is not in PATH" % binary)
