import pygame as pg
from settings import *
vec = pg.math.Vector2
#Copie un vecteur

class Variables:
    pass

#Classe des joueurs et murs
class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.powerup = 0
        self.i = 0
        self.k = 0
        self.Attack = False
        self.Dir = None
        self.plist = []
        self.image = self.game.PlayerAnimateDownIdle[self.i]
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.size = self.rect.size
        self.pos = vec(x, y) * TILESIZE
        self.rot = -90
        self.rots = -90
        self.last_shot = 0
        self.Move = False
        self.attack = 0
        self.health = PLAYERLIFE

    def get_key(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -Player_speed
            self.rot = 90
            self.rots = 90
            self.Dir = 'Up'
            self.Move = True
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = Player_speed
            self.rot = 270
            self.rots = 270
            self.Dir = 'Down'
            self.Move = True
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -Player_speed
            self.rot = 180
            self.rots = 180
            self.Dir = 'Left'
            self.Move = True
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = Player_speed
            self.rot = 360
            self.rots = 360
            self.Dir = 'Right'
            self.Move = True
        if keys[pg.K_x] and self.powerup >= 100:
                dir = vec(1, 0).rotate(-360)
                sword(self.game, self.pos, dir)
                dir = vec(1, 0).rotate(-180)
                sword(self.game, self.pos, dir)
                dir = vec(1, 0).rotate(-90)
                sword(self.game, self.pos, dir)
                dir = vec(1, 0).rotate(-270)
                sword(self.game, self.pos, dir)
                dir = vec(1, 0).rotate(-45)
                sword(self.game, self.pos, dir)
                dir = vec(1, 0).rotate(-135)
                sword(self.game, self.pos, dir)
                dir = vec(1, 0).rotate(-225)
                sword(self.game, self.pos, dir)
                dir = vec(1, 0).rotate(-315)
                sword(self.game, self.pos, dir)
                self.powerup = 0
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if not self.attack:
                if self.rots%360 == 0:
                    # 4 premiers bits de self.attack
                    # a droite
                    self.attack = 2**0
                if self.rots%360 == 90:
                    # 4 suivants.. etc
                    # En haut
                    self.attack = 2**5
                if self.rots%360 == 180:
                    # a gauche
                    self.attack = 2**10
                if self.rots%360 == 270:
                    # En bas
                    self.attack = 2**15

                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rots)
                sword(self.game, self.pos, dir)
                if self.powerup < 100:
                    self.powerup += 5
                if self.powerup >= 100:
                    self.powerup = 100
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071 #évite une accélération permanente

    def GetIndex(self):
        p1 = [self.pos[0] // TILESIZE, self.pos[1] // TILESIZE]
        p2 = [(self.pos[0] + self.size[0]) // TILESIZE, self.pos[1] // TILESIZE]
        p3 = [self.pos[0] // TILESIZE, (self.pos[1] + self.size[1]) // TILESIZE]
        p4 = [(self.pos[0] + self.size[0]) // TILESIZE, (self.pos[1] + self.size[1]) // TILESIZE]
        self.plist = [p1, p2, p3, p4]
        self.plist = [[int(x), int(y)] for x, y in self.plist]
        return self.plist

    def update(self):
        self.Move = False
        self.get_key()
        self.k += 1
        if self.k >= 7:
            self.k = 0
            self.i += 1
        if self.i >= 4:
            self.i = 0
        if self.Move == False:
            if self.Dir == 'Up' or self.Dir == 'Down':
                self.image = self.game.PlayerAnimateDownIdle[self.i]
            if self.Dir == 'Right':
                self.image = self.game.player_Move_RightIdle
            if self.Dir == 'Left':
                self.image = self.game.player_Move_LeftIdle
        if self.Move == True:
            #pg.mixer.music.load(path.join(img_folder + '\Audio', "footstep05.ogg"))
            if self.Dir == 'Right':
                self.image = self.game.playerAnimateRight[self.i]
            if self.Dir == 'Left':
                self.image = self.game.playerAnimateLeft[self.i]
            if self.Dir == 'Up':
                self.image = self.game.playerAnimateUp[self.i]
            if self.Dir == 'Down':
                self.image = self.game.playerAnimateDown[self.i]



        r = self.attack
        if self.attack:
            for i, sprites in enumerate(Variables.PlayerAttackAnimation):
                if r < 32:
                    break
                r /= 32
                r = int(r)
            else:
                raise Exception("How the hell did this happen...")

            r+=1
            if r > 30:
                self.attack = 0
            else:
                self.attack = r << (i * 5) # a >> b == a * 2**b
            t = 0 if r%30 < 8 else 1
            self.image = sprites[t]
        self.pos += self.vel * self.game.dt
        indices = self.GetIndex()
        if self.vel.x < 0:
            if Variables.GlobalWallBool[indices[0][1]][indices[0][0]] or Variables.GlobalWallBool[indices[2][1]][indices[2][0]]:
                self.pos.x -= self.vel.x * self.game.dt
                self.vel.x = 0
        else:
            if Variables.GlobalWallBool[indices[1][1]][indices[1][0]] or Variables.GlobalWallBool[indices[3][1]][indices[3][0]]:
                self.pos.x -= self.vel.x * self.game.dt
                self.vel.x = 0
        if self.vel.y < 0:
            if Variables.GlobalWallBool[indices[0][1]][indices[0][0]] or Variables.GlobalWallBool[indices[1][1]][indices[1][0]]:
                self.pos.y -= self.vel.y * self.game.dt
                self.vel.y = 0
        else:
            if Variables.GlobalWallBool[indices[2][1]][indices[2][0]] or Variables.GlobalWallBool[indices[3][1]][indices[3][0]]:
                self.pos.y -= self.vel.y * self.game.dt
                self.vel.y = 0
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        # [[x0, y0], [x1, y1], [x2, y2], [x3, y3]]
        # 0  1
        # 2  3
        #Pour tirer là où y a la souris
    def shootingMouse(self):
        #position souris
        pos = pg.mouse.get_pos()
        #Vérifie Où se trouve la souris par rapport au joueur
        if self.pos.x >= pos.x : #Ici on fera un vecteur joueur - souris
            #Jsuis à gauche
            pass
        if self.pos.x <= pos.x: #Idem
            #Jsuis à Droite
            pass
        if self.pos.y >= pos.y: #Idem
            #Jsuis en haut
            pass
        if self.pos.y <= pos.y: #Idem
            #Jsuis en bas
            pass
        pass
#Classe de l'arme / projectile
class sword(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        # self.damage = dmg
        self.groups = game.all_sprites, game.swords
        self.game = game
        pg.sprite.Sprite.__init__(self,self.groups)
        self.image = game.sword_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = self.pos
        self.vel = dir*SWORD_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > SWORD_LIFE:
            self.kill()

#classe des monstres et ennemies
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.size = self.rect.size
        self.plist = []
        self.roty = 0
        self.rotx = 0
        self.health = MOBLIFE
#Obtient la position sur le grillage
    def GetIndex(self):
        p1 = [self.pos[0] // TILESIZE, self.pos[1] // TILESIZE]
        p2 = [(self.pos[0] + self.size[0]) // TILESIZE, self.pos[1] // TILESIZE]
        p3 = [self.pos[0] // TILESIZE, (self.pos[1] + self.size[1]) // TILESIZE]
        p4 = [(self.pos[0] + self.size[0]) // TILESIZE, (self.pos[1] + self.size[1]) // TILESIZE]
        self.plist = [p1, p2, p3, p4]
        self.plist = [[int(x), int(y)] for x, y in self.plist]
        return self.plist

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        #Equation de mouvement
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        #Test de collisions
        indicies = self.GetIndex()
        if self.vel.x > 0 :
            if Variables.GlobalWallBool[indicies[1][1]][indicies[1][0]] or Variables.GlobalWallBool[indicies[3][1]][indicies[3][0]]:
                self.pos.x -= self.vel.x * self.game.dt + 0.5 * self.acc.x * self.game.dt ** 2
                self.vel.x = 0
        else:
            if Variables.GlobalWallBool[indicies[0][1]][indicies[0][0]] or Variables.GlobalWallBool[indicies[2][1]][indicies[2][0]]:
                self.pos.x -= self.vel.x * self.game.dt + 0.5 * self.acc.x * self.game.dt ** 2
                self.vel.x = 0
        if self.vel.y > 0 :
            if Variables.GlobalWallBool[indicies[2][1]][indicies[2][0]] or Variables.GlobalWallBool[indicies[3][1]][indicies[3][0]]:
                self.pos.y -= self.vel.y * self.game.dt + 0.5 * self.acc.y * self.game.dt ** 2
                self.vel.y = 0
        else:
            if Variables.GlobalWallBool[indicies[0][1]][indicies[0][0]] or Variables.GlobalWallBool[indicies[1][1]][indicies[1][0]]:
                self.pos.y -= self.vel.y * self.game.dt + 0.5 * self.acc.y * self.game.dt ** 2
                self.vel.y = 0
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.health <= 0:
            self.kill()
    def healthBar(self):
            if self.health > 60:
                col = GREEN
            elif self.health > 30:
                col = YELLOW
            else:
                col = RED
            width = int(self.rect.width * self.health / MOBLIFE)
            self.health_bar = pg.Rect(0, 0, width, 7)
            if self.health < MOBLIFE:
                pg.draw.rect(self.image, col, self.health_bar)

#Classe des "murs" les zones infranchissables
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #Créer une surface carrée de la taille des carreaux
        self.image = game.wall_img
        #Obtient le rectangle
        self.rect = self.image.get_rect()
        self.x = x
        self.size = self.rect.size
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.pos = self.rect
        self.plist = []

#Classe du selecteur dans le menu
class Mouse(pg.sprite.Sprite):
    def __init__(self):
        self.pos = vec(0, 0)
        self.image = pg.image.load()
        pass
    def getKey(self):
        pass
    def update(self):
        pass
