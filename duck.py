"""Module contains Duck class."""

import pygame
import config as c
from game_object import GameObject


class Duck(GameObject):
    """
    Duck object class, based on GameObject class.

    Every Duck object is a rectangle moving by arrow keys.

    :param x: left coordinate
    :param y: top coordinate
    :param w: object width
    :param h: object height
    :param offset: object offset from the window border
    :param character: character - 0: square, 1: duck (default), 2: horse
    :param seen: is character seen (default True)
    """

    def __init__(
                self,
                x: int,
                y: int,
                w: int,
                h: int,
                color: tuple,
                offset: int,
                character: int,
                seen: bool = True):
        """Init Duck object with certain features."""
        GameObject.__init__(self, x, y, w, h)
        self.seen = seen
        self.color = color
        self.offset = offset
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.coordinates = (x, y)
        self.character = character
        self.file_path = c.character_images[self.character]
        self.myImage = pygame.image.load(self.file_path).convert_alpha()
        self.myImage = pygame.transform.scale(self.myImage, (w, h))

    def draw(self, surface):
        """
        Draw duck.

        :param surface: pygame Surface
        """
        if self.seen:
            surface.blit(self.myImage, self.bounds)

    def handle(self, key):
        """
        Handle keyboard events.

        :param key: key pressed
        """
        if key == pygame.K_LEFT:
            self.moving_left = not self.moving_left
            self.myImage = pygame.transform.flip(self.myImage, True, False)

        elif key == pygame.K_RIGHT:
            self.moving_right = not self.moving_right
        elif key == pygame.K_UP:
            self.moving_up = not self.moving_up
        elif key == pygame.K_DOWN:
            self.moving_down = not self.moving_down

    def change_size(self,
                    new_width: int,
                    new_height: int):
        """
        Change character size.

        :param new_width: new width
        :param new_height: new height
        """
        center = self.bounds.center
        self.bounds.width = new_width
        self.bounds.height = new_height
        self.bounds.center = center
        self.myImage = pygame.image.load(self.file_path)
        self.myImage = pygame.transform.scale(self.myImage, (new_width, new_height))

    def change_character(self):
        """Change character image according to self.character."""
        file_path = c.character_images[self.character]
        self.myImage = pygame.image.load(file_path)

    def update(self):
        """Update wall position."""
        self.myImage = pygame.transform.scale(
                                self.myImage,
                                (self.bounds.width, self.bounds.height))
        dx, dy = 0, 0
        if self.moving_left:
            dx = -(min(self.offset, self.left))
        elif self.moving_right:
            dx = min(self.offset, c.screen_width - self.right)
        elif self.moving_down:
            dy = min(self.offset, c.screen_height - self.bottom)
        elif self.moving_up:
            dy = -(min(self.offset, self.top))
        else:
            return

        self.move(dx, dy)

    def delete(self):
        """Delete duck.

        Makes it an invisible dot.
        """
        self.seen = False
        self.bounds.height = 0
        self.bounds.width = 0
