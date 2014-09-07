import sublime, sys, os
import unittest
import unittest.mock as mock
from unittest.mock import MagicMock
import MavensMate.util as util
import MavensMate.lib.mm_installer as mm_installer
from MavensMate.lib.mm_installer import MmInstaller
import MavensMate.config as config

debug = config.debug
settings = sublime.load_settings('mavensmate.sublime-settings')
packages_path = sublime.packages_path()

class MmInstallerTests(unittest.TestCase):
    
    pass