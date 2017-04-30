import sublime
import sublime_plugin


class __vi_tests_write_buffer(sublime_plugin.TextCommand):

    """
    Replaces buffer content with the specified text.
    """

    def run(self, edit, text=''):
        self.view.replace(edit, sublime.Region(0, self.view.size()), text)
