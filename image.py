"""Module contains Image class."""

import pygame
from game_object import GameObject

class Image(GameObject):
    """
    Image class, based on GameObject class.

    :param x: left coordinate
    :param y: top coordinate
    :param w: object width
    :param h: object height
    :param file_path: path to image
    :param seen: is object seen (default True)
    """

    def __init__(self,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 file_path: str,
                 seen: bool = True):
        """Init Image object with certain features."""        
        super().__init__(x, y, w, h)
        self.seen = seen
        self.myImage = pygame.image.load(file_path)
        self.myImage = pygame.transform.scale(self.myImage, (w, h))
        # self.rect = self.myImage.get_rect()
        self.coordinates = (x, y)

    def draw(self, surface):
        """
        Draw Image object.

        :param surface: pygame Surface
        """
        # pygame.draw.rect(surface, (255,0,128), self.rect, 1)
        # pygame.display.update()
        if self.seen:
            surface.blit(self.myImage, self.coordinates)

    def delete(self):
        """Delete Image from screen.

        Makes it an invisible dot.
        """
        self.seen = False
        self.coordinates = (0, 0)
