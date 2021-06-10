import unittest
from duck import Duck
from wall import Wall
from bonus import Bonus
from button import Button
from image import Image
import config as c
import pygame as pg


class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        pg.init()
        size = width, height, = 0, 0
        screen = pg.display.set_mode(size, pg.HIDDEN)
        self.duck = Duck(0, 0, 0, 0, (255, 255, 255), 5, 0)
        self.wall = Wall(0, 0, 0, 0, (255, 255, 255), [0, 0], 0)
        self.bonus = Bonus(0, 0, 0, 0, 
                            (255, 255, 255), 
                            5, 
                            'default', 
                            True, 0, False)
        self.button = Button(0, 0, 0, 0, '', lambda x: None, 0, (255, 255, 255))

    def test_101_duck_resize(self):
        self.duck.change_size(2, 2)
        self.assertEqual(self.duck.bounds.width, 2, "wrong width after resize")
        self.assertEqual(self.duck.bounds.height, 2, "wrong height after resize")

    def test_102_change_character(self):
        self.duck.character = 0
        self.duck.change_character()

        self.assertEqual(
            self.duck.file_path, c.character_images[0], "wrong file path after changing"
        )

        self.duck.character = 1
        self.duck.change_character()

        self.assertEqual(
            self.duck.file_path, c.character_images[1], "wrong file path after changing"
        )

        self.duck.character = 2
        self.duck.change_character()

        self.assertEqual(
            self.duck.file_path, c.character_images[2], "wrong file path after changing"
        )

    def test_103_duck_delete(self):
        self.duck.delete()

        self.assertEqual(self.duck.seen, False, "wrong seen state")
        self.assertEqual(self.duck.bounds.height, 0, "wrong height after delete")
        self.assertEqual(self.duck.bounds.width, 0, "wrong width after delete")

    def test_201_wall_delete(self):
        self.wall.delete()

        self.assertEqual(self.wall.seen, False, "wrong seen state")
        self.assertEqual(self.wall.bounds.height, 0, "wrong height after delete")
        self.assertEqual(self.wall.bounds.width, 0, "wrong width after delete")

    def test_301_bonus_load_image(self):
        self.bonus.load_image(True)
        self.assertEqual(
            self.bonus.filepath, c.star_image, "wrong file path after changing"
        )

        self.bonus.load_image(False)
        self.assertEqual(
            self.bonus.filepath, c.bomb_image, "wrong file path after changing"
        )

    def test_302_bonus_delete(self):
        self.wall.delete()

        self.assertEqual(self.bonus.seen, False, "wrong seen state after delete")
        self.assertEqual(self.bonus.bounds.height, 0, "wrong height after delete")
        self.assertEqual(self.bonus.bounds.width, 0, "wrong width after delete")

    def test_401_button_delete(self):
        self.button.delete()

        self.assertEqual(self.button.bounds.height, 0, "wrong height after delete")
        self.assertEqual(self.button.bounds.width, 0, "wrong width after delete")
    
    def tearDown(self):
        pg.quit()