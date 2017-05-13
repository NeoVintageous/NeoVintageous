from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_big_s(ViewTestCase):

    def test_deletes_whole_line_in_internal_normal_mode(self):
        self.write('aaa aaa\nbbb bbb\nccc ccc\n')
        self.select(8)

        self.view.run_command('_vi_big_s_action', {'mode': self.modes.INTERNAL_NORMAL})

        self.assertContent('aaa aaa\n\nccc ccc\n')

        self.write('aaa aaa\nbbb bbb\nccc ccc\n')
        self.select(16)

        self.view.run_command('_vi_big_s_action', {'mode': self.modes.INTERNAL_NORMAL})

        self.assertContent('aaa aaa\nbbb bbb\n\n')

    def test_deletes_whole_line_and_reindents_in_internal_normal_mode(self):
        self.settings().set('translate_tabs_to_spaces', False)
        self.write("\taaa aaa\nbbb bbb\nccc ccc")
        self.select(9)

        self.view.run_command('_vi_big_s_action', {'mode': self.modes.INTERNAL_NORMAL})

        self.assertContent("\taaa aaa\n\t\nccc ccc")
