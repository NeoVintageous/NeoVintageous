from NeoVintageous.tests import unittest


class ExCopyTestCaseMixin:
    def _run_ex_copy(self, command_line):
        self.view.run_command('ex_copy', {'command_line': command_line})


class Test_ex_copy_Copying_InNormalMode_SingleLine_DefaultStart(ExCopyTestCaseMixin, unittest.ViewTestCase):

    def test_can_copy_default_line_range(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)
        self._run_ex_copy('copy3')
        self.assertContent('abc\nxxx\nabc\nxxx\nabc')

    def test_can_copy_to_eof(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)
        self._run_ex_copy('copy4')
        self.assertContent('abc\nxxx\nabc\nabc\nxxx')

    def test_can_copy_to_bof(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)
        self._run_ex_copy('copy0')
        self.assertContent('xxx\nabc\nxxx\nabc\nabc')

    def test_can_copy_to_empty_line(self):
        self.write('abc\nxxx\nabc\n\nabc')
        self.select(4)
        self._run_ex_copy('copy4')
        self.assertContent('abc\nxxx\nabc\n\nxxx\nabc')

    def test_can_copy_to_same_line(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)
        self._run_ex_copy('copy2')
        self.assertContent('abc\nxxx\nxxx\nabc\nabc')

    def test_bad_address_does_not_mutate_view(self):
        self.write('abc')
        self.select(0)
        self._run_ex_copy('copy 1,10')
        self.assertContent('abc')


class Test_ex_copy_Copying_InNormalMode_MultipleLines(ExCopyTestCaseMixin, unittest.ViewTestCase):

    def test_can_copy_default_line_range(self):
        self.write('abc\nxxx\nxxx\nabc\nabc')
        self.select(4)
        self._run_ex_copy('.,.+1copy4')
        self.assertContent('abc\nxxx\nxxx\nabc\nxxx\nxxx\nabc')

    def test_can_copy_to_eof(self):
        self.write('abc\nxxx\nxxx\nabc\nabc')
        self.select(4)
        self._run_ex_copy('.,.+1copy5')
        self.assertContent('abc\nxxx\nxxx\nabc\nabc\nxxx\nxxx')

    def test_can_copy_to_bof(self):
        self.write('abc\nxxx\nxxx\nabc\nabc')
        self.select(4)
        self._run_ex_copy('.,.+1copy0')
        self.assertContent('xxx\nxxx\nabc\nxxx\nxxx\nabc\nabc')

    def test_can_copy_to_empty_line(self):
        self.write('abc\nxxx\nxxx\nabc\n\nabc')
        self.select(4)
        self._run_ex_copy('.,.+1copy5')
        self.assertContent('abc\nxxx\nxxx\nabc\n\nxxx\nxxx\nabc')

    def test_can_copy_to_same_line(self):
        self.write('abc\nxxx\nxxx\nabc\nabc')
        self.select(4)
        self._run_ex_copy('.,.+1copy2')
        self.assertContent('abc\nxxx\nxxx\nxxx\nxxx\nabc\nabc')


class Test_ex_copy_InNormalMode_CaretPosition(ExCopyTestCaseMixin, unittest.ViewTestCase):

    def test_can_reposition_caret(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)
        self._run_ex_copy('copy 3')
        self.assertContent('abc\nxxx\nabc\nxxx\nabc')
        self.assertSelection(12)


class Test_ex_copy_ModeTransition(ExCopyTestCaseMixin, unittest.ViewTestCase):

    def test_from_normal_mode_to_normal_mode(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select(4)
        self._run_ex_copy('copy 3')
        self.assertNormalMode()

    def test_from_visual_mode_to_normal_mode(self):
        self.write('abc\nxxx\nabc\nabc')
        self.select((4, 5))
        self._run_ex_copy('copy 3')
        self.assertNormalMode()
