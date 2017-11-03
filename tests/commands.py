from sublime import Region
from sublime_plugin import TextCommand


class __neovintageous_test_write(TextCommand):

    def run(self, edit, text=''):
        self.view.replace(edit, Region(0, self.view.size()), text)
