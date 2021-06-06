"""Module contains Duck class."""

import pygame
from game_object import GameObject
from text_object import TextObject
import config as c


class Button(GameObject):
    """
    Button object class, based on GameObject class.

    Every Button object is a rectangle that can handle mouse events.

    :param x: left coordinate
    :param y: top coordinate
    :param w: object width
    :param h: object height
    :param text: text on the button
    :param on_click: mouse click event
    :param padding: text padding
    """

    def __init__(self,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 text: str,
                 on_click=lambda x: None,
                 padding: int = 0):
        """Init Button object with certain features."""
        super().__init__(x, y, w, h)
        self.state = 'normal'
        self.on_click = on_click

        self.text = TextObject(x + padding,
                               y + padding, lambda: text,
                               c.button_text_color,
                               c.font_name,
                               c.font_size)

    @property
    def back_color(self):
        """Set button color."""
        return dict(normal=c.button_normal_back_color,
                    hover=c.button_hover_back_color,
                    pressed=c.button_pressed_back_color)[self.state]

    def draw(self, surface):
        """
        Draw buttton with text.

        :param surface: pygame Surface
        """
        pygame.draw.rect(surface,
                         self.back_color,
                         self.bounds, border_radius=3)
        self.text.draw(surface)

    def handle_mouse_event(self, type, pos: int):
        """
        Handle mouse events.

        :param type: type of mouse event
        :param pos: mouse position
        """
        if type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos: int):
        """
        Handle mouse movement.

        :param pos: mouse position
        """
        if self.bounds.collidepoint(pos):
            if self.state != 'pressed':
                self.state = 'hover'
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos: int):
        """
        Handle pressed mouse button.

        :param pos: mouse position
        """
        if self.bounds.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        """
        Handle released mouse button.

        :param pos: mouse position
        """
        if self.state == 'pressed':
            self.on_click(self)
            self.state = 'hover'
