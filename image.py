import pygame

from game_object import GameObject


class Image(GameObject):
    def __init__(self,
                 x,
                 y,
                 w,
                 h,
                 file_path,
                 seen = True):
        super().__init__(x, y, w, h)
        self.seen = seen
        self.myImage = pygame.image.load(file_path)
        self.myImage = pygame.transform.scale(self.myImage, (w, h))
        # self.rect = self.myImage.get_rect()
        self.coordinates = (x, y)

    def draw(self, surface):
        # pygame.draw.rect(surface, (255,0,128), self.rect, 1)
        # pygame.display.update()
        if self.seen:
            surface.blit(self.myImage, self.coordinates)
    
    def delete(self):
        self.seen = False
        self.coordinates = (0, 0)
