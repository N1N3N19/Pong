import pygame
from constant import *

class Paddle:
    def __init__(self, screen, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        #feature property
        self.extra_speed = 0
        self.point = 0
        self.added_size = 0
        self.rect = pygame.Rect(x, y, width, height)
        self.dy = 0

    def update(self, dt):
        if self.dy > 0:
            if self.rect.y + self.rect.height < HEIGHT:
                self.rect.y += self.dy*dt
        else:
            if self.rect.y >= 0:
                self.rect.y += self.dy*dt
    
    def change_size(self, extra_size):
        self.height += extra_size
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)