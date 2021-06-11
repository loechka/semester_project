"""Module contains Game class."""

import pygame as pg
from collections import defaultdict
import sys

class Game:
    """
    Base Game class.

    Responsible for game window creation, handling events and game time.

    :param caption: window name
    :param width: window width
    :param height: window height
    :param back_image_file: path to back image
    :param frame_rate: frame rate
    """

    def __init__(self,
                 caption: str,
                 width: int,
                 height: int,
                 back_image_file: str,
                 frame_rate: int):
        """Init Game with certain features."""
        self.frame_rate = frame_rate
        self.game_over = False
        self.objects = []
        # pg.mixer.pre_init(44100, 16, 2, 4096)
        pg.mixer.pre_init(44100, -16, 2, 512)
        pg.init()
        pg.font.init()
        self.surface = pg.display.set_mode(
                                            (width, height),
                                            flags=pg.DOUBLEBUF)
        pg.display.set_caption(caption)
        self.surface.set_alpha(None)
        self.background_image = pg.image.load(back_image_file).convert_alpha()
        self.background_image.set_colorkey((0, 0, 0))
        self.background_image = pg.transform.scale(
                                        self.background_image,
                                        (width, height))
        self.clock = pg.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []
        pg.event.wait()
        pg.event.set_allowed = [[
                                pg.QUIT,
                                pg.KEYDOWN,
                                pg.KEYUP,
                                pg.MOUSEBUTTONDOWN,
                                pg.MOUSEBUTTONUP,
                                pg.MOUSEMOTION]]

    def update(self):
        """Update game objects."""
        for o in self.objects:
            o.update()

    def draw(self):
        """Draw game object."""
        for o in self.objects:
            o.draw(self.surface)

    def handle_events(self):
        """Handle keyboard and mouse events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pg.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pg.MOUSEBUTTONDOWN,
                                pg.MOUSEBUTTONUP,
                                pg.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def run(self):
        """Handle game running."""
        while not self.game_over:
            self.surface.blit(self.background_image, (0, 0))
            # self.surface.fill((0, 0, 0))

            self.handle_events()
            self.update()
            self.draw()

            pg.display.update()
            self.clock.tick(self.frame_rate)
