import pygame
WIDTH = 1280
HEIGHT = 720

PADDLE_SPEED = 800

#Game state
MENU = 'menu'
PREPARE = 'prepare'
START = 'start'
SERVE = 'serve'
UPGRADE = 'upgrade'
EXIT = 'exit'
BACK = 'back'
#GAME_MODE
PLAYER_VS_BOT = 'bot'
PLAYER_VS_PLAYER = 'player'


#Key Press
W = pygame.K_w
S = pygame.K_s
KEYUP = pygame.K_UP
KEYDOWN = pygame.K_DOWN
ENTER = pygame.K_RETURN
#Bot difficulty
BOT_LEVEL = 0
ENEMY_TOUCH = False
WINNING_SCORE = 2
MAX_FRAME_RATE = 60
