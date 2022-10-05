import pygame as pg
from settings import *

class Map:
    def __init__(self, filename):
        self.Data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.Data.append(line.strip())
        self.tilewidth = len(self.Data[0])
        self.tileheight = len(self.Data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width * TILESIZE
        self.height = height * TILESIZE


    def apply(self, entity):
        #On dessine tout sur l'écran décallé de ça
        return entity.rect.move(self.camera.topleft)
    def update(self, target):

         #Calcule un décallage de combien on se déplace
        x = -target.rect.centerx + int(WIDTH / 2) #entier
        y = -target.rect.centery + int(HEIGHT / 2)


        #Limitation du scrolling de la Map
        x = min(0, x) #Gauche
        y = min(0, y) #Haut
        x = max(-(self.width - WIDTH), x)#Droite
        y = max(-(self.height - HEIGHT), y)#bas

        self.camera = pg.Rect(x, y, self.width, self.height)
