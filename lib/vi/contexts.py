import sublime

from NeoVintageous.lib.vi.utils import modes
from NeoVintageous.lib.vi import utils


class KeyContext(object):
    def __get__(self, instance, owner):
        self.state = instance
        return self

    def vi_is_view(self, key, operator, operand, match_all):
        value = utils.is_view(self.state.view)
        return self._check(value, operator, operand, match_all)

    def vi_command_mode_aware(self, key, operator, operand, match_all):
        in_command_mode = self.state.view.settings().get('command_mode')
        is_view = self.vi_is_view(key, operator, operand, match_all)
        value = in_command_mode and is_view
        return self._check(value, operator, operand, match_all)

    def vi_insert_mode_aware(self, key, operator, operand, match_all):
        in_command_mode = self.state.view.settings().get('command_mode')
        is_view = self.vi_is_view(key, operator, operand, match_all)
        value = (not in_command_mode) and is_view
        return self._check(value, operator, operand, match_all)

    def vi_use_ctrl_keys(self, key, operator, operand, match_all):
        value = self.state.settings.view['vintageous_use_ctrl_keys']
        return self._check(value, operator, operand, match_all)

    def vi_is_cmdline(self, key, operator, operand, match_all):
        value = (self.state.view.score_selector(0, 'text.excmdline') != 0)
        return self._check(value, operator, operand, match_all)

    def vi_enable_cmdline_mode(self, key, operator, operand, match_all):
        value = self.state.settings.view['vintageous_enable_cmdline_mode']
        return self._check(value, operator, operand, match_all)

    def vi_mode_normal_insert(self, key, operator, operand, match_all):
        value = self.state.mode == modes.NORMAL_INSERT
        return self._check(value, operator, operand, match_all)

    def vi_mode_visual_block(self, key, operator, operand, match_all):
        value = self.state.mode == modes.VISUAL_BLOCK
        return self._check(value, operator, operand, match_all)

    def vi_mode_select(self, key, operator, operand, match_all):
        value = self.state.mode == modes.SELECT
        return self._check(value, operator, operand, match_all)

    def vi_mode_visual_line(self, key, operator, operand, match_all):
        value = self.state.mode == modes.VISUAL_LINE
        return self._check(value, operator, operand, match_all)

    def vi_mode_insert(self, key, operator, operand, match_all):
        value = self.state.mode == modes.INSERT
        return self._check(value, operator, operand, match_all)

    def vi_mode_visual(self, key, operator, operand, match_all):
        value = self.state.mode == modes.VISUAL
        return self._check(value, operator, operand, match_all)

    def vi_mode_normal(self, key, operator, operand, match_all):
        value = self.state.mode == modes.NORMAL
        return self._check(value, operator, operand, match_all)

    def vi_mode_normal_or_visual(self, key, operator, operand, match_all):
        # XXX: This context is used to disable some keys for VISUALLINE.
        # However, this is hiding some problems in visual transformers that might not be dealing
        # correctly with VISUALLINE.
        normal = self.vi_mode_normal(key, operator, operand, match_all)
        visual = self.vi_mode_visual(key, operator, operand, match_all)
        visual = visual or self.vi_mode_visual_block(key, operator, operand, match_all)
        return self._check((normal or visual), operator, operand, match_all)

    def vi_mode_normal_or_any_visual(self, key, operator, operand, match_all):
        normal_or_visual = self.vi_mode_normal_or_visual(key, operator, operand, match_all)
        visual_line = self.vi_mode_visual_line(key, operator, operand, match_all)
        return self._check((normal_or_visual or visual_line), operator, operand, match_all)

    def check(self, key, operator, operand, match_all):
        func = getattr(self, key, None)
        if func:
            return func(key, operator, operand, match_all)
        else:
            return None

    def _check(self, value, operator, operand, match_all):
        if operator == sublime.OP_EQUAL:
            if operand is True:
                return value
            elif operand is False:
                return not value
        elif operator is sublime.OP_NOT_EQUAL:
            if operand is True:
                return not value
            elif operand is False:
                return value
