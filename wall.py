import pygame

from game_object import GameObject
import config as c


class Wall(GameObject):
    def __init__(self, x, y, w, h, color, speed, seen = True):
        GameObject.__init__(self, x, y, w, h, speed)
        self.seen = seen
        self.color = color
        file_path = c.wall_image
        self.myImage = pygame.image.load(file_path)
        self.myImage = pygame.transform.scale(self.myImage, (w, h))

    def draw(self, surface):
        #pygame.draw.rect(surface, self.color, self.bounds)
        if self.seen:
            surface.blit(self.myImage, self.bounds)


    def update(self):
        super().update()

    def delete(self):
        self.seen = False
        self.bounds.height = 0
        self.bounds.width = 0
