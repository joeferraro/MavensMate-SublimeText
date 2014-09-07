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
    
    @mock.patch("sys.platform", "linux2") 
    def test_should_return_linux_platform_flag(self): 
        self.assertEquals('linux', mm_installer.get_platform_flag())

    @mock.patch("sys.platform", "win32") 
    def test_should_return_win_platform_flag(self): 
        self.assertEquals('win', mm_installer.get_platform_flag())

    @mock.patch("sys.platform", "darwin") 
    def test_should_return_osx_platform_flag(self): 
        self.assertEquals('osx', mm_installer.get_platform_flag())

    @mock.patch("sys.platform", "linux2") 
    def test_should_return_latest_non_prerelease_because_not_beta_user(self):
        settings.set('mm_beta_user', False)
        mock_releases = util.parse_json_from_file(os.path.join(packages_path, 'MavensMate', 'tests', 'fixtures', 'releases.json'))
        mm_installer.get_mm_releases = MagicMock(return_value=mock_releases)
        releases = mm_installer.get_mm_releases()
        self.assertEquals(7, len(releases))
        installer = MmInstaller()
        self.assertEquals('v0.2.3', installer.latest_release['tag_name'])

    @mock.patch("sys.platform", "linux2") 
    def test_should_return_prerelease_as_latest_release_because_beta_user(self):
        settings.set('mm_beta_user', True)
        mock_releases = util.parse_json_from_file(os.path.join(packages_path, 'MavensMate', 'tests', 'fixtures', 'releases.json'))
        mm_installer.get_mm_releases = MagicMock(return_value=mock_releases)
        releases = mm_installer.get_mm_releases()
        self.assertEquals(7, len(releases))
        installer = MmInstaller()
        self.assertEquals('v0.2.4', installer.latest_release['tag_name'])
