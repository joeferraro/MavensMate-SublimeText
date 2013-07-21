import sublime
import threading
import sys

class HookedThread(threading.Thread):

    def __init__(self):
        run_old = self.run

        def run_with_except_hook(*args, **kw):
            try:
                run_old(*args, **kw)
            except (KeyboardInterrupt, SystemExit):
                raise 
            except:
                sys.excepthook(*sys.exc_info())

        self.run = run_with_except_hook
        threading.Thread.__init__(self)

class ThreadTracker(object):
    pending_threads = {}
    current_thread = {}

    @classmethod
    def add(cls, thread):
        cls.pending_threads[thread.window_id] = thread

    @classmethod
    def get_last_added(cls, window_id):
        return cls.pending_threads.get(window_id)

    @classmethod
    def set_current(cls, window_id, thread):
        cls.current_thread[window_id] = thread

    @classmethod
    def get_current(cls, window_id):
        return cls.current_thread.get(window_id)

def unset_current_thread(fn):

    def handler(self, *args, **kwargs):
        result = fn(self, *args, **kwargs)
        ThreadTracker.set_current(self.window_id, None)
        return result

    return handler

class PanelThreadProgress():
    """
    Animates an indicator, [=   ], in the MavensMate panel while a thread runs

    :param thread:
        The thread to track for activity

    :param message:
        The message to display next to the activity indicator

    :param success_message:
        The message to display once the thread is complete
    """

    def __init__(self, thread, success_message="TESTING", callback=None):
        self.thread = thread
        self.success_message = success_message
        self.addend = 1
        self.size = 8
        self.callback = None
        sublime.set_timeout(lambda: self.run(0), 100)

    def run(self, i):
        if not self.thread.is_alive():
            if hasattr(self.thread, 'result'):
                #thread is done, we need to handle the result
                self.thread.callback(self.thread.operation, self.thread.process_id, self.thread.printer, self.thread.result, self.thread)
                #self.thread.printer.panel.run_command('write_operation_status', {'text': self.thread.result, 'region': [self.thread.status_region.end(), self.thread.status_region.end()+10] })
                return
            if self.callback != None:
                self.callback()
            return

        #we need to recalculate this every run in case a thread has responded and added
        #text to the panel
        process_region = self.thread.printer.panel.find(self.thread.process_id,0)
        status_region = self.thread.printer.panel.find('Result:',process_region.begin())
        
        before = i % self.size
        after = (self.size - 1) - before

        text = '%s[%s=%s]' % \
            ('', ' ' * before, ' ' * after)

        self.thread.printer.panel.run_command('write_operation_status', {'text': text, 'region': [status_region.end(), status_region.end()+10] })

        if not after:
            self.addend = -1
        if not before:
            self.addend = 1
        i += self.addend

        sublime.set_timeout(lambda: self.run(i), 100)

class ThreadProgress():
    """
    Animates an indicator, [=   ], in the status area while a thread runs

    :param thread:
        The thread to track for activity

    :param message:
        The message to display next to the activity indicator

    :param success_message:
        The message to display once the thread is complete
    """

    def __init__(self, thread, message, success_message, callback=None):
        self.thread = thread
        self.message = message
        self.success_message = success_message
        self.addend = 1
        self.size = 8
        self.callback = None
        sublime.set_timeout(lambda: self.run(0), 100)

    def run(self, i):
        if not self.thread.is_alive():
            if hasattr(self.thread, 'result') and not self.thread.result:
                sublime.status_message('')
                return
            sublime.status_message(self.success_message)
            if self.callback != None:
                self.callback()
            return

        before = i % self.size
        after = (self.size - 1) - before

        sublime.status_message('%s [%s=%s]' % \
            (self.message, ' ' * before, ' ' * after))

        if not after:
            self.addend = -1
        if not before:
            self.addend = 1
        i += self.addend

        sublime.set_timeout(lambda: self.run(i), 100)