#Embedded file name: ./sftp/commands.py
import sublime
import sublime_plugin
import os
import json
import subprocess
import re
import sys
import hmac
import binascii
from itertools import izip, cycle
import time
import traceback
import tempfile
import shutil
import difflib
import codecs
try:
    import ssl
except ImportError:
    pass

if os.name != 'nt':
    import unicodedata
from .errors import handle_exception, NotFoundError, ConnectionError, PermissionError, AuthenticationError
from .panel_printer import PanelPrinter, ProgressThread
from .threads import HookedThread, SyncThread, ThreadTracker, unset_current_thread
from .debug import debug_print, get_debug
from .times import time_diff
from .views import get_view_by_group_index
from .paths import canonicalize, local_to_remote, remote_to_local, is_dir, is_root, dirname, path_type, fix_windows_path, ignore_paths, ignore_rm_paths
from .config import get_default_config, find_config, load_config, parse_config, build_config, get_server_config_folder, prepare_server_config, setup_tmp_dir
from .sftp_transport import SFTP
from .ftp_transport import FTP
from .vcs import Hg, Git, SVN
transports = {'SFTP': SFTP,
 'FTP': FTP}
if 'ssl' in sys.modules:
    from .ftps_transport import FTPS
    transports['FTPS'] = FTPS

class SftpCommand(object):
    connections = {}
    identifiers = {}
    usage = {}
    remote_roots = {}
    remote_time_offsets = {}

    @classmethod
    def setup_elements(cls, config):
        if not hasattr(SftpCommand, 'elements'):
            SftpCommand.elements = [0,
             config.get('email'),
             'sftp_flags',
             'ssh_key_file',
             'psftp']
            SftpCommand.elements.append('Sublime SFTP\n\n' + 'Thanks for trying out Sublime SFTP.' + ' It is free to try, but a license must be purchased for ' + 'continued use.\n\n' + 'Please visit http://sublime.wbond.net/sftp for details.')
            SftpCommand.elements.append(config.get('product_key'))
            key = SftpCommand.elements[1]
            for element in SftpCommand.elements[2:-2]:
                key = hmac.new(element, key).digest()

            SftpCommand.elements[1] = key

    def create_default_config(self, file):
        handle = open(file, 'w')
        handle.write(get_default_config(True))
        handle.close()

    def first_path(self, paths):
        if paths == None or paths == []:
            return
        return paths[0]

    def get_path(self, paths = None, allow_multiple = False, view = None):
        type_ = type(paths).__name__
        if (paths == None or paths == []) and type_ not in ('str', 'unicode'):
            if view != None:
                return view.file_name()
            if hasattr(self, 'window') and self.window.active_view() != None:
                return self.window.active_view().file_name()
            return
        if allow_multiple or type_ == 'str' or type_ == 'unicode':
            return paths
        return paths[0]

    def has_config(self, path):
        return bool(find_config(path, True))

    def get_config(self, paths = None, quiet = False):
        path = self.get_path(paths)
        config, config_file = load_config(path)
        if config == None:
            return
        config_dir = dirname(config_file)
        return build_config(config, config_dir, config_file, quiet)

    def save_files(self, files = []):
        if not isinstance(files, list):
            files = [files]
        window = self.window if hasattr(self, 'window') else self.view.window()
        original_view = window.active_view()
        for view in window.views():
            file = view.file_name()
            if files and file not in files or not file:
                continue
            if find_config(file, True) and view.is_dirty():
                window.focus_view(view)
                view_settings = view.settings()
                view_settings.set('sftp_auto_save', True)
                view.run_command('save')

        if original_view:
            window.focus_view(original_view)


class SftpThread(HookedThread):

    def __init__(self, window_id, config, file, action, should_join = True, quiet = False, increment = True, reset_lcd = None, on_connect = None, on_fail = None, on_complete = None, hide = True, skip_ignore = False, skip_symlinks = True):
        self.window_id = window_id
        self.printer = PanelPrinter.get(window_id)
        self.config = config
        self.file = file
        self.action = action
        self.quiet = quiet
        self.result = None
        self.connection = None
        self.increment = increment
        self.should_join = should_join
        self.reset_lcd = reset_lcd
        self.on_connect = on_connect
        self.on_fail = on_fail
        self.on_complete = on_complete
        self.connection_id = str(window_id) + '-' + self.config['user'] + '@' + self.config['host'] + ':' + self.config['port']
        self.hide = hide
        self.failed = False
        self.skip_ignore = skip_ignore
        self.skip_symlinks = skip_symlinks
        SftpCommand.setup_elements(self.config)
        super(SftpThread, self).__init__()

    @classmethod
    def cleanup(cls):
        for connection_id in SftpCommand.connections:
            connection = SftpCommand.connections[connection_id]
            connection.close()

    def close_connection(self, identifier, dir, window_id, disconnected = False):
        if not SftpCommand.usage.get(identifier):
            return
        SftpCommand.usage[identifier] -= 1
        if SftpCommand.usage[identifier] and not disconnected:
            return
        debug_print('SFTP: Closing unused connection ' + identifier, 2)
        if SftpCommand.connections.get(identifier):
            SftpCommand.connections[identifier].close(disconnected)
            debug_print('SFTP: Closed unused connection ' + identifier, 2)
            del SftpCommand.connections[identifier]
        if SftpCommand.identifiers.get(str(window_id) + '-' + dir):
            del SftpCommand.identifiers[str(window_id) + '-' + dir]

    def kill(self):
        debug_print('SFTP: Killing connection ' + self.connection_id, 2)
        self.connection.close()
        dir = self.config['local_dir']
        dir = str(self.window_id) + '-' + dir
        identifier = SftpCommand.identifiers.get(dir, None)
        if SftpCommand.identifiers.get(dir):
            del SftpCommand.identifiers[dir]
        if identifier:
            del SftpCommand.connections[identifier]
            del SftpCommand.usage[identifier]
        ThreadTracker.set_current(self.window_id, None)

    @unset_current_thread
    def run(self):
        self.start = time.time()
        if self.should_join:
            last_thread = ThreadTracker.get_last_added(self.window_id)
            ThreadTracker.add(self)
            if last_thread != None:
                debug_print('SFTP: Waiting for previous thread', 2)
                last_thread.join()
        debug_print('SFTP: Beginning file transfer thread', 2)
        ThreadActivity(self, self.printer, 'SFTP Working')
        self.printer.reset_hide()
        ThreadTracker.set_current(self.window_id, self)
        try:
            if not self.make_connection():
                return
            debug_print('SFTP: Checking license key', 2)
            SftpCommand.setup_elements(self.config)
            do_show = False
            self.action not in ('list', 'listr', 'llist', 'llistr', 'cwd') and SftpCommand.elements[0] += 1
            key_prefix = ''.join((chr(ord(x) ^ ord(y)) for x, y in izip(SftpCommand.elements[1], cycle('22'))))
            key_prefix = binascii.hexlify(key_prefix)[:30]
            clen = 6
            chunks = [ key_prefix[(i - 1) * clen:i * clen] for i in xrange(1, len(key_prefix) / clen + 1) ]
            key_prefix = '-'.join(chunks)
            if SftpCommand.elements[0] > 0 and SftpCommand.elements[0] % 10 == 0 and key_prefix != SftpCommand.elements[-1]:

                def reg():
                    if int(sublime.version()) >= 2190:
                        if sublime.ok_cancel_dialog(SftpCommand.elements[-2], 'Buy Now'):
                            sublime.active_window().run_command('open_url', {'url': 'http://wbond.net/sublime_packages/sftp/buy'})
                    else:
                        sublime.error_message(SftpCommand.elements[-2])

                sublime.set_timeout(reg, 1)
                do_show = True
            self.do_operation(do_show)
        except OSError as e:
            if self.on_fail:
                self.on_fail(e)
            self.close_connection(self.connection_id, self.config['local_dir'], self.window_id, str(e) == 'Disconnected')
            if str(e) == 'Disconnected':
                try:
                    debug_print('SFTP: Reconnecting after disconnection', 2)
                    if not self.make_connection():
                        return
                    self.do_operation()
                except OSError:
                    self.printer.write('\nMultiple disconnection errors, ' + 'giving up')

    def make_connection(self):
        self.failed = True
        old_identifier = SftpCommand.identifiers.get(str(self.window_id) + '-' + self.config['local_dir'], None)
        if old_identifier != None and self.connection_id != old_identifier:
            self.close_connection(old_identifier, self.config['local_dir'], self.window_id)
        self.connection = SftpCommand.connections.get(self.connection_id, None)
        if self.connection == None:
            class_name = self.config['type'].upper()
            class_object = transports[class_name]
            debug_print('SFTP: Creating file transfer object', 2)
            merged_config = self.config.copy()
            merged_config['remote_time_offset'] = SftpCommand.remote_time_offsets.get(self.connection_id)
            self.connection = class_object(self.printer, **merged_config)
            try:
                debug_print('SFTP: Starting connection', 2)
                self.connection.connect()
                debug_print('SFTP: Successful connected', 2)
                SftpCommand.connections[self.connection_id] = self.connection
            except (AuthenticationError, ConnectionError) as e:
                self.printer.error(e)
                return False
            except OSError as e:
                self.close_connection(self.connection_id, self.config['local_dir'], self.window_id)
                return False

        if str(self.window_id) + '-' + self.config['local_dir'] not in SftpCommand.identifiers:
            SftpCommand.identifiers[str(self.window_id) + '-' + self.config['local_dir']] = self.connection_id
            if self.connection_id not in SftpCommand.usage:
                SftpCommand.usage[self.connection_id] = 0
            SftpCommand.usage[self.connection_id] += 1
        if self.connection_id not in SftpCommand.remote_roots:
            SftpCommand.remote_roots[self.connection_id] = []
        if self.config['remote_dir'] not in SftpCommand.remote_roots[self.connection_id]:
            try:
                progress = ProgressThread(self.printer, '\nValidating remote folder "%s"' % self.config['initial_remote_dir'])
                initial_dir = self.connection.pwd()
                self.connection.cd(self.config['initial_remote_dir'])
                self.connection.ls(self.config['path_map'], config=self.config)
                SftpCommand.remote_roots[self.connection_id].append(self.config['remote_dir'])
            except (NotFoundError, PermissionError) as e:
                progress.stop('failure (' + str(e) + ')')
                progress.join()
                self.connection.remote_time_offset = 0
                output = '\nInitial folder and contents:'
                try:
                    for path in self.connection.ls(self.config['path_map'], config=self.config):
                        if path[0] == '.':
                            path[0] = ''
                        output += '\n  "%s%s"' % (initial_dir, path[0])

                    self.printer.write(output)
                except ConnectionError as e:
                    self.close_connection(self.connection_id, self.config['local_dir'], self.window_id)
                    self.printer.write('\nListing initial folder "%s" ... failure (%s)' % (initial_dir, str(e)))

                self.printer.error(e)
                return False
            except ConnectionError as e:
                progress.stop('failure (%s)' % str(e))
                progress.join()
                self.close_connection(self.connection_id, self.config['local_dir'], self.window_id)
                self.printer.error(e)
                return False
            except OSError as e:
                is_ftp = self.config['type'] == 'ftp'
                is_pasv = self.config.get('ftp_passive_mode') != False
                if str(e) == 'Disconnected' and is_ftp and is_pasv:
                    e = OSError('Disconnected - possible PASV mode error, try setting ftp_passive_mode to false in sftp-config.json')
                self.close_connection(self.connection_id, self.config['local_dir'], self.window_id)
                progress.stop('failure (%s)' % str(e))
                progress.join()
                raise e
            except (AttributeError, EOFError) as e:
                backtrace = traceback.format_exc()
                handle_exception('Unknown Error', backtrace)
                self.close_connection(self.connection_id, self.config['local_dir'], self.window_id)
                progress.stop('failure (Unknown Error)')
                progress.join()
                return False

            progress.stop('success')
            progress.join()
        if self.connection_id not in SftpCommand.remote_time_offsets:
            SftpCommand.remote_time_offsets[self.connection_id] = self.connection.remote_time_offset
        if self.on_connect:
            self.on_connect()
        self.failed = False
        return True

    def do_operation(self, show = False):
        self.failed = True
        self.connection.debug(get_debug())
        debug_print('SFTP: Starting operation ' + self.action, 2)
        success, result = getattr(self.connection, self.action)(self.file, path_map=self.config['path_map'], chmod_dirs=self.config.get('dir_permissions'), chmod_files=self.config.get('file_permissions'), ignore_regex=self.config.get('ignore_regex') if not self.skip_ignore else None, quiet=self.quiet, config=self.config, skip_symlinks=self.skip_symlinks)
        if show:

            def do_print():
                self.printer.write('\nUNREGISTERED: Please visit http://sublime.wbond.net/sftp')

            sublime.set_timeout(do_print, 1)
        debug_print('SFTP: Finished operation ' + self.action, 2)
        if self.hide:
            sublime.set_timeout(lambda : self.printer.hide(self), 1)
        if self.reset_lcd:
            self.connection.lcd(self.reset_lcd)
        if self.on_fail and not success:
            self.on_fail(result)
        if self.on_complete and success:
            sublime.set_timeout(self.on_complete, 1)
        self.result = result
        if success:
            self.failed = False


class SftpShowPanelCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self):
        PanelPrinter.get(self.window.id()).show(True)


class SftpCreateServerCommand(sublime_plugin.WindowCommand):

    def run(self):
        config_dir = get_server_config_folder()
        self.window.run_command('new_file_at', {'dirs': [config_dir]})
        view_settings = self.window.active_view().settings()
        view_settings.set('syntax', 'Packages/JavaScript/JSON.tmLanguage')
        view_settings.set('sftp_new_server', True)
        snippet = get_default_config(remove_settings=['save_before_upload',
         'upload_on_save',
         'confirm_sync',
         'ignore_regex',
         'confirm_overwrite_newer',
         'sync_skip_deletes',
         'confirm_downloads'], force_settings={'sync_down_on_open': True})
        self.window.active_view().run_command('insert_snippet', {'contents': snippet})


class SftpLastServerCommand(sublime_plugin.WindowCommand):

    def run(self):
        name = BrowsePathThread.get_last()
        if not name:
            return
        self.window.run_command('sftp_browse_server', {'name': name})


class SftpBrowseServerCommand(sublime_plugin.WindowCommand):

    def run(self, name = None):
        config_dir = get_server_config_folder()
        self.config_dir = config_dir
        servers = []
        for filename in os.listdir(config_dir):
            if filename in ('.DS_Store', 'Thumbs.db', 'desktop.ini'):
                continue
            config = prepare_server_config(filename)
            if config:
                servers.append(config)

        self.servers = servers
        choices = [ ['  ' + r['name'], '  ' + r['desc'] + ' ' + r.get('remote_path', '')] for r in servers ]
        choices.insert(0, [u'Add New Server\u2026', 'Set up a new SFTP or FTP server to browse'])
        self.window_id = self.window.id()
        self.printer = PanelPrinter.get(self.window_id)
        names = [ s['name'] for s in servers ]
        if name and name in names:
            self.on_done(names.index(name) + 1)
            return
        self.window.show_quick_panel(choices, self.on_done)

    def on_done(self, index):
        if index == -1:
            return
        if index == 0:
            self.window.run_command('sftp_create_server')
            return
        index -= 1
        raw_config = self.servers[index]
        tmp_dir = setup_tmp_dir(raw_config)
        config = build_config(raw_config, tmp_dir, raw_config['file_path'])
        if not config:
            return
        config['is_tmp'] = True
        config['tmp_dir'] = tmp_dir
        debug_print('SFTP: Starting Browse Path Thread from List', 2)
        BrowsePathThread(config, self.printer, self.window_id, self.window, None).start()


class SftpEditServerCommand(sublime_plugin.WindowCommand):

    def run(self):
        config_dir = get_server_config_folder()
        self.config_dir = config_dir
        servers = []
        for filename in os.listdir(config_dir):
            if filename in ('.DS_Store', 'Thumbs.db', 'desktop.ini'):
                continue
            config = prepare_server_config(filename)
            if config:
                servers.append(config)

        self.servers = servers
        choices = [ ['  ' + r['name'], '  ' + r['desc'] + ' ' + r.get('remote_path', '')] for r in servers ]
        self.window.show_quick_panel(choices, self.on_done)

    def on_done(self, index):
        if index == -1:
            return
        remote = self.servers[index]
        config_path = os.path.join(self.config_dir, remote['name'])

        def open_file():
            self.window.run_command('open_file', {'file': fix_windows_path(config_path)})
            self.window.active_view().settings().set('syntax', 'Packages/JavaScript/JSON.tmLanguage')

        sublime.set_timeout(open_file, 1)


class SftpDeleteServerCommand(sublime_plugin.WindowCommand):

    def run(self):
        config_dir = get_server_config_folder()
        self.config_dir = config_dir
        servers = []
        for filename in os.listdir(config_dir):
            if filename in ('.DS_Store', 'Thumbs.db', 'desktop.ini'):
                continue
            config = prepare_server_config(filename)
            if config:
                servers.append(config)

        self.servers = servers
        choices = [ ['  ' + r['name'], '  ' + r['desc'] + ' ' + r.get('remote_path', '')] for r in servers ]
        self.window.show_quick_panel(choices, self.on_done)

    def on_done(self, index):
        if index == -1:
            return
        remote = self.servers[index]
        self.config_path = os.path.join(self.config_dir, remote['name'])
        choices = [['Yes', 'Delete %s server' % remote['name']], ['No', 'Do not delete %s server' % remote['name']]]
        self.window.show_quick_panel(choices, self.confirm_delete)

    def confirm_delete(self, index):
        if index == -1 or index == 1:
            return
        os.unlink(self.config_path)


class QuickPanelBrowser(object):

    def cleanup(self):
        if 'is_tmp' not in self.config:
            return
        tmp_dir = dirname(self.config['local_dir'])
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)


