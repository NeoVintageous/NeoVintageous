from sublime import Region
from sublime_plugin import TextCommand


__all__ = [
    '_vi_cmd_line_a',
    '_vi_cmd_line_k'
]


# TODO command appears to be unused
class _vi_cmd_line_a(TextCommand):
    def run(self, edit):
        self.view.sel().clear()
        self.view.sel().add(Region(1))


# TODO command appears to be unused
class _vi_cmd_line_k(TextCommand):
    def run(self, edit):
        text = self.view.substr(Region(0, self.view.sel()[0].b))
        self.view.replace(edit, Region(0, self.view.size()), text)
        self.view.sel().clear()
        self.view.sel().add(Region(self.view.size()))
