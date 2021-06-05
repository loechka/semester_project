"""Module contains Bonus class."""

import pygame
from game_object import GameObject
import config as c


class Bonus(GameObject):
    """
    Bonus object class, based on GameObject class.

    There are two types of bonuses: good - star, bad - bomb.
    Every good or bad bonus can have two different effects:
    change amount of lives, change charecter size.
    """

    def __init__(
                self,
                x: int,
                y: int,
                w: int,
                h: int,
                color: tuple,
                speed: int,
                one_type: str = 'default',
                good: bool = True,
                type: int = 0,
                seen: bool = True):
        """
        Init Bonus object with certain features.

        Keyword arguments:
        :param x: left coordinate
        :param y: top coordinate
        :param w: object width
        :param h: object height
        :param color: object color
        :params speed: object speed
        :params one_type: key for generating same bonuses - 'deafult' - use param good, \
            'star' - star, 'bomb' - bomb
        :param good: is bonus good - True - star, False - bomb (default True)
        :param type: bonus type: 0 - +/- lives, 1 - change size (default 0)
        :param seen: is bonus seen (default True)
        """
        GameObject.__init__(self, x, y, w, h, speed)
        self.one_type = one_type
        if self.one_type == 'default':
            self.good = good
        elif self.one_type == 'bomb':
            self.good = False
        else:
            self.good = True
        self.type = type
        self.seen = seen
        self.color = color
        self.load_image(self.good)

    def load_image(self, good: bool):
        """
        Load certain image according to bonus type.

        Keyword arguments:
        :param good: is bonus good: True - star, False - bomb (default True)
        """
        if good:
            self.filepath = c.star_image
        else:
            self.filepath = c.bomb_image
        self.myImage = pygame.image.load(self.filepath).convert_alpha()
        self.myImage = pygame.transform.scale(
                                    self.myImage,
                                    (self.bounds.width, self.bounds.height))

    def draw(self, surface):
        """
        Draw bonus.

        Keyword arguments:
        :param surface: pygame Surface
        """
        if self.seen:
            surface.blit(self.myImage, self.bounds)

    def update(self):
        """Update bonus."""
        super().update()

    def delete(self):
        """Delete bonus.

        Makes it an invisible dot.
        """
        self.seen = False
        self.bounds.height = 0
        self.bounds.width = 0