class BrowsePathThread(HookedThread, QuickPanelBrowser):
    last_name = None

    @classmethod
    def get_last(cls):
        return cls.last_name

    def __init__(self, config, printer, window_id, window, remote_path, second_time = False):
        self.config = config
        self.printer = printer
        self.window_id = window_id
        self.window = window
        self.remote_path = remote_path
        super(BrowsePathThread, self).__init__()

    def run(self):
        BrowsePathThread.last_name = self.config['name']
        if self.remote_path == None:
            pwd_thread = SftpThread(self.window_id, self.config, None, 'cwd', hide=False)
            pwd_thread.start()
            pwd_thread.join()
            if pwd_thread.failed:
                sublime.set_timeout(self.printer.show, 1)
                self.cleanup()
                return
            self.remote_path = pwd_thread.result
        reset_lcd = None
        if self.config.get('is_tmp'):
            reset_lcd = dirname(dirname(self.config['local_dir']))
        list_dir_thread = SftpThread(self.window_id, self.config, self.remote_path, 'list', reset_lcd=reset_lcd, hide=False, skip_ignore=True, skip_symlinks=False)
        list_dir_thread.start()
        list_dir_thread.join()
        if list_dir_thread.failed and list_dir_thread.result in ('File not found', 'Folder not found', 'Permission denied'):
            debug_print('SFTP: Starting Browse Thread after Error', 2)
            BrowsePathThread(self.config, self.printer, self.window_id, self.window, dirname(self.remote_path), second_time=True).start()
            return
        if list_dir_thread.failed:
            sublime.set_timeout(self.printer.show, 1)
            self.cleanup()
            return
        self.files = []
        self.entries = []
        listing = [ p[0] for p in list_dir_thread.result if is_dir(p[0]) ]
        listing.extend([ p[0] for p in list_dir_thread.result if not is_dir(p[0]) and p[0] != '.' ])
        if list_dir_thread.result:
            self.files.extend([ p for p in listing ])
            self.entries.extend([ u'    ' + p for p in listing if is_dir(p) ])
            self.entries.extend([ '    ' + p for p in listing if not is_dir(p) ])
        self.files.insert(0, '')
        self.entries.insert(0, u'' + self.config['host'] + ':' + self.remote_path)
        if not is_root(self.remote_path):
            self.files.insert(1, '..')
            self.entries.insert(1, u' \u2022 Up a folder')
        self.files.insert(1, '.')
        self.entries.insert(1, u' \u2022 Folder actions')
        self.existing_files = ['.', '..']
        if list_dir_thread.result:
            self.existing_files.extend([ p[0].rstrip('/\\') for p in list_dir_thread.result ])
        sublime.set_timeout(self.show_files, 1)

    def show_files(self):
        self.window.show_quick_panel(self.entries, self.show_files_action)

    def custom_path(self):
        self.window.show_input_panel('Browse to', self.remote_path, self.browse_to, None, self.show_files)

    def browse_to(self, input):
        if len(input) == 0:
            input = '/'
        input = canonicalize(input, 'remote')
        debug_print('SFTP: Starting Custom Browse Path Thread', 2)
        BrowsePathThread(self.config, self.printer, self.window_id, self.window, input).start()

    def show_files_action(self, index):
        if index == -1:
            self.cleanup()
            return
        selected = self.files[index]
        new_path = None
        if selected == '':
            self.custom_path()
            return
        if selected == '..':
            new_path = dirname(self.remote_path)
        else:
            if selected == '.':
                self.selected_path = self.remote_path
                self.modify_dir()
                return
            if not is_dir(selected):
                self.selected_path = os.path.join(self.remote_path, selected)
                self.modify_file()
                return
            new_path = os.path.join(self.remote_path, selected)
        debug_print('SFTP: Starting Browse Sub-path Thread', 2)
        BrowsePathThread(self.config, self.printer, self.window_id, self.window, new_path).start()

    def modify_dir(self):
        actions = [u'' + self.config['host'] + ':' + self.selected_path,
         u' \u2022 Back to list',
         u' \u2022 New file',
         u' \u2022 New folder',
         u' \u2022 Rename',
         u' \u2022 Delete']
        if not self.config.get('is_tmp'):
            actions.insert(4, u' \u2022 Download')
        self.window.show_quick_panel(actions, self.modify_dir_action)

    def modify_dir_action(self, index):
        if index == -1:
            self.cleanup()
            return
        if index == 0 or index == 1:
            self.show_files()
            return
        is_tmp = self.config.get('is_tmp')
        if index == 2:
            self.window.show_input_panel('New file name', '', self.new_file, None, self.modify_dir)
        if index == 3:
            self.window.show_input_panel('New folder name', '', self.new_folder, None, self.modify_dir)
        if index == 4 and not is_tmp:
            debug_print('SFTP: Starting Download Folder Thread', 2)
            DownloadPathThread(self.config, self.printer, self.window_id, self.window, self.selected_path).start()
        if not is_tmp and index == 5 or is_tmp and index == 4:
            self.window.show_input_panel('New name', os.path.basename(self.selected_path.rstrip('/\\')), self.rename_folder, None, self.modify_dir)
        if not is_tmp and index == 6 or is_tmp and index == 5:
            name = canonicalize(os.path.basename(self.selected_path.rstrip('/\\')), 'remote')
            choices = [['Yes', 'Delete %s and all children' % name], ['No', 'Do not delete %s' % name]]
            self.window.show_quick_panel(choices, self.confirm_delete_dir)

    def new_file(self, new_name):
        if new_name.find('\\') != -1 or new_name.find('/') != -1:

            def try_again_slash():
                sublime.error_message('SFTP: file name may not contain slashes')
                self.window.show_input_panel('New file name', '', self.new_file, None, self.modify_dir)

            sublime.set_timeout(try_again_slash, 1)
            return
        if new_name in self.existing_files:

            def try_again_existing():
                sublime.error_message('SFTP: a file or folder with that name specified already exists')
                self.window.show_input_panel('New file name', '', self.new_file, None, self.modify_dir)

            sublime.set_timeout(try_again_existing, 1)
            return
        new_path = os.path.join(self.selected_path, new_name)
        debug_print('SFTP: Starting New File Thread', 2)
        NewFileThread(self.config, self.printer, self.window_id, self.window, new_path).start()

    def new_folder(self, new_name):
        if new_name.find('\\') != -1 or new_name.find('/') != -1:

            def try_again_slash():
                sublime.error_message('SFTP: folder name may not contain slashes')
                self.window.show_input_panel('New folder name', '', self.new_folder, None, self.modify_dir)

            sublime.set_timeout(try_again_slash, 1)
            return
        if new_name in self.existing_files:

            def try_again_existing():
                sublime.error_message('SFTP: a file or folder with that name specified already exists')
                self.window.show_input_panel('New folder name', '', self.new_folder, None, self.modify_dir)

            sublime.set_timeout(try_again_existing, 1)
            return
        new_path = os.path.join(self.selected_path, new_name)
        debug_print('SFTP: Starting New Folder Thread', 2)
        NewFolderThread(self.config, self.printer, self.window_id, self.window, new_path).start()

    def rename_folder(self, new_name):
        if new_name == os.path.basename(self.selected_path.rstrip('\\/')):
            self.cleanup()
            return
        if new_name.find('\\') != -1 or new_name.find('/') != -1:

            def try_again():
                sublime.error_message('SFTP: folder name may not contain slashes')
                self.window.show_input_panel('New name', os.path.basename(self.selected_path.rstrip('/\\')), self.rename_folder, None, self.modify_dir)

            sublime.set_timeout(try_again, 1)
            return
        new_path = os.path.join(dirname(self.selected_path), new_name)
        new_path = canonicalize(new_path, 'remote')
        debug_print('SFTP: Starting Rename Folder Thread', 2)
        RenamePathThread(self.config, self.printer, self.window_id, self.window, self.selected_path, new_path).start()

    def confirm_delete_dir(self, index):
        if index == -1 or index == 1:
            self.modify_dir()
            return
        DeletePathThread(self.config, self.printer, self.window_id, self.window, self.selected_path).start()

    def modify_file(self):
        actions = [u'' + self.config['host'] + ':' + self.selected_path,
         u' \u2022 Back to list',
         u' \u2022 Edit',
         u' \u2022 Rename',
         u' \u2022 Delete']
        if not self.config.get('is_tmp'):
            actions[2] += ' (remote version)'
            actions.insert(3, u' \u2022 Download')
        self.window.show_quick_panel(actions, self.modify_file_action)

    def modify_file_action(self, index):
        if index == -1:
            self.cleanup()
            return
        is_tmp = self.config.get('is_tmp')
        if index == 0 or index == 1:
            self.show_files()
            return
        if index == 2:
            debug_print('SFTP: Starting Edit File Thread', 2)
            EditFileThread(self.config, self.printer, self.window_id, self.window, self.selected_path).start()
            return
        if index == 3 and not is_tmp:
            debug_print('SFTP: Starting Download File Thread', 2)
            DownloadPathThread(self.config, self.printer, self.window_id, self.window, self.selected_path).start()
        if not is_tmp and index == 4 or is_tmp and index == 3:
            self.window.show_input_panel('New name', os.path.basename(self.selected_path.rstrip('/\\')), self.rename_file, None, self.modify_file)
        if not is_tmp and index == 5 or is_tmp and index == 4:
            name = os.path.basename(self.selected_path)
            choices = [['Yes', 'Delete %s' % name], ['No', 'Do not delete %s' % name]]
            self.window.show_quick_panel(choices, self.confirm_delete_file)

    def rename_file(self, new_name):
        if new_name == os.path.basename(self.selected_path.rstrip('\\/')):
            self.cleanup()
            return
        if new_name.find('\\') != -1 or new_name.find('/') != -1:

            def try_again():
                sublime.error_message('SFTP: file name may not contain slashes')
                self.window.show_input_panel('New name', os.path.basename(self.selected_path.rstrip('/\\')), self.rename_path, None, self.modify_file)

            sublime.set_timeout(try_again, 1)
            return
        new_path = os.path.join(dirname(self.selected_path), new_name)
        debug_print('SFTP: Starting Rename File Thread', 2)
        RenamePathThread(self.config, self.printer, self.window_id, self.window, self.selected_path, new_path).start()

    def confirm_delete_file(self, index):
        if index == -1 or index == 1:
            self.modify_file()
            return
        debug_print('SFTP: Starting Delete File Thread', 2)
        DeletePathThread(self.config, self.printer, self.window_id, self.window, self.selected_path).start()


class DownloadPathThread(HookedThread):

    def __init__(self, config, printer, window_id, window, remote_path, on_complete = None):
        self.config = config
        self.printer = printer
        self.window_id = window_id
        self.window = window
        self.remote_path = remote_path
        self.on_complete = on_complete
        super(DownloadPathThread, self).__init__()

    def run(self):
        sublime.set_timeout(self.printer.show, 1)
        if not is_dir(self.remote_path):
            download_thread = SftpThread(self.window_id, self.config, self.remote_path, 'get', should_join=False)
            download_thread.start()
            download_thread.join()
            local_path = remote_to_local(self.remote_path, self.config['path_map'])
            if not download_thread.failed:

                def open_file():
                    self.window.run_command('open_file', {'file': fix_windows_path(local_path)})
                    if self.on_complete:
                        self.on_complete()

                sublime.set_timeout(open_file, 1)
            else:
                BrowsePathThread(self.config, self.printer, self.window_id, self.window, dirname(self.remote_path)).start()
        else:
            download_thread = DownloadFolderThread(self.window_id, self.config, self.remote_path)
            download_thread.start()
            download_thread.join()
            if download_thread.error:
                sublime.set_timeout(self.printer.show, 1)
            BrowsePathThread(self.config, self.printer, self.window_id, self.window, self.remote_path).start()


class EditFileThread(HookedThread):

    def __init__(self, config, printer, window_id, window, remote_path):
        self.config = config
        self.printer = printer
        self.window_id = window_id
        self.window = window
        self.remote_path = remote_path
        self.local_path = None
        if not config.get('tmp_dir'):
            self.local_path = remote_to_local(remote_path, config.get('path_map'))
            raw_config, config_file = load_config(self.config['local_dir'])
            tmp_dir = setup_tmp_dir(raw_config)
            raw_config, config_file = load_config(tmp_dir)
            new_config = build_config(raw_config, tmp_dir, config_file)
            new_config['tmp_dir'] = tmp_dir
            self.config = new_config
        super(EditFileThread, self).__init__()

    def run(self):
        config = self.config.copy()
        config['path_map'] = {config['tmp_dir']: config['remote_dir']}
        local_path = remote_to_local(self.remote_path, config['path_map'])
        sublime.set_timeout(self.printer.show, 1)
        download_thread = SftpThread(self.window_id, config, self.remote_path, 'get', should_join=False, reset_lcd=dirname(dirname(config['local_dir'])))
        download_thread.start()
        download_thread.join()
        if not download_thread.failed:

            def open_file():
                self.window.run_command('open_file', {'file': fix_windows_path(local_path)})
                view = self.window.active_view()
                if self.local_path:
                    view.settings().set('local_path', self.local_path)
                view.settings().set('remote_loading', True)
                view.settings().set('synced', True)
                view.settings().set('is_remote', True)
                view.settings().set('tmp_dir', self.config['tmp_dir'])

            sublime.set_timeout(open_file, 1)
        else:
            BrowsePathThread(self.config, self.printer, self.window_id, self.window, dirname(self.remote_path)).start()


class NewFileThread(HookedThread):

    def __init__(self, config, printer, window_id, window, remote_path):
        self.config = config
        self.printer = printer
        self.window_id = window_id
        self.window = window
        self.remote_path = remote_path
        super(NewFileThread, self).__init__()

    def run(self):
        local_path = remote_to_local(self.remote_path, self.config['path_map'])
        if not os.path.exists(dirname(local_path)):
            os.makedirs(dirname(local_path))
        open(local_path, 'a').close()
        sublime.set_timeout(self.printer.show, 1)
        reset_lcd = None
        if self.config.get('is_tmp'):
            reset_lcd = dirname(dirname(self.config['local_dir']))
        mv_thread = SftpThread(self.window_id, self.config, local_path, 'put', reset_lcd=reset_lcd)
        mv_thread.start()
        mv_thread.join()
        if not mv_thread.failed:

            def status():
                sublime.status_message('%s successfully created' % path_type(self.remote_path, True))
                self.window.run_command('open_file', {'file': fix_windows_path(local_path)})
                view = self.window.active_view()
                if 'is_tmp' in self.config:
                    view.settings().set('is_remote', True)
                    view.settings().set('tmp_dir', self.config['local_dir'])

            sublime.set_timeout(status, 1)
        else:
            BrowsePathThread(self.config, self.printer, self.window_id, self.window, dirname(self.remote_path)).start()


class NewFolderThread(HookedThread):

    def __init__(self, config, printer, window_id, window, remote_path):
        self.config = config
        self.printer = printer
        self.window_id = window_id
        self.window = window
        self.remote_path = remote_path
        super(NewFolderThread, self).__init__()

    def run(self):
        local_path = remote_to_local(self.remote_path, self.config['path_map'])
        os.makedirs(local_path)
        sublime.set_timeout(self.printer.show, 1)
        reset_lcd = None
        if self.config.get('is_tmp'):
            reset_lcd = dirname(dirname(self.config['local_dir']))
        mv_thread = SftpThread(self.window_id, self.config, local_path, 'put', reset_lcd=reset_lcd)
        mv_thread.start()
        mv_thread.join()
        if not mv_thread.failed:

            def status():
                sublime.status_message('Folder successfully created')

            sublime.set_timeout(status, 1)
        BrowsePathThread(self.config, self.printer, self.window_id, self.window, dirname(self.remote_path)).start()


