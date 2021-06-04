"""Module contains Game class."""

import pygame
from collections import defaultdict
import sys


class Game:
    """
    Base Game class.

    Responsible for game window creation, handling events and game time.
    """

    def __init__(self,
                 caption: str,
                 width: int,
                 height: int,
                 back_image_filename: str,
                 frame_rate: int):
        """
        Init Game with certain features.

        Keyword arguments:
        :param caption: window name
        :param width: window width
        :param height: window height
        :param back_image_filename: path to back image
        :params frame_rate: frame rate
        """
        
        self.frame_rate = frame_rate
        self.game_over = False
        self.objects = []
        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height), flags = pygame.DOUBLEBUF)
        pygame.display.set_caption(caption)
        self.surface.set_alpha(None)
        self.background_image = pygame.image.load(back_image_filename).convert_alpha()
        self.background_image = pygame.transform.scale(
                                        self.background_image,
                                        (width, height))
        self.clock = pygame.time.Clock()
        #self.clock.tick(60)
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []
        pygame.event.wait()
        pygame.event.set_allowed = [[
                                    pygame.QUIT, 
                                    pygame.KEYDOWN,
                                    pygame.KEYUP,
                                    pygame.MOUSEBUTTONDOWN,
                                    pygame.MOUSEBUTTONUP,
                                    pygame.MOUSEMOTION]]

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
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

            pygame.display.update()
            self.clock.tick(self.frame_rate)
