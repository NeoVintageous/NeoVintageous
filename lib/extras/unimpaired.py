# https://github.com/tpope/vim-unimpaired
from sublime_plugin import TextCommand

from NeoVintageous.lib.api import plugin


__all__ = [
    'NeovintageousUnimpairedBlankUpCommand',
    'NeovintageousUnimpairedBlankDownCommand',
    'NeovintageousUnimpairedMoveUpCommand',
    'NeovintageousUnimpairedMoveDownCommand'
]


# LINE OPERATIONS                                 *unimpaired-lines*
# ------------------------------------------------------------------

@plugin.register(seq='[<space>', modes=(plugin.modes.NORMAL,))
class UnimpairedBlankUp(plugin.ViOperatorDef):
    def translate(self, state):
        return {
            'action': 'neovintageous_unimpaired_blank_up',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@plugin.register(seq=']<space>', modes=(plugin.modes.NORMAL,))
class UnimpairedBlankDown(plugin.ViOperatorDef):
    def translate(self, state):
        return {
            'action': 'neovintageous_unimpaired_blank_down',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@plugin.register(seq='[e', modes=(plugin.modes.NORMAL,))
class UnimpairedMoveUp(plugin.ViOperatorDef):
    def translate(self, state):
        return {
            'action': 'neovintageous_unimpaired_move_up',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


@plugin.register(seq=']e', modes=(plugin.modes.NORMAL,))
class UnimpairedMoveDown(plugin.ViOperatorDef):
    def translate(self, state):
        return {
            'action': 'neovintageous_unimpaired_move_down',
            'action_args': {
                'mode': state.mode,
                'count': state.count
            }
        }


# Add [count] blank lines above the cursor.
class NeovintageousUnimpairedBlankUpCommand(TextCommand):
    def run(self, edit, mode=None, count=1):
        new_sels = []
        for sel in self.view.sel():
            line = self.view.line(sel)
            new_sels.append(self.view.find('[^\\s]', line.begin()).begin() + count)
            self.view.insert(
                edit,
                line.begin() - 1 if line.begin() > 0 else 0,
                '\n' * count
            )

        if new_sels:
            self.view.sel().clear()
            self.view.sel().add_all(new_sels)


# Add [count] blank lines below the cursor.
class NeovintageousUnimpairedBlankDownCommand(TextCommand):
    def run(self, edit, mode=None, count=1):
        end_point = self.view.size()
        new_sels = []
        for sel in self.view.sel():
            line = self.view.line(sel)
            new_sels.append(self.view.find('[^\\s]', line.begin()).begin())
            self.view.insert(
                edit,
                line.end() + 1 if line.end() < end_point else end_point,
                '\n' * count
            )

        if new_sels:
            self.view.sel().clear()
            self.view.sel().add_all(new_sels)


# Exchange the current line with [count] lines above it.
class NeovintageousUnimpairedMoveUpCommand(TextCommand):
    def run(self, edit, mode=None, count=1):
        for i in range(count):
            self.view.run_command('swap_line_up')


# Exchange the current line with [count] lines below it.
class NeovintageousUnimpairedMoveDownCommand(TextCommand):
    def run(self, edit, mode=None, count=1):
        for i in range(count):
            self.view.run_command('swap_line_down')
