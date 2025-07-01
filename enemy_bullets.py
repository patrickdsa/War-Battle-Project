import pygame
import tank
from tank import Tank
from settings import screen
from explosion import Explosion
from const import SCREEN_HEIGHT
from sounds import enemy_shot
from groups import tank_group, explosion_group


class EnemyBullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/bullets/EnemyBullet.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        hits = pygame.sprite.spritecollide(self, tank_group, False, pygame.sprite.collide_mask)
        if hits:
            self.kill()
            enemy_shot.play()
            for tank_sprite in hits:
                tank_sprite.hp_remaining -= 1
                explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
                explosion_group.add(explosion)