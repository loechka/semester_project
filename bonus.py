import pygame

from game_object import GameObject
import config as c


class Bonus(GameObject):
    def __init__(self, x, y, w, h, color, speed, good=True, type=0, seen=True):
        GameObject.__init__(self, x, y, w, h, speed)
        self.good = good
        self.type = type
        self.seen = seen
        self.color = color
        self.load_image(self.good)

    def load_image(self, good):
        if good:
            self.filepath = c.star_image
        else:
            self.filepath = c.bomb_image
        self.myImage = pygame.image.load(self.filepath)
        self.myImage = pygame.transform.scale(
                                    self.myImage,
                                    (self.bounds.width, self.bounds.height))

    def draw(self, surface):
        if self.seen:
            surface.blit(self.myImage, self.bounds)

    def update(self):
        super().update()

    def delete(self):
        self.seen = False
        self.bounds.height = 0
        self.bounds.width = 0
