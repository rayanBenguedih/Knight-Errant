import pygame as pg
pg.init()
# Quelque couleurs (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
TEAL = (0, 255, 255)

#Settings du joueurs
Player_speed = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'knight iso char_run right_0.png'
PlayerSize = 64
PLAYERLIFE = 100
Recover = 1000
POWERUPBAR = 100

#Settings écrans
screenX = pg.display.Info().current_w
screenY = pg.display.Info().current_h
# Settings du jeu
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Knight Errant"
BGCOLOR = BROWN

WALL_IMG = 'tileGreen_39.png'

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#Settings des monstres
MOB_IMG = 'zombie1_hold.png'
MOB_HIT_RECT = pg.Rect(0, 0, 40, 40)
MOB_SPEED = 150
MOBLIFE = 100
MOBDMG = 10
#Setting de l'arme
SWORD_IMG = 'Sword.png'
SWORD_SPEED = 500
SWORD_LIFE = 3000
SWORD_RATE = 250
SWORDDMG = 25
#Settings des divers images d'écran de jeu
SCREENIMG1 = 'screenimg1.jpg'
SCREENIMG2 = 'screenimg2.jpg'
SCREENIMG3 = 'screenimg3.jpg'
