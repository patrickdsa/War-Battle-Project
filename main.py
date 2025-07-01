import pygame
from pygame import mixer
from pygame.locals import *
import random
from const import SCREEN_HEIGHT, SCREEN_WIDTH, fps, YELLOW, RED, ROWS, COLS, ENEMY_COOLDOWN, COUNTDOWN, WHITE, GAME_OVER

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

explosion1_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')
explosion1_sound.set_volume(0.25)

#explosion2_sound = pygame.mixer.Sound('sounds/explosion2.wav')
#explosion1_sound.set_volume(0.25)

tankshot = pygame.mixer.Sound('assets/sounds/tankshot.wav')
tankshot.set_volume(0.25)

enemy_shot = pygame.mixer.Sound('assets/sounds/enemyshot.wav')
enemy_shot.set_volume(0.25)

font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

# fps
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('War Battle')

# load background
background_load = pygame.image.load('assets/background_imgs/War.png')
background = pygame.transform.scale(background_load, (SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_background():
    screen.blit(background, (0, 0))

# creating texts

def draw_text (text, font, text_color,x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))



# create class

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, hp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/tank/tank.png')
        self.image = pygame.transform.scale(self.image, (190, 190)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.hp_start = hp
        self.hp_remaining = hp
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        speed = 8
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



class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/bullets/TankBullet.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, enemy_group, True):
            self.kill()
            explosion1_sound.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


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

class EnemyBullets (pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('assets/bullets/EnemyBullet.png')
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):
            self.rect.y += 2
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()
            if pygame.sprite.spritecollide(self, tank_group, False, pygame.sprite.collide_mask):
                self.kill()
                enemy_shot.play()
                tank.hp_remaining -= 1
                explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
                explosion_group.add(explosion)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,10):
            img = pygame.image.load(f'assets/explosion/sprite_0{num}.png')
            if size == 1:
                img = pygame.transform.scale(img, (10, 10))
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 1:
                img = pygame.transform.scale(img, (60, 60))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len (self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #delete explosion

        if self.index >= len (self.images) - 1 and self.counter >= explosion_speed:
            self.kill()



last_enemy_shot = pygame.time.get_ticks()
last_count = pygame.time.get_ticks()

# sprite groups
tank_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_bullets_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

def create_enemy():
    for row in range(ROWS):
        for item in range(COLS):
            enemy = Enemy(100 + item * 100,  100 + row * 70)
            enemy_group.add(enemy)

create_enemy()
tank = Tank(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT - 100), 3)
tank_group.add(tank)

while True:

    clock.tick(fps)

    # background
    draw_background()

    if COUNTDOWN == 0:

        #create alien shoots
        time_now = pygame.time.get_ticks()
        if time_now - last_enemy_shot > ENEMY_COOLDOWN and len(enemy_bullets_group) < 5 and len(enemy_group) > 0:
            enemy_attack = random.choice(enemy_group.sprites())
            enemy_bullet = EnemyBullets(enemy_attack.rect.centerx, enemy_attack.rect.bottom)
            enemy_bullets_group.add(enemy_bullet)
            last_enemy_shot = time_now

        if len (enemy_group) == 0:
            GAME_OVER = 1

        if GAME_OVER == 0:
            # update groups
            GAME_OVER = tank.update()
            bullet_group.update()
            enemy_group.update()
            enemy_bullets_group.update()
        else:
            if GAME_OVER == -1:
                draw_text('GAME OVER!', font40, WHITE, int(SCREEN_WIDTH / 2 - 100), int(SCREEN_HEIGHT / 2 + 50))
            if GAME_OVER == 1:
                draw_text('YOU WIN!', font40, WHITE, int(SCREEN_WIDTH / 2 - 100), int(SCREEN_HEIGHT / 2 + 50))

    explosion_group.update()

    if COUNTDOWN > 0:
        draw_text('GET READY FOR BATTLE', font40, WHITE, int(SCREEN_WIDTH / 2 - 110), int(SCREEN_HEIGHT / 2 + 50))
        draw_text(str(COUNTDOWN), font40, WHITE, int(SCREEN_WIDTH / 2 - 10), int(SCREEN_HEIGHT / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            COUNTDOWN -= 1
            last_count = count_timer

    # draw sprite groups
    tank_group.draw(screen)
    bullet_group.draw(screen)
    enemy_group.draw(screen)
    enemy_bullets_group.draw(screen)
    explosion_group.draw(screen)

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()
