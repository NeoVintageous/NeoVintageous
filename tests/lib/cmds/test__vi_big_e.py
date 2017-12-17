from NeoVintageous.tests import unittest


class Test__vi_big_e(unittest.ViewTestCase):

    def test_normal(self):
        self.write('01. 4')
        self.select(1)
        self.view.run_command('_vi_big_e', {'mode': unittest.NORMAL_MODE, 'count': 1})
        self.assertSelection(2)

    def test_internal_normal(self):
        self.write('012 4')
        self.select(1)
        self.view.run_command('_vi_big_e', {'mode': unittest.INTERNAL_NORMAL_MODE, 'count': 1})
        self.assertSelection((1, 3))

    def test_visual_forward(self):
        self.write('0ab3 5')
        self.select((1, 3))
        self.view.run_command('_vi_big_e', {'mode': unittest.VISUAL_MODE, 'count': 1})
        self.assertSelection((1, 4))

    def test_visual_reverse_no_crossover(self):
        self.write('0b2 a5')
        self.select((5, 1))
        self.view.run_command('_vi_big_e', {'mode': unittest.VISUAL_MODE, 'count': 1})
        self.assertSelection((5, 2))

    def test_visual_reverse_crossover(self):
        self.write('0ba3 5')
        self.select((3, 1))
        self.view.run_command('_vi_big_e', {'mode': unittest.VISUAL_MODE, 'count': 1})
        self.assertSelection((2, 4))