class RenamePathThread(HookedThread):

    def __init__(self, config, printer, window_id, window, remote_path, new_remote_path):
        self.config = config
        self.printer = printer
        self.window_id = window_id
        self.window = window
        self.remote_path = remote_path
        self.new_remote_path = new_remote_path
        super(RenamePathThread, self).__init__()

    def run(self):
        sublime.set_timeout(self.printer.show, 1)
        reset_lcd = None
        if self.config.get('is_tmp'):
            reset_lcd = dirname(dirname(self.config['local_dir']))
        mv_thread = SftpThread(self.window_id, self.config, [self.remote_path, self.new_remote_path], 'mv', reset_lcd=reset_lcd)
        mv_thread.start()
        mv_thread.join()
        if not mv_thread.failed:

            def status():
                sublime.status_message('%s successfully renamed' % path_type(self.remote_path, True))

            sublime.set_timeout(status, 1)
        BrowsePathThread(self.config, self.printer, self.window_id, self.window, dirname(self.remote_path)).start()


class DeletePathThread(HookedThread):

    def __init__(self, config, printer, window_id, window, remote_path):
        self.config = config
        self.printer = printer
        self.window_id = window_id
        self.window = window
        self.remote_path = remote_path
        super(DeletePathThread, self).__init__()

    def run(self):
        if is_dir(self.remote_path):
            reset_lcd = None
            if self.config.get('is_tmp'):
                reset_lcd = dirname(dirname(self.config['local_dir']))
            list_thread = SftpThread(self.window_id, self.config, self.remote_path, 'listr', should_join=False, reset_lcd=reset_lcd, hide=False, skip_symlinks='file')
            list_thread.start()
            list_thread.join()
            if list_thread.failed or not list_thread.result:
                return
            remote_paths = [ p[0] for p in list_thread.result[::-1] ]
        else:
            remote_paths = self.remote_path
        sublime.set_timeout(self.printer.show, 1)
        reset_lcd = None
        if self.config.get('is_tmp'):
            reset_lcd = dirname(dirname(self.config['local_dir']))
        rm_thread = SftpThread(self.window_id, self.config, remote_paths, 'rm', reset_lcd=reset_lcd)
        rm_thread.start()
        rm_thread.join()
        if not rm_thread.failed:

            def status():
                sublime.status_message('%s successfully deleted' % path_type(self.remote_path, True))

            sublime.set_timeout(status, 1)
        BrowsePathThread(self.config, self.printer, self.window_id, self.window, dirname(self.remote_path)).start()


class SftpBrowseCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None, group = None, index = None, reset_lcd = None):
        config = self.get_config(paths)
        if not config:
            return
        if paths == None:
            active_view = self.window.active_view()
            if active_view and active_view.settings().get('is_remote') and config.get('is_server'):
                self.window.run_command('sftp_browse_server', {'name': config.get('name')})
                return
        printer = PanelPrinter.get(self.window.id())
        path = self.get_path(paths)
        if path == None:
            return
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        path = canonicalize(path, 'local')
        remote_path = local_to_remote(path, config['path_map'])
        debug_print('SFTP: Starting Browse Thread', 2)
        BrowsePathThread(config, printer, self.window.id(), self.window, remote_path).start()

    def is_visible(self, paths = None):
        path = self.get_path(paths)
        if not path:
            return False
        return self.has_config(path)


class SftpUploadFileCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None, group = None, index = None, reset_lcd = None):
        if paths == None and group != None and index != None:
            selected_view = get_view_by_group_index(self.window, group, index)
            paths = [selected_view.file_name()]
        config = self.get_config(paths)
        if not config:
            return
        printer = PanelPrinter.get(self.window.id())
        printer.show()
        files = self.get_path(paths, True)
        if config['save_before_upload']:
            self.save_files(files)
        if config['confirm_overwrite_newer']:
            debug_print('SFTP: Starting Confirm Overwrite File Thread', 2)
            ConfirmOverwriteFileThread(self.window, printer, config, files, reset_lcd=reset_lcd).start()
        else:
            debug_print('SFTP: Starting Upload File Thread', 2)
            SftpThread(self.window.id(), config, files, 'put', reset_lcd=reset_lcd).start()

    def is_visible(self, paths = None):
        path = self.get_path(paths)
        if not path or os.path.isdir(path):
            return False
        return self.has_config(path)


class ConfirmOverwriteFileThread(HookedThread, SyncThread):

    def __init__(self, window, printer, config, files, reset_lcd):
        self.window = window
        self.window_id = window.id()
        self.printer = printer
        self.config = config
        if not isinstance(files, list):
            files = [files]
        self.files = files
        self.reset_lcd = reset_lcd
        super(ConfirmOverwriteFileThread, self).__init__()

    def run(self):
        last_thread = ThreadTracker.get_last_added(self.window_id)
        ThreadTracker.add(self)
        if last_thread != None:
            last_thread.join()
        path_map = self.config['path_map']
        for path in self.files:
            remote_path = local_to_remote(path, path_map, self.config['remote_encoding'])
            nonlocal = {'progress': None}

            def on_connect():
                nonlocal['progress'] = ProgressThread(self.printer, '\nChecking modification date of "%s"' % remote_path)

            def on_fail(e):
                if not nonlocal['progress']:
                    return
                nonlocal['progress'].stop('failure (%s)' % str(e))
                nonlocal['progress'].join()

            dir = canonicalize(dirname(path), 'local')
            remote_dir = local_to_remote(dir, path_map, self.config['remote_encoding'])
            list_dir_thread = SftpThread(self.window_id, self.config, remote_dir, 'list', should_join=False, hide=False, on_connect=on_connect, on_fail=on_fail, skip_symlinks='file')
            list_dir_thread.start()
            list_dir_thread.join()

            def upload_file():
                debug_print('SFTP: Starting Confirmed Upload File Thread', 2)
                put_thread = SftpThread(self.window_id, self.config, path, 'put', should_join=False, hide=False, reset_lcd=self.reset_lcd)
                put_thread.start()
                put_thread.join()

            if list_dir_thread.failed and list_dir_thread.result in ('File not found', 'Folder not found'):
                upload_file()
                continue
            if list_dir_thread.failed:
                return
            if nonlocal['progress']:
                nonlocal['progress'].stop('success')
                nonlocal['progress'].join()
            remote_paths = list_dir_thread.result
            if list_dir_thread.failed or remote_paths == None:
                remote_paths = []
            remote_dict = dict(remote_paths)
            remote_mod_time = remote_dict.get(os.path.basename(remote_path), None)
            local_mod_time = int(os.lstat(path)[8])
            if local_mod_time >= remote_mod_time:
                upload_file()
                continue
            nonlocal = {'confirmed': None}

            def on_confirm():
                nonlocal['confirmed'] = True

            def on_reject():
                nonlocal['confirmed'] = False

            local_time = self.make_time(local_mod_time)
            remote_time = self.make_time(remote_mod_time)
            operations = [u'Upload local "%s" (%s) over remote "%s" [%s vs. %s]' % (self.strip(path, dir, 'local'),
              time_diff(local_mod_time, remote_mod_time),
              self.strip(remote_path, remote_dir, 'remote'),
              local_time,
              remote_time)]
            self.confirm(operations, on_confirm, on_reject)
            while True:
                if nonlocal['confirmed'] != None:
                    break
                time.sleep(0.01)

            if nonlocal['confirmed']:
                upload_file()

        def do_hide():
            self.printer.hide()

        sublime.set_timeout(do_hide, 1)


class SftpMonitorFileCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None):
        config = self.get_config(paths)
        if not config:
            return
        printer = PanelPrinter.get(self.window.id())
        path = self.get_path(paths)
        if not path:
            return
        view = self.window.active_view()
        if view.id() not in [ v.id for v in self.window.views() ]:
            file_name = fix_windows_path(view.file_name())
            self.window.run_command('open_file', {'file': file_name})
        if not view.get_status('sftp_monitor'):
            debug_print('SFTP: Starting File Monitoring', 2)
            sftp_settings = sublime.load_settings('SFTP.sublime-settings')
            frequency = sftp_settings.get('monitoring_frequency', 200)
            frequency = float(frequency) / 1000.0
            delay = sftp_settings.get('monitoring_upload_delay', 500)
            delay = float(delay) / 1000.0
            view.set_status('sftp_monitor', 'SFTP: Monitoring')
            MonitorFileThread(self.window, view, printer, config, path, frequency, delay).start()
        else:
            view.erase_status('sftp_monitor')

    def is_visible(self, paths = None):
        if paths == None:
            active_view = self.window.active_view()
            if active_view and active_view.settings().get('is_remote'):
                return False
        path = self.get_path(paths)
        if not path or os.path.isdir(path):
            return False
        return self.has_config(path)


class MonitorFileThread(HookedThread):

    def __init__(self, window, view, printer, config, path, frequency, delay):
        self.window = window
        self.window_id = window.id()
        self.view = view
        self.printer = printer
        self.config = config
        self.path = path
        self.frequency = frequency
        self.delay = delay
        super(MonitorFileThread, self).__init__()

    def run(self):
        nonlocal = {'cont': True}
        uploaded_mod_time = int(os.lstat(self.path)[8])
        num = 0
        while nonlocal['cont']:
            mod_time = int(os.lstat(self.path)[8])
            if mod_time > uploaded_mod_time:
                time.sleep(self.delay)

                def show():
                    self.printer.show()

                sublime.set_timeout(show, 1)
                debug_print('SFTP: Starting Monitored Upload File Thread', 2)
                SftpThread(self.window_id, self.config, self.path, 'put').start()
                uploaded_mod_time = mod_time
            num = (num + 1) % 5
            if num == 4:

                def check_view():
                    if self.view == None or not self.view.get_status('sftp_monitor'):
                        nonlocal['cont'] = False

                sublime.set_timeout(check_view, 1)
            time.sleep(self.frequency)

        def stop_monitoring():
            debug_print('SFTP: Stoping File Monitoring', 2)
            self.view.erase_status('sftp_monitor')

        sublime.set_timeout(stop_monitoring, 1)


class SftpUploadOpenFilesCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None):
        debug_print('SFTP: Starting Upload Open Files Command', 2)
        for view in self.window.views():
            path = view.file_name()
            if not path:
                debug_print('SFTP: Skipping View Without File Name', 2)
                continue
            paths = [path]
            if not self.has_config(path):
                debug_print('SFTP: Skipping View Without Remote', 2)
                continue
            config = self.get_config(paths)
            if not config:
                continue
            PanelPrinter.get(self.window.id()).show()
            files = self.get_path(paths, True)
            if config['save_before_upload']:
                self.save_files(files)
            debug_print('SFTP: Starting Upload File Thread', 2)
            SftpThread(self.window.id(), config, files, 'put').start()

    def is_visible(self, paths = None):
        if paths == None:
            active_view = self.window.active_view()
            if active_view and active_view.settings().get('is_remote'):
                return False
        path = self.get_path(paths)
        if not path or os.path.isdir(path):
            return False
        return self.has_config(path)


class SftpDiffRemoteFileCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None):
        config = self.get_config(paths)
        if not config:
            return
        printer = PanelPrinter.get(self.window.id())
        printer.show()
        file = self.get_path(paths)
        remote_file = local_to_remote(file, config['path_map'])
        local_path = config['path_map'].keys()[0]
        remote_path = config['path_map'][local_path]
        tmp_dir = os.path.join(tempfile.gettempdir(), 'sublime-sftp-diff-') + str(int(time.time()))
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        config['path_map'] = {tmp_dir: remote_path}
        tmp_file = remote_to_local(remote_file, config['path_map'])
        tmp_file_direct_parent = dirname(tmp_file)
        if not os.path.exists(tmp_file_direct_parent):
            os.makedirs(tmp_file_direct_parent)
        debug_print('SFTP: Starting Diff Remote Thread', 2)
        SftpThread(self.window.id(), config, remote_file, 'get', reset_lcd=dirname(tmp_dir), on_complete=lambda : self.complete(printer, file, remote_file, tmp_dir, tmp_file)).start()

    def complete(self, printer, file, remote_file, tmp_dir, tmp_file):
        printer.show()
        progress = ProgressThread(printer, '\nDiffing "%s" with "%s"' % (file, remote_file))
        sftp_settings = sublime.load_settings('SFTP.sublime-settings')
        if sftp_settings.get('diff_command'):
            diff_command_args = sftp_settings.get('diff_command')
            diff_thread = DiffCommandThread(diff_command_args, file, tmp_file, tmp_dir, sftp_settings.get('delete_temp_diff_folder', True))
            debug_print('SFTP: Starting Diff Command Thread', 2)
            diff_thread.start()
            progress.stop('success (external diff launched)')
            progress.join()
        else:
            settings = sublime.load_settings('Base File.sublime-settings')
            fallback_encoding = settings.get('fallback_encoding')
            fallback_encoding = re.sub('^[a-zA-Z ]*\\((.*)\\)$', '\\1', fallback_encoding)
            try:
                file_lines = codecs.open(file, 'r', 'utf-8').read().splitlines()
            except UnicodeDecodeError:
                debug_print('SFTP: Using fallback encoding "%s" when reading local file for diff' % fallback_encoding, 2)
                file_lines = codecs.open(file, 'r', fallback_encoding).read().splitlines()

            try:
                tmp_file_lines = codecs.open(tmp_file, 'r', 'utf-8').read().splitlines()
            except UnicodeDecodeError:
                debug_print('SFTP: Using fallback encoding "%s" when reading remote file for diff' % fallback_encoding, 2)
                tmp_file_lines = codecs.open(tmp_file, 'r', fallback_encoding).read().splitlines()

            file_date = time.ctime(os.stat(file).st_mtime)
            tmp_file_date = time.ctime(os.stat(tmp_file).st_mtime)
            diff = difflib.unified_diff(file_lines, tmp_file_lines, file, tmp_file, file_date, tmp_file_date, lineterm='')
            diff = u'\n'.join([ line for line in diff ])
            if diff == '':
                progress.stop('success (no changes)')
                printer.reset_hide()
            else:
                name = os.path.basename(file)
                new_view = self.window.new_file()
                new_view.set_name('(local) ' + name + ' -> (remote) ' + name)
                new_view.set_scratch(True)
                new_view.set_syntax_file('Packages/Diff/Diff.tmLanguage')
                edit = new_view.begin_edit()
                new_view.insert(edit, 0, diff)
                new_view.end_edit(edit)
                progress.stop('success')
            progress.join()
            if os.path.exists(tmp_dir):
                try:
                    shutil.rmtree(tmp_dir)
                except WindowsError:
                    pass

    def is_visible(self, paths = None):
        if paths == None:
            active_view = self.window.active_view()
            if active_view and active_view.settings().get('is_remote'):
                return False
        path = self.get_path(paths)
        if not path or os.path.isdir(path):
            return False
        return self.has_config(path)


class DiffCommandThread(HookedThread):

    def __init__(self, args, file, tmp_file, tmp_dir, delete_tmp_dir):
        self.args = args
        self.file = file
        self.tmp_file = tmp_file
        self.tmp_dir = tmp_dir
        self.delete_tmp_dir = delete_tmp_dir
        super(DiffCommandThread, self).__init__()

    def run(self):
        args = []
        for arg in self.args:
            if arg == '%1$s':
                arg = self.file
            elif arg == '%2$s':
                arg = self.tmp_file
            args.append(arg)

        proc = subprocess.Popen(args)
        proc.wait()
        if self.delete_tmp_dir and os.path.exists(self.tmp_dir):
            try:
                shutil.rmtree(self.tmp_dir)
            except WindowsError:
                pass


class SftpRenameLocalAndRemotePathsCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None, files = None, dirs = None):
        if paths == None and files != None:
            paths = files
        if paths == None and dirs != None:
            paths = dirs
        config = self.get_config(paths)
        if not config:
            return
        printer = PanelPrinter.get(self.window.id())
        path = self.get_path(paths)
        remote_path = local_to_remote(path, config['path_map'])

        def prompt_new_name():
            self.window.show_input_panel('New Name', os.path.basename(path.rstrip('/\\')), on_done, None, None)

        def on_done(new_name):
            if new_name.find('\\') != -1 or new_name.find('/') != -1:
                sublime.error_message('SFTP: %s name may not contain slashes' % path_type(path))
                prompt_new_name()
                return
            new_path = dirname(path) + new_name
            if os.path.exists(new_path):
                sublime.error_message('SFTP: a file or folder with that name specified already exists')
                prompt_new_name()
                return
            new_remote_path = dirname(remote_path) + new_name
            printer.show()
            RenameLocalAndRemotePathThread(self.window, config, path, new_path, remote_path, new_remote_path).start()

        prompt_new_name()

    def is_visible(self, paths = None, files = None, dirs = None):
        if paths == None and files == None and dirs == None:
            active_view = self.window.active_view()
            if active_view and active_view.settings().get('is_remote'):
                return False
        if dirs == [] or files == []:
            return
        if paths == None and files != None:
            paths = files
        if paths == None and dirs != None:
            paths = dirs
        path = self.get_path(paths)
        if not path:
            return False
        return self.has_config(path)


class RenameLocalAndRemotePathThread(HookedThread):

    def __init__(self, window, config, path, new_path, remote_path, new_remote_path):
        self.window = window
        self.window_id = window.id()
        self.config = config
        self.path = path
        self.new_path = new_path
        self.remote_path = remote_path
        self.new_remote_path = new_remote_path
        super(RenameLocalAndRemotePathThread, self).__init__()

    def run(self):
        last_thread = ThreadTracker.get_last_added(self.window_id)
        ThreadTracker.add(self)
        if last_thread != None:
            last_thread.join()
        mv_thread = SftpThread(self.window_id, self.config, [self.remote_path, self.new_remote_path], 'mv', should_join=False, reset_lcd=dirname(self.config['local_dir']))
        mv_thread.start()
        mv_thread.join()
        if mv_thread.failed:
            return
        os.rename(self.path, self.new_path)
        if int(sublime.version()) < 2178:
            return

        def do_retarget():
            view = self.window.find_open_file(self.path)
            if view:
                view.retarget(self.new_path)

        sublime.set_timeout(do_retarget, 1)


class SftpDeleteLocalAndRemotePathsCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None, files = None, dirs = None):
        if paths == None and files != None:
            paths = files
        if paths == None and dirs != None:
            paths = dirs
        config = self.get_config(paths)
        if not config:
            return
        printer = PanelPrinter.get(self.window.id())
        path = self.get_path(paths)
        if os.path.isdir(path):
            path = canonicalize(path, 'local')
        remote_path = local_to_remote(path, config['path_map'])
        type_ = path_type(remote_path)

        def on_done(index):
            if index == -1 or index == 1:
                return
            printer.show()
            DeleteLocalAndRemotePathThread(self.window, config, path, remote_path).start()

        choices = [['Yes', 'Delete local and remote %ss %s' % (type_, os.path.basename(remote_path.rstrip('/\\')))], ['No', 'Do not delete local and remote %ss %s' % (type_, os.path.basename(remote_path.rstrip('/\\')))]]
        self.window.show_quick_panel(choices, on_done)

    def is_visible(self, paths = None, files = None, dirs = None):
        if paths == None and files == None and dirs == None:
            active_view = self.window.active_view()
            if active_view and active_view.settings().get('is_remote'):
                return False
        if dirs == [] or files == []:
            return
        if paths == None and files != None:
            paths = files
        if paths == None and dirs != None:
            paths = dirs
        path = self.get_path(paths)
        if not path:
            return False
        return self.has_config(path)


class DeleteLocalAndRemotePathThread(HookedThread):

    def __init__(self, window, config, path, remote_path):
        self.window_id = window.id()
        self.config = config
        self.path = path
        self.remote_path = remote_path
        super(DeleteLocalAndRemotePathThread, self).__init__()

    def run(self):
        last_thread = ThreadTracker.get_last_added(self.window_id)
        ThreadTracker.add(self)
        if last_thread != None:
            last_thread.join()
        if is_dir(self.remote_path):
            list_thread = SftpThread(self.window_id, self.config, self.remote_path, 'listr', should_join=False, hide=False, skip_symlinks='file')
            list_thread.start()
            list_thread.join()
            if list_thread.failed and list_thread.result in ('File not found', 'Folder not found'):
                remote_paths = []
            else:
                if list_thread.failed or not list_thread.result:
                    return
                remote_paths = [ p[0] for p in list_thread.result[::-1] ]
        else:
            remote_paths = self.remote_path
        if remote_paths:
            rm_thread = SftpThread(self.window_id, self.config, remote_paths, 'rm', should_join=False)
            rm_thread.start()
            rm_thread.join()
            if rm_thread.failed and rm_thread.result not in ('File not found', 'Folder not found'):
                return
        if is_dir(self.path):
            shutil.rmtree(self.path)
        else:
            os.remove(self.path)


class SftpDeleteRemotePathCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None, files = None, dirs = None):
        if paths == None and files != None:
            paths = files
        if paths == None and dirs != None:
            paths = dirs
        config = self.get_config(paths)
        if not config:
            return
        printer = PanelPrinter.get(self.window.id())
        path = self.get_path(paths)
        remote_path = local_to_remote(path, config['path_map'])
        type_ = path_type(remote_path)

        def on_done(index):
            if index == -1 or index == 1:
                return
            printer.show()
            DeleteRemotePathThread(self.window, config, remote_path).start()

        choices = [['Yes', 'Delete remote %s %s' % (type_, os.path.basename(remote_path.rstrip('/\\')))], ['No', 'Do not delete remote %s %s' % (type_, os.path.basename(remote_path.rstrip('/\\')))]]
        self.window.show_quick_panel(choices, on_done)

    def is_visible(self, paths = None, files = None, dirs = None):
        if paths == None and files == None and dirs == None:
            active_view = self.window.active_view()
            if active_view and active_view.settings().get('is_remote'):
                return False
        if dirs == [] or files == []:
            return
        if paths == None and files != None:
            paths = files
        if paths == None and dirs != None:
            paths = dirs
        path = self.get_path(paths)
        if not path:
            return False
        return self.has_config(path)


class DeleteRemotePathThread(HookedThread):

    def __init__(self, window, config, remote_path):
        self.window_id = window.id()
        self.config = config
        self.remote_path = remote_path
        super(DeleteRemotePathThread, self).__init__()

    def run(self):
        last_thread = ThreadTracker.get_last_added(self.window_id)
        ThreadTracker.add(self)
        if last_thread != None:
            last_thread.join()
        if is_dir(self.remote_path):
            list_thread = SftpThread(self.window_id, self.config, self.remote_path, 'listr', should_join=False, hide=False, skip_symlinks='file')
            list_thread.start()
            list_thread.join()
            if list_thread.failed or not list_thread.result:
                return
            remote_paths = [ p[0] for p in list_thread.result[::-1] ]
        else:
            remote_paths = self.remote_path
        rm_thread = SftpThread(self.window_id, self.config, remote_paths, 'rm', should_join=False)
        rm_thread.start()
        rm_thread.join()


class SftpDownloadFileCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None):
        config = self.get_config(paths)
        if not config:
            return
        self.printer = PanelPrinter.get(self.window.id())
        file = self.get_path(paths)
        view = self.window.active_view()
        self.on_complete = None
        if view and view.file_name() == file:
            self.on_complete = lambda : view.run_command('revert')
        self.remote_file = local_to_remote(file, config['path_map'])
        self.config = config
        if not config['confirm_downloads']:
            self.do_download()
            return
        debug_print('SFTP: Starting Confirm Download File Thread', 2)
        basename = os.path.basename(file)
        if os.name != 'nt':
            basename = unicodedata.normalize('NFC', basename)
        choices = [['Yes', u'Download the file %s' % basename], ['No', u'Do not download the file %s' % basename]]

        def on_choose(index):
            if index == -1 or index == 1:
                return
            self.do_download()

        self.window.show_quick_panel(choices, on_choose)

    def do_download(self):
        self.printer.show()
        debug_print('SFTP: Starting Download File Thread', 2)
        SftpThread(self.window.id(), self.config, self.remote_file, 'get', on_complete=self.on_complete).start()

    def is_visible(self, paths = None):
        path = self.get_path(paths)
        if not path or os.path.isdir(path):
            return False
        return self.has_config(path)


class SftpUploadFolderCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None):
        config = self.get_config(paths)
        if not config:
            return
        dir = self.get_path(paths)
        if not os.path.isdir(dir):
            dir = dirname(dir)
        dir = canonicalize(dir, 'local')
        debug_print('SFTP: Starting Upload Folder Command Thread', 2)
        UploadFolderThread(self.window, config, dir, self.save_files).start()

    def is_visible(self, paths = None):
        if paths == None:
            active_view = self.window.active_view()
            if active_view and active_view.settings().get('is_remote'):
                return False
        path = self.get_path(paths)
        if not path:
            return False
        return self.has_config(path)


class UploadFolderThread(HookedThread):

    def __init__(self, window, config, dir, save_files):
        self.config = config
        self.printer = PanelPrinter.get(window.id())
        self.window_id = window.id()
        self.dir = dir
        self.save_files = save_files
        super(UploadFolderThread, self).__init__()

    def run(self):
        last_thread = ThreadTracker.get_last_added(self.window_id)
        ThreadTracker.add(self)
        if last_thread != None:
            last_thread.join()

        def do_run():
            self.printer.show()
            basename = os.path.basename(self.dir.rstrip('/\\'))
            progress = ProgressThread(self.printer, '\nUploading folder "%s"' % basename)
            paths = [self.dir]
            for root, dirs, files in os.walk(self.dir):
                paths.extend([ os.path.join(root, path) for path in dirs ])
                paths.extend([ os.path.join(root, path) for path in files ])

            paths, to_upload, ignored = ignore_paths(paths, self.config)
            paths.sort()
            message = '%d %s to upload' % (to_upload, 'files' if to_upload != 1 else 'file')
            if ignored:
                message += ', %d ignored' % ignored
            progress.stop(message)
            progress.join()
            if paths:
                if self.config['save_before_upload']:
                    self.save_files(paths)
                debug_print('SFTP: Starting Upload Folder Thread', 2)
                SftpThread(self.window_id, self.config, paths, 'put').start()
            else:
                self.printer.hide()

        sublime.set_timeout(do_run, 10)


class SftpSyncUpCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None, ignore_delete = False, on_complete = None):
        config = self.get_config(paths)
        if not config:
            return
        printer = PanelPrinter.get(self.window.id())
        printer.show()
        path = self.get_path(paths)
        if os.path.isdir(path):
            path = canonicalize(path, 'local')
        if os.name != 'nt':
            path = unicodedata.normalize('NFC', path)
        if config.get('sync_skip_deletes'):
            ignore_delete = True
        debug_print('SFTP: Starting Sync Up Command Thread', 2)
        SyncUpThread(self.window, config, path, self.save_files, ignore_delete, on_complete).start()

    def is_visible(self, paths = None):
        if paths == None:
            active_view = self.window.active_view()
            if active_view and active_view.settings().get('is_remote'):
                return False
        path = self.get_path(paths)
        if not path:
            return False
        return self.has_config(path)


class SyncUpThread(HookedThread, SyncThread):

    def __init__(self, window, config, path, save_files, ignore_delete, on_complete):
        self.config = config
        self.printer = PanelPrinter.get(window.id())
        self.window = window
        self.window_id = window.id()
        self.path = path
        self.save_files = save_files
        self.ignore_delete = ignore_delete
        self.on_complete = on_complete
        super(SyncUpThread, self).__init__()

    def run(self):
        last_thread = ThreadTracker.get_last_added(self.window_id)
        ThreadTracker.add(self)
        if last_thread != None:
            last_thread.join()
        path_map = self.config['path_map']
        path = self.path
        remote_path = local_to_remote(path, path_map, self.config['remote_encoding'])
        list_operation = 'listr' if is_dir(path) else 'list'
        nonlocal = {'progress': None}

        def on_connect():
            nonlocal['progress'] = ProgressThread(self.printer, '\nDetermining operations to sync local path "%s" up to remote path "%s"' % (path, remote_path))

        def on_fail(e):
            if nonlocal['progress']:
                nonlocal['progress'].stop('failure (%s)' % str(e))
                nonlocal['progress'].join()

        dir = path if is_dir(path) else dirname(path)
        remote_dir = local_to_remote(dir, path_map, self.config['remote_encoding'])
        list_dir_thread = SftpThread(self.window_id, self.config, remote_dir, list_operation, should_join=False, hide=False, on_connect=on_connect, on_fail=on_fail, quiet=True, skip_symlinks=False)
        list_dir_thread.start()
        list_dir_thread.join()
        if list_dir_thread.failed and list_dir_thread.result in ('File not found', 'Folder not found'):
            remote_paths = []
        else:
            if list_dir_thread.failed:
                return
            remote_paths = list_dir_thread.result
        list_dir_thread = SftpThread(self.window_id, self.config, dir, 'l' + list_operation, should_join=False, hide=False)
        list_dir_thread.start()
        list_dir_thread.join()
        if list_dir_thread.failed and list_dir_thread.result in ('File not found', 'Folder not found'):
            local_paths = []
        else:
            if list_dir_thread.failed:
                return
            local_paths = list_dir_thread.result
        if not is_dir(path):
            local_paths = [ [os.path.join(dir, _path[0]), _path[1]] for _path in local_paths if os.path.join(dir, _path[0]) == path ]
            remote_paths = [ [os.path.join(remote_dir, _path[0]), _path[1]] for _path in remote_paths if os.path.join(remote_dir, _path[0]) == remote_path ]
        local_dict = dict(local_paths)
        remote_dict = dict(remote_paths)
        to_rm = set([ path[0] for path in remote_paths ])
        to_put = []
        for local_path, local_time in local_paths:
            remote_path = local_to_remote(local_path, path_map)
            remote_time = remote_dict.get(remote_path)
            if remote_time == None or remote_time <= local_time and not is_dir(local_path):
                to_put.append(local_path)
            to_rm = to_rm - set([remote_path])

        to_rm = list(to_rm)
        to_rm = sorted(to_rm, key=lambda s: s.lower())
        to_put, num_to_put, num_to_put_ignored = ignore_paths(to_put, self.config)
        to_rm, num_to_rm, num_to_rm_ignored = ignore_rm_paths(to_rm, self.config, 'remote')
        if self.ignore_delete:
            to_rm = []
        operations = []
        for local_path in to_put:
            local_time = self.make_time(local_dict.get(local_path))
            remote_path = local_to_remote(local_path, path_map)
            remote_time = self.make_time(remote_dict.get(remote_path))
            if is_dir(remote_path):
                operation = 'Create remote "%s"' % self.strip(remote_path, remote_dir, 'remote')
            elif remote_time == 'None':
                operation = 'Upload local "%s" to remote "%s"' % (self.strip(local_path, dir, 'local'), self.strip(remote_path, remote_dir, 'remote'))
            else:
                operation = u'Upload local "%s" (%s) over remote "%s" [%s vs. %s]' % (self.strip(local_path, dir, 'local'),
                 time_diff(local_dict.get(local_path), remote_dict.get(remote_path)),
                 self.strip(remote_path, remote_dir, 'remote'),
                 local_time,
                 remote_time)
            operations.append(operation)

        operations += [ 'Delete remote path "%s"' % self.strip(path, remote_dir, 'remote') for path in to_rm ]
        if operations:
            if nonlocal['progress']:
                nonlocal['progress'].stop('success')
                nonlocal['progress'].join()

            def handle_yes():
                failed = False
                if to_rm:
                    to_rm.reverse()
                    rm_thread = SftpThread(self.window_id, self.config, to_rm, 'rm', should_join=False)
                    rm_thread.start()
                    rm_thread.join()
                    if not failed:
                        failed = rm_thread.failed
                    if to_put:
                        put_thread = SftpThread(self.window_id, self.config, to_put, 'put', should_join=False)
                        put_thread.start()
                        put_thread.join()
                        if not failed:
                            failed = put_thread.failed
                        not failed and self.on_complete and self.on_complete()
                    failed or sublime.set_timeout(lambda : self.printer.hide(), 1)

            if self.config.get('confirm_sync'):

                def handle_no():
                    sublime.set_timeout(lambda : self.printer.hide(), 1)

                self.confirm(operations, handle_yes, handle_no, should_join=True)
            else:
                handle_yes()
        else:
            if nonlocal['progress']:
                nonlocal['progress'].stop('success (No operations to perform)')
                nonlocal['progress'].join()
            sublime.set_timeout(lambda : self.printer.hide(), 1)


class SftpSyncDownCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None, ignore_delete = False, on_complete = None, reset_lcd = None, synchronous = False):
        config = self.get_config(paths)
        if not config:
            return
        printer = PanelPrinter.get(self.window.id())
        printer.show()
        path = self.get_path(paths)
        if os.path.isdir(path):
            path = canonicalize(path, 'local')
        if os.name != 'nt':
            path = unicodedata.normalize('NFC', path)
        if config.get('sync_skip_deletes'):
            ignore_delete = True
        debug_print('SFTP: Starting Sync Down Command Thread', 2)
        SyncDownThread(self.window, config, path, self.save_files, ignore_delete, on_complete, reset_lcd, synchronous).start()

    def is_visible(self, paths = None):
        if paths == None:
            active_view = self.window.active_view()
            if active_view and active_view.settings().get('is_remote'):
                return False
        path = self.get_path(paths)
        if not path:
            return False
        return self.has_config(path)


