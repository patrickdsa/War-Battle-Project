import pygame
from settings import screen

from bullets import Bullets
from const import SCREEN_WIDTH, RED, YELLOW
from explosion import Explosion
from sounds import tankshot
from groups import bullet_group, explosion_group


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, hp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/tank/tank.png')
        self.image = pygame.transform.scale(self.image, (160, 160)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.hp_start = hp
        self.hp_remaining = hp
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        speed = 6.5
        cooldown = 500
        GAME_OVER = 0
        # Keys events
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += speed

        time_now = pygame.time.get_ticks()

        # Tank shoot
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            tankshot.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        # improving pixel colision
        self.mask = pygame.mask.from_surface(self.image)

        # hp bar
        pygame.draw.rect(screen, RED, (self.rect.x, (self.rect.bottom - 25), self.rect.width, 15))
        if self.hp_remaining > 0:
            pygame.draw.rect(screen, YELLOW, (self.rect.x, (self.rect.bottom - 25),
                                              int(self.rect.width * (self.hp_remaining / self.hp_start)), 15))
        elif self.hp_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add (explosion)
            self.kill()
            GAME_OVER = -1
        return GAME_OVER