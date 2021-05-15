import pygame

from game_object import GameObject


class Wall(GameObject):
    def __init__(self, x, y, w, h, color, speed):
        GameObject.__init__(self, x, y, w, h, speed)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

    def update(self):
        super().update()
