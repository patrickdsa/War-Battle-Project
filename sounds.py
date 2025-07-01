import pygame
from pygame import mixer



pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')
explosion_sound.set_volume(0.25)

battle_music = pygame.mixer.Sound('assets/sounds/battle_music.wav')
battle_music.set_volume(0.05)

death_sound = pygame.mixer.Sound('assets/sounds/death_sound.wav')
death_sound.set_volume(0.25)

tankshot = pygame.mixer.Sound('assets/sounds/tankshot.wav')
tankshot.set_volume(0.25)

win_sound = pygame.mixer.Sound('assets/sounds/win_sound.wav')
win_sound.set_volume(0.20)

enemy_shot = pygame.mixer.Sound('assets/sounds/enemyshot.wav')
enemy_shot.set_volume(0.25)
