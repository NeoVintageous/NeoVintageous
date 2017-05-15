import sublime
import sublime_plugin


__all__ = [
    '_vi_cmd_line_a',
    '_vi_cmd_line_k'
]


# TODO command appears to be unused
class _vi_cmd_line_a(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(1))


# TODO command appears to be unused
class _vi_cmd_line_k(sublime_plugin.TextCommand):
    def run(self, edit):
        text = self.view.substr(sublime.Region(0, self.view.sel()[0].b))
        self.view.replace(edit, sublime.Region(0, self.view.size()), text)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(self.view.size()))
