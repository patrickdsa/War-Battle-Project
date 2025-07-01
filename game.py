import pygame
from pygame.locals import *
import random
from const import SCREEN_HEIGHT, SCREEN_WIDTH, fps, YELLOW, RED, ROWS, COLS, ENEMY_COOLDOWN, COUNTDOWN, WHITE, \
    GAME_OVER
from enemy import Enemy
from enemy_bullets import EnemyBullets
from groups import tank_group, enemy_group, bullet_group, enemy_bullets_group, explosion_group
from settings import screen
from sounds import death_sound, win_sound, battle_music, music_channel
from tank import Tank



#functions
def draw_background():
    screen.blit(background, (0, 0))

# creating texts

def draw_text (text, font, text_color,x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def create_enemy():
    for row in range(ROWS):
        for item in range(COLS):
            enemy = Enemy(100 + item * 100,  100 + row * 70)
            enemy_group.add(enemy)


pygame.init()
font40 = pygame.font.SysFont('Constantia', 40)
font30 = pygame.font.SysFont('Constantia', 30)


# fps
clock = pygame.time.Clock()
pygame.display.set_caption('War Battle')

# load background
background_load = pygame.image.load('assets/background_imgs/war.png')
background = pygame.transform.scale(background_load, (SCREEN_WIDTH, SCREEN_HEIGHT))

last_enemy_shot = pygame.time.get_ticks()
last_count = pygame.time.get_ticks()
music_played = False


# Main
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
                death_sound.play()
                death_sound.stop()
                draw_text('DEFEAT!', font40, WHITE, int(SCREEN_WIDTH / 2 - 100), int(SCREEN_HEIGHT / 2 + 50))
                draw_text('THE ENEMY FORCES HAS WON!', font30, WHITE, int(SCREEN_WIDTH / 2 - 230), int(SCREEN_HEIGHT / 2 + 100))
            if GAME_OVER == 1:
                win_sound.play()
                win_sound.stop()
                draw_text('YOU WIN SOLDIER!', font40, WHITE, int(SCREEN_WIDTH / 2 - 200), int(SCREEN_HEIGHT / 2 + 50))

    explosion_group.update()

    if COUNTDOWN > 0:
        draw_text('GET READY FOR BATTLE', font40, WHITE, int(SCREEN_WIDTH / 2 - 230), int(SCREEN_HEIGHT / 2 + 50))
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
