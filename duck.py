import pygame

import config as c
from game_object import GameObject


class Duck(GameObject):
    def __init__(self, x, y, w, h, color, offset, character):
        GameObject.__init__(self, x, y, w, h)
        self.color = color
        self.offset = offset
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.coordinates = (x,y)

        file_path = c.character_images[character]
        self.myImage = pygame.image.load(file_path)
        self.myImage = pygame.transform.scale(self.myImage, (w, h))

    def draw(self, surface):
        # pygame.draw.rect(surface, self.color, self.bounds)
        surface.blit(self.myImage, self.bounds)

    def handle(self, key):
        if key == pygame.K_LEFT:
            self.moving_left = not self.moving_left
        elif key == pygame.K_RIGHT:
            self.moving_right = not self.moving_right
        elif key == pygame.K_UP:
            self.moving_up = not self.moving_up
        elif key == pygame.K_DOWN:
            self.moving_down = not self.moving_down
    
    def change_size(self, new_width, new_height):
        center = self.bounds.center
        self.bounds.width = new_width
        self.bounds.height = new_height
        self.bounds.center = center

    def update(self):
        dx, dy = 0, 0
        if self.moving_left:
            dx = -(min(self.offset, self.left))
            self.change_size(c.duck_width_large, c.duck_height_large)
        elif self.moving_right:
            dx = min(self.offset, c.screen_width - self.right)
            self.change_size(c.duck_width_small, c.duck_height_small)
        elif self.moving_down:
            dy = min(self.offset, c.screen_height - self.bottom)
        elif self.moving_up:
            dy = -(min(self.offset, self.top))
        else:
            return

        self.move(dx, dy)
