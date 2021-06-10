"""Module contains Wall class."""

import pygame
from game_object import GameObject
import config as c


class Wall(GameObject):
    """
    Wall object class, based on GameObject class.

    Every class object is a moving left rectangle.

    :param x: left coordinate
    :param y: top coordinate
    :param w: object width
    :param h: object height
    :param color: object color
    :param speed: object speed
    :param seen: is object seen (default True)
    """

    def __init__(
                self,
                x: int,
                y: int,
                w: int,
                h: int,
                color: tuple,
                speed: int,
                seen: bool = True):
        """Init Wall object with certain features."""
        GameObject.__init__(self, x, y, w, h, speed)
        self.seen = seen
        self.color = color
        file_path = c.wall_image
        self.myImage = pygame.image.load(file_path).convert_alpha()
        self.myImage = pygame.transform.scale(self.myImage, (w, h))

    def draw(self, surface):
        """
        Draw wall.

        :param surface: pygame Surface
        """
        if self.seen:
            surface.blit(self.myImage, self.bounds)

    def update(self):
        """Update wall."""
        super().update()

    def delete(self):
        """Delete wall.

        Makes it an invisible dot.
        """
        self.seen = False
        self.bounds.height = 0
        self.bounds.width = 0
