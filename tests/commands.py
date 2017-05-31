import sublime
import sublime_plugin


class __neovintageous_test_write(sublime_plugin.TextCommand):

    def run(self, edit, text=''):
        self.view.replace(edit, sublime.Region(0, self.view.size()), text)
