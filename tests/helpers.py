import sublime
import sublime_plugin


class __vi_tests_write_buffer(sublime_plugin.TextCommand):
    """Replaces the buffer's content with the specified `text`.

       `text`: Text to be written to the buffer.
    """
    def run(self, edit, text=''):
        self.view.replace(edit, sublime.Region(0, self.view.size()), text)