class SyncDownThread(HookedThread, SyncThread):

    def __init__(self, window, config, path, save_files, ignore_delete, on_complete, reset_lcd, synchronous):
        self.config = config
        self.printer = PanelPrinter.get(window.id())
        self.window = window
        self.window_id = window.id()
        self.path = path
        self.save_files = save_files
        self.ignore_delete = ignore_delete
        self.on_complete = on_complete
        self.reset_lcd = reset_lcd
        self.synchronous = synchronous
        super(SyncDownThread, self).__init__()

    def run(self):
        last_thread = ThreadTracker.get_last_added(self.window_id)
        ThreadTracker.add(self)
        if last_thread != None:
            last_thread.join()
        path_map = self.config['path_map']
        path = self.path
        remote_path = local_to_remote(path, path_map, self.config['remote_encoding'])
        list_operation = 'listr' if is_dir(path) else 'list'
        nonlocal = {'progress': None}

        def on_connect():
            nonlocal['progress'] = ProgressThread(self.printer, '\nDetermining operations to sync remote path "%s" down to local path "%s"' % (remote_path, path))

        def on_fail(e):
            if nonlocal['progress']:
                nonlocal['progress'].stop('failure (%s)' % str(e))
                nonlocal['progress'].join()

        dir = path if is_dir(path) else canonicalize(dirname(path), 'local')
        remote_dir = local_to_remote(dir, path_map, self.config['remote_encoding'])
        list_dir_thread = SftpThread(self.window_id, self.config, remote_dir, list_operation, should_join=False, hide=False, on_connect=on_connect, on_fail=on_fail, quiet=True, skip_symlinks=False)
        list_dir_thread.start()
        list_dir_thread.join()
        if list_dir_thread.failed and list_dir_thread.result in ('File not found', 'Folder not found'):
            remote_paths = []
        else:
            if list_dir_thread.failed:
                return
            remote_paths = list_dir_thread.result
        list_dir_thread = SftpThread(self.window_id, self.config, dir, 'l' + list_operation, should_join=False, hide=False)
        list_dir_thread.start()
        list_dir_thread.join()
        if list_dir_thread.failed and list_dir_thread.result in ('File not found', 'Folder not found'):
            local_paths = []
        else:
            if list_dir_thread.failed:
                return
            local_paths = list_dir_thread.result
        if not is_dir(path):
            local_paths = [ [os.path.join(dir, _path[0]), _path[1]] for _path in local_paths if os.path.join(dir, _path[0]) == path ]
            remote_paths = [ [os.path.join(remote_dir, _path[0]), _path[1]] for _path in remote_paths if os.path.join(remote_dir, _path[0]) == remote_path ]
        local_dict = dict(local_paths)
        remote_dict = dict(remote_paths)
        to_rm = set([ path[0] for path in local_paths ])
        to_get = []
        for remote_path, remote_time in remote_paths:
            local_path = remote_to_local(remote_path, path_map)
            local_time = local_dict.get(local_path)
            if local_time == None or local_time <= remote_time and not is_dir(local_path):
                to_get.append(remote_path)
            to_rm = to_rm - set([local_path])

        to_rm = list(to_rm)
        to_rm = sorted(to_rm, key=lambda s: s.lower())
        to_get, num_to_get, num_to_get_ignored = ignore_paths(to_get, self.config)
        to_rm, num_to_rm, num_to_rm_ignored = ignore_rm_paths(to_rm, self.config, 'local')
        if self.ignore_delete:
            to_rm = []
        operations = []
        for remote_path in to_get:
            remote_time = self.make_time(remote_dict.get(remote_path))
            local_path = remote_to_local(remote_path, path_map)
            local_time = self.make_time(local_dict.get(local_path))
            if is_dir(local_path):
                operation = 'Create local "%s"' % self.strip(local_path, dir, 'local')
            elif local_time == 'None':
                operation = 'Download remote "%s" to "%s"' % (self.strip(remote_path, remote_dir, 'remote'), self.strip(local_path, dir, 'local'))
            else:
                operation = u'Download remote "%s" (%s) over local "%s" [%s vs. %s]' % (self.strip(remote_path, remote_dir, 'remote'),
                 time_diff(remote_dict.get(remote_path), local_dict.get(local_path)),
                 self.strip(local_path, dir, 'local'),
                 remote_time,
                 local_time)
            operations.append(operation)

        operations += [ 'Delete local "%s"' % self.strip(path, dir, 'local') for path in to_rm ]
        if operations:
            if nonlocal['progress']:
                nonlocal['progress'].stop('success')
                nonlocal['progress'].join()
            nonlocal['done'] = False

            def handle_yes():
                failed = False
                if to_rm:
                    to_rm.reverse()
                    rm_thread = SftpThread(self.window_id, self.config, to_rm, 'lrm', should_join=False)
                    rm_thread.start()
                    rm_thread.join()
                    if not failed:
                        failed = rm_thread.failed
                    if to_get:
                        get_thread = SftpThread(self.window_id, self.config, to_get, 'get', should_join=False, reset_lcd=self.reset_lcd)
                        get_thread.start()
                        get_thread.join()
                        if not failed:
                            failed = get_thread.failed
                        if not failed and self.on_complete and self.on_complete == 'open_refresh':

                            def do_refresh():
                                if not to_get:
                                    return
                                local_path = remote_to_local(to_get[0], path_map)
                                self.window.run_command('open_file', {'file': fix_windows_path(local_path)})
                                self.window.active_view().run_command('revert')

                            sublime.set_timeout(do_refresh, 1)
                        else:
                            self.on_complete()
                    failed or sublime.set_timeout(lambda : self.printer.hide(), 1)
                nonlocal['done'] = True

            if self.config.get('confirm_sync'):

                def handle_no():
                    sublime.set_timeout(lambda : self.printer.hide(), 1)
                    nonlocal['done'] = True

                self.confirm(operations, handle_yes, handle_no, should_join=not self.synchronous)
                if self.synchronous:
                    while True:
                        if nonlocal['done']:
                            break
                        time.sleep(0.01)

            else:
                handle_yes()
        else:
            if nonlocal['progress']:
                nonlocal['progress'].stop('success (No operations to perform)')
                nonlocal['progress'].join()
            sublime.set_timeout(lambda : self.printer.hide(), 1)


class SftpSyncBothCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None, on_complete = None):
        config = self.get_config(paths)
        if not config:
            return
        printer = PanelPrinter.get(self.window.id())
        printer.show()
        path = self.get_path(paths)
        if os.path.isdir(path):
            path = canonicalize(path, 'local')
        if os.name != 'nt':
            path = unicodedata.normalize('NFC', path)
        debug_print('SFTP: Starting Sync Both Command Thread', 2)
        SyncBothThread(self.window, config, path, self.save_files, on_complete).start()

    def is_visible(self, paths = None):
        if paths == None:
            active_view = self.window.active_view()
            if active_view and active_view.settings().get('is_remote'):
                return False
        path = self.get_path(paths)
        if not path:
            return False
        return self.has_config(path)


class SyncBothThread(HookedThread, SyncThread):

    def __init__(self, window, config, path, save_files, on_complete):
        self.config = config
        self.printer = PanelPrinter.get(window.id())
        self.window = window
        self.window_id = window.id()
        self.path = path
        self.save_files = save_files
        self.on_complete = on_complete
        super(SyncBothThread, self).__init__()

    def run(self):
        last_thread = ThreadTracker.get_last_added(self.window_id)
        ThreadTracker.add(self)
        if last_thread != None:
            last_thread.join()
        path_map = self.config['path_map']
        path = self.path
        remote_path = local_to_remote(path, path_map, self.config['remote_encoding'])
        nonlocal = {'progress': None}

        def on_connect():
            nonlocal['progress'] = ProgressThread(self.printer, '\nDetermining operations to sync local path "%s" both directions with remote path "%s"' % (path, remote_path))

        def on_fail(e):
            if nonlocal['progress']:
                nonlocal['progress'].stop('failure (%s)' % str(e))
                nonlocal['progress'].join()

        dir = path if is_dir(path) else dirname(path)
        remote_dir = local_to_remote(dir, path_map, self.config['remote_encoding'])
        list_dir_thread = SftpThread(self.window_id, self.config, remote_dir, 'listr', should_join=False, hide=False, on_connect=on_connect, on_fail=on_fail, quiet=True, skip_symlinks=False)
        list_dir_thread.start()
        list_dir_thread.join()
        if list_dir_thread.failed and list_dir_thread.result in ('File not found', 'Folder not found'):
            remote_paths = []
        else:
            if list_dir_thread.failed:
                return
            remote_paths = list_dir_thread.result
        list_dir_thread = SftpThread(self.window_id, self.config, dir, 'llistr', should_join=False, hide=False)
        list_dir_thread.start()
        list_dir_thread.join()
        if list_dir_thread.failed and list_dir_thread.result in ('File not found', 'Folder not found'):
            local_paths = []
        else:
            if list_dir_thread.failed:
                return
            local_paths = list_dir_thread.result
        if not is_dir(path):
            local_paths = [ _path for _path in local_paths if _path[0] == path ]
            remote_paths = [ _path for _path in remote_paths if _path[0] == remote_path ]
        local_dict = dict(local_paths)
        remote_dict = dict(remote_paths)
        to_put = []
        to_get = []
        for local_path, local_time in local_paths:
            remote_path = local_to_remote(local_path, path_map)
            remote_time = remote_dict.get(remote_path)
            if remote_time == None or remote_time <= local_time and not is_dir(local_path):
                to_put.append(local_path)

        for remote_path, remote_time in remote_paths:
            local_path = remote_to_local(remote_path, path_map)
            local_time = local_dict.get(local_path)
            if local_time == None or local_time < remote_time and not is_dir(remote_path):
                to_get.append(remote_path)

        to_put, num_to_put, num_to_put_ignored = ignore_paths(to_put, self.config)
        to_get, num_to_get, num_to_get_ignored = ignore_paths(to_get, self.config)
        operations = []
        for local_path in to_put:
            local_time = self.make_time(local_dict.get(local_path))
            remote_path = local_to_remote(local_path, path_map)
            remote_time = self.make_time(remote_dict.get(remote_path))
            if is_dir(remote_path):
                operation = 'Create remote "%s"' % self.strip(remote_path, remote_dir, 'remote')
            elif remote_time == 'None':
                operation = 'Upload local "%s" to remote "%s"' % (self.strip(local_path, dir, 'local'), self.strip(remote_path, remote_dir, 'remote'))
            else:
                operation = u'Upload local "%s" (%s) over remote "%s" [%s vs. %s]' % (self.strip(local_path, dir, 'local'),
                 time_diff(local_dict.get(local_path), remote_dict.get(remote_path)),
                 self.strip(remote_path, remote_dir, 'remote'),
                 local_time,
                 remote_time)
            operations.append(operation)

        for remote_path in to_get:
            remote_time = self.make_time(remote_dict.get(remote_path))
            local_path = remote_to_local(remote_path, path_map)
            local_time = self.make_time(local_dict.get(local_path))
            if is_dir(local_path):
                operation = 'Create local "%s"' % self.strip(local_path, dir, 'local')
            elif local_time == 'None':
                operation = 'Download remote "%s" to "%s"' % (self.strip(remote_path, remote_dir, 'remote'), self.strip(local_path, dir, 'local'))
            else:
                operation = u'Download remote "%s" (%s) over local "%s" [%s vs. %s]' % (self.strip(remote_path, remote_dir, 'remote'),
                 time_diff(remote_dict.get(remote_path), local_dict.get(local_path)),
                 self.strip(local_path, dir, 'local'),
                 remote_time,
                 local_time)
            operations.append(operation)

        if operations:
            if nonlocal['progress']:
                nonlocal['progress'].stop('success')
                nonlocal['progress'].join()

            def handle_yes():
                failed = False
                if to_put:
                    put_thread = SftpThread(self.window_id, self.config, to_put, 'put', should_join=False)
                    put_thread.start()
                    put_thread.join()
                    if not failed:
                        failed = put_thread.failed
                    if to_get:
                        get_thread = SftpThread(self.window_id, self.config, to_get, 'get', should_join=False)
                        get_thread.start()
                        get_thread.join()
                        if not failed:
                            failed = get_thread.failed
                        not failed and self.on_complete and self.on_complete()
                    failed or sublime.set_timeout(lambda : self.printer.hide(), 1)

            if self.config.get('confirm_sync'):

                def handle_no():
                    sublime.set_timeout(lambda : self.printer.hide(), 1)

                self.confirm(operations, handle_yes, handle_no, should_join=True)
            else:
                handle_yes()
        else:
            if nonlocal['progress']:
                nonlocal['progress'].stop('success (No operations to perform)')
                nonlocal['progress'].join()
            sublime.set_timeout(lambda : self.printer.hide(), 1)


class SftpDownloadFolderCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None):
        config = self.get_config(paths)
        if not config:
            return
        self.printer = PanelPrinter.get(self.window.id())
        dir = self.get_path(paths)
        if not os.path.isdir(dir):
            dir = dirname(dir)
        self.remote_dir = local_to_remote(dir, config['path_map'])
        self.config = config
        if not config['confirm_downloads']:
            self.do_download()
            return
        debug_print('SFTP: Starting Confirm Download Folder Thread', 2)
        basename = os.path.basename(dir)
        if os.name != 'nt':
            basename = unicodedata.normalize('NFC', basename)
        choices = [['Yes', u'Download the folder %s' % basename], ['No', u'Do not download the folder %s' % basename]]

        def on_choose(index):
            if index == -1 or index == 1:
                return
            self.do_download()

        self.window.show_quick_panel(choices, on_choose)

    def do_download(self):
        self.printer.show()
        debug_print('SFTP: Starting Download Folder Command Thread', 2)
        DownloadFolderThread(self.window.id(), self.config, self.remote_dir).start()

    def is_visible(self, paths = None):
        if paths == None:
            active_view = self.window.active_view()
            if active_view and active_view.settings().get('is_remote'):
                return False
        path = self.get_path(paths)
        if not path:
            return False
        return self.has_config(path)


class DownloadFolderThread(HookedThread):

    def __init__(self, window_id, config, remote_dir):
        self.config = config
        self.printer = PanelPrinter.get(window_id)
        self.window_id = window_id
        self.remote_dir = remote_dir
        self.error = False
        super(DownloadFolderThread, self).__init__()

    def run(self):
        last_thread = ThreadTracker.get_last_added(self.window_id)
        ThreadTracker.add(self)
        if last_thread != None:
            last_thread.join()
        nonlocal = {'progress': None}

        def on_connect():
            nonlocal['progress'] = ProgressThread(self.printer, '\nDownloading folder "%s"' % self.remote_dir)

        list_dir_thread = SftpThread(self.window_id, self.config, self.remote_dir, 'listr', should_join=False, on_connect=on_connect, hide=False, skip_symlinks=False)
        list_dir_thread.start()
        list_dir_thread.join()
        remote_paths = list_dir_thread.result
        if remote_paths != None:
            remote_paths = [ path[0] for path in remote_paths ]
            remote_paths, to_download, ignored = ignore_paths(remote_paths, self.config)
            message = ' %d %s to download' % (to_download, 'files' if to_download != 1 else 'file')
            if ignored:
                message += ', %d ignored' % ignored
        else:
            message = 'failure (Error)'
        if nonlocal['progress']:
            nonlocal['progress'].stop(message)
            nonlocal['progress'].join()
        if remote_paths:
            debug_print('SFTP: Starting Download Folder Thread', 2)
            download_thread = SftpThread(self.window_id, self.config, remote_paths, 'get', should_join=False)
            download_thread.start()
            download_thread.join()
            self.error = download_thread.failed
        else:
            sublime.set_timeout(lambda : self.printer.hide(), 1)


class SftpVcsChangedFilesCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self):
        config = self.get_config()
        if not config:
            return
        printer = PanelPrinter.get(self.window.id())
        printer.show()
        vcs = None
        path = self.get_path()
        settings = sublime.load_settings('SFTP.sublime-settings')
        vcses = [(SVN, settings.get('svn_binary_path')), (Git, settings.get('git_binary_path')), (Hg, settings.get('hg_binary_path'))]
        for vcs_class, binary_path in vcses:
            try:
                vcs = vcs_class(path, binary_path)
            except NotFoundError:
                pass

        if vcs == None:
            printer.write('\nLooking for changed files ... failure')
            printer.error('The current file does not appear to be inside ' + 'of an SVN, Git or Mercurial working copy')
            return
        if config['save_before_upload']:
            self.save_files()
        debug_print('SFTP: Starting VCS Command Thread', 2)
        VcsThread(self.window, config, vcs).start()

    def is_visible(self, paths = None):
        path = self.get_path(paths)
        if not path or os.path.isdir(path):
            return False
        return self.has_config(path)


class VcsThread(HookedThread):

    def __init__(self, window, config, vcs):
        self.window_id = window.id()
        self.printer = PanelPrinter.get(window.id())
        self.config = config
        self.vcs = vcs
        super(VcsThread, self).__init__()

    def run(self):
        last_thread = ThreadTracker.get_last_added(self.window_id)
        ThreadTracker.add(self)
        if last_thread != None:
            last_thread.join()
        progress = ProgressThread(self.printer, '\nLooking for changed files')
        try:
            files = self.vcs.list_changed_files()
            files = [ file for file in files if re.match(re.escape(self.config['local_dir']), file) != None ]
        except NotFoundError as e:
            progress.stop('failure\n' + str(e))
            progress.join()
            self.printer.error(e)
            return

        to_upload = len(files)
        ignored = 0
        if 'ignore_regex' in self.config:
            files = [ file for file in files if not re.search(self.config['ignore_regex'], file) ]
            ignored = to_upload - len(files)
            to_upload = len(files)
        message = '%d %s to upload' % (to_upload, 'files' if to_upload != 1 else ' file')
        if ignored:
            message += ', %d ignored' % ignored
        progress.stop(message)
        progress.join()
        if files:
            debug_print('SFTP: Starting VCS Thread', 2)
            SftpThread(self.window_id, self.config, files, 'put').start()
        else:
            sublime.set_timeout(self.printer.hide, 10)


class SftpCancelUploadCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self):
        current_thread = ThreadTracker.get_current(self.window.id())
        if current_thread:
            current_thread.kill()

    def is_visible(self, paths = None):
        return ThreadTracker.get_current(self.window.id()) != None


class SftpEditConfigCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None):
        path = self.get_path(paths)
        if not path:
            return
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        file = find_config(path, True)
        file = fix_windows_path(file)
        self.window.run_command('open_file', {'file': file})

    def is_visible(self, paths = None):
        path = self.get_path(paths)
        if not path:
            return False
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        config_file = find_config(path, True)
        return config_file != False

    def is_enabled(self, paths = None):
        path = self.get_path(paths)
        if not path:
            return False
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        config_file = find_config(path, True)
        return config_file != False


class SftpCreateConfigCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths):
        path = self.get_path(paths)
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        file = os.path.join(path, 'sftp-config.json')
        self.create_default_config(file)

        def open_file():
            self.window.run_command('open_file', {'file': fix_windows_path(file)})

            def run_snippet():
                snippet = get_default_config()
                view = self.window.active_view()
                view.sel().add(sublime.Region(0, view.size()))
                view.run_command('insert_snippet', {'contents': snippet})

            sublime.set_timeout(run_snippet, 350)

        sublime.set_timeout(open_file, 350)

    def is_visible(self, paths = None):
        path = self.get_path(paths)
        if not path:
            return False
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        return find_config(path, True) == False

    def is_enabled(self, paths = None):
        path = self.get_path(paths)
        if not path:
            return False
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        return find_config(path, True) == False


class SftpSwitchConfigCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None):
        path = self.get_path(paths)
        if not path:
            return
        config_file = find_config(path, True)
        if config_file == False:
            return
        self.config_dir = os.path.dirname(config_file)

        def add_desc(config):
            remote_type = config.get('type', 'sftp').upper()
            user = config.get('user')
            host = config.get('host')
            remote_path = config.get('remote_path')
            port = ':' + str(config.get('port')) if config.get('port') else ''
            config['desc'] = u'%s %s@%s%s %s' % (remote_type,
             user,
             host,
             port,
             remote_path)
            return config

        alt_config_files = []
        alt_configs = {}
        for num in ['',
         '2',
         '3',
         '4',
         '5',
         '6',
         '7',
         '8',
         '9']:
            alt_config_file = config_file.replace('sftp-settings.json', 'sftp-config.json')[0:-5] + '-alt' + num + '.json'
            if os.path.exists(alt_config_file):
                alt_config_files.append(alt_config_file)
                alt_configs[alt_config_file] = add_desc(parse_config(alt_config_file))

        config = add_desc(parse_config(config_file))
        self.choices = [[config['desc'], os.path.basename(config_file)]]
        for alt_config_file in alt_config_files:
            self.choices.append([alt_configs[alt_config_file]['desc'], os.path.basename(alt_config_file)])

        self.window_id = self.window.id()
        self.printer = PanelPrinter.get(self.window_id)
        self.window.show_quick_panel(self.choices, self.on_done)

    def on_done(self, index):
        if index == -1:
            return
        if index == 0:
            return
        main_config_file = os.path.join(self.config_dir, self.choices[0][1])
        alt_config_file = os.path.join(self.config_dir, self.choices[index][1])
        original_config = ''
        with open(main_config_file, 'rb') as f:
            original_config = f.read()
        new_config = ''
        with open(alt_config_file, 'rb') as f:
            new_config = f.read()
        with open(main_config_file, 'wb') as f:
            f.write(new_config)
        with open(alt_config_file, 'wb') as f:
            f.write(original_config)

    def is_visible(self, paths = None):
        path = self.get_path(paths)
        if not path:
            return False
        config_file = find_config(path, True)
        if config_file == False:
            return False
        alt_config_file = config_file.replace('sftp-settings.json', 'sftp-config.json')[0:-5] + '-alt.json'
        if os.path.exists(alt_config_file):
            return True
        return False


class SftpCreateAltConfigCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, paths = None):
        path = self.get_path(paths)
        if not path:
            return
        config_file = find_config(path, True)
        if config_file == False:
            return
        new_config_file = None
        for num in ['',
         '2',
         '3',
         '4',
         '5',
         '6',
         '7',
         '8',
         '9']:
            alt_config_file = config_file.replace('sftp-settings.json', 'sftp-config.json')[0:-5] + '-alt' + num + '.json'
            if not os.path.exists(alt_config_file):
                new_config_file = alt_config_file
                break

        if not new_config_file:
            sublime.error_message('SFTP: There can not be more than 9 alternate configs')
            return False
        original_config = ''
        with open(config_file, 'rb') as f:
            original_config = f.read()
        with open(new_config_file, 'wb') as f:
            f.write(original_config)
        self.window.run_command('open_file', {'file': fix_windows_path(new_config_file)})

    def is_visible(self, paths = None):
        path = self.get_path(paths)
        if not path:
            return False
        config_file = find_config(path, True)
        if config_file == False:
            return False
        return True


class SftpCreateSubConfigCommand(sublime_plugin.WindowCommand, SftpCommand):

    def run(self, dirs):
        file = os.path.join(dirs[0], 'sftp-config.json')
        self.create_default_config(file)
        file = fix_windows_path(file)
        self.window.run_command('open_file', {'file': file})

    def is_visible(self, dirs):
        path = self.first_path(dirs)
        config_file = find_config(path, True)
        return config_file != False and os.path.dirname(config_file) != path

    def is_enabled(self, dirs):
        path = self.first_path(dirs)
        config_file = find_config(path, True)
        return config_file != False and os.path.dirname(config_file) != path