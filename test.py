import unittest
from duck import Duck
import config as c

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.duck = Duck(0, 0, 0, 0, (255, 255, 255), 5, 0)         

    def test_duck_resize(self):
        self.duck.change_size()
        self.assertEqual(self.duck.bounds.width, c.duck_width,
                         'wrong width after resize')
        self.assertEqual(self.duck.bounds.height, c.duck_height,
                         'wrong height after resize')

        self.duck.change_size('small')
        self.assertEqual(self.duck.bounds.width, c.duck_width_small,
                         'wrong width after resize')
        self.assertEqual(self.duck.bounds.height, c.duck_height_small,
                         'wrong height after resize')

        self.duck.change_size('large')
        self.assertEqual(self.duck.bounds.width, c.duck_width_large,
                         'wrong width after resize')
        self.assertEqual(self.duck.bounds.height, c.duck_height_large,
                         'wrong height after resize')