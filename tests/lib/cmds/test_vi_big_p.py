from collections import namedtuple

from NeoVintageous.tests import unittest

from NeoVintageous.lib.vi import registers


test_data = namedtuple('test_data', 'content regions in_register params expected msg')

TESTS = (
    # INTERNAL NORMAL MODE
    test_data(content='abc',
              regions=[[(0, 0), (0, 0)]],
              in_register=['xxx'], params={'mode': unittest.INTERNAL_NORMAL, 'count': 1},
              expected=('xxxabc', unittest.Region(2, 2)), msg='failed in {0}'),

    # INTERNAL NORMAL MODE - linewise
    test_data(content='abc',
              regions=[[(0, 0), (0, 0)]],
              in_register=['xxx\n'], params={'mode': unittest.INTERNAL_NORMAL, 'count': 1},
              expected=('xxx\nabc', unittest.Region(0, 0)), msg='failed in {0}'),

    # VISUAL MODE
    test_data(content='abc',
              regions=[[(0, 0), (0, 3)]],
              in_register=['xxx'], params={'mode': unittest.VISUAL, 'count': 1},
              expected=('xxx', unittest.Region(2, 2)), msg='failed in {0}'),

    # VISUAL MODE - linewise
    test_data(content='aaa bbb ccc',
              regions=[[(0, 4), (0, 7)]],
              in_register=['xxx\n'], params={'mode': unittest.VISUAL, 'count': 1},
              expected=('aaa \nxxx\n ccc', unittest.Region(5, 5)), msg='failed in {0}'),
)


class Test__vi_big_p(unittest.ViewTestCase):

    def test_all(self):
        for (i, data) in enumerate(TESTS):
            # TODO: Perhaps we should ensure that other state is reset too?
            self.write(data.content)
            self.select([self._R(*region) for region in data.regions])

            self.view.settings().set('vintageous_use_sys_clipboard', False)
            registers._REGISTER_DATA['"'] = data.in_register

            self.view.run_command('_vi_big_p', data.params)

            msg = "[{0}] {1}".format(i, data.msg)
            self.assertEqual(data.expected[0], self.content(), msg.format(i))
            self.assertEqual(data.expected[1], self.view.sel()[0], msg.format(i))
