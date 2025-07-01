import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/enemy/enemy' + str(random.randint(1,2)) + ".png")
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move = 1

    def update(self):
        self.rect.x += self.move
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move *= -1
            self.move_counter *= self.move