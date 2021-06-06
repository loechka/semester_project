"""Module contains TextObject class."""

import pygame


class TextObject:
    """
    TextObject class.

    Create a message on screen.

    :param x: horisontal coordinate
    :param y: vertical coordinate
    :param text_func: message text
    :param color: message text color
    :param font_name:  message text font name
    :param font_size:  message text font size
    :param text_type: text type (default 0)
    """

    def __init__(
                self,
                x: int,
                y: int,
                text_func,
                color: tuple,
                font_name: str,
                font_size: int,
                text_type: int = 0):
        """Init TextObject with certain features."""
        self.pos = (x, y)
        self.text_type = text_type
        if self.text_type == 0:
            self.text_func = text_func
        else:
            self.text_func = text_func()
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        if self.text_type == 0:
            self.bounds = self.get_surface(self.text_func())
        else:
            self.bounds = self.get_surface(self.text_func)

    def draw(self, surface, centralized=False):
        """
        Draw message.

        :param surface: pygame Surface
        :param centralized: is the message centralized (default False)
        """
        if self.text_type == 0:
            text_surface, self.bounds = self.get_surface(self.text_func())
        else:
            text_surface, self.bounds = self.get_surface(self.text_func)
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2, self.pos[1])
        else:
            pos = self.pos
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        """
        Render message.

        :param text: message text
        """
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        """Update TextObject."""
        pass
