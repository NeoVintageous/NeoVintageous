from sublime import Region
from sublime_plugin import TextCommand


class _neovintageous_test_write(TextCommand):

    def run(self, edit, text):
        self.view.erase(edit, Region(0, self.view.size()))
        self.view.insert(edit, 0, text)
