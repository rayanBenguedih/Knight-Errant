#Knight Errant

import pygame as pg
import sys
from os import path
from Sprites import *
from settings import *
from tilemap import *
from niveau_aleatoire import *

#from niveau_aleatoire import *

def startGame(Menu):
    while not Menu:
        g.new()
        g.run()

#HUD fonctions, le menu
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGHT = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGHT
    outline_rect = pg.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
def draw_player_powerup(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGHT = 100
    BAR_HEIGHT = 20
    fill = pct*BAR_LENGHT
    outline_rect = pg.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, YELLOW, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Button:
    def __init__(self, game, pos, dim, col, txt):
        self.txt = txt
        pg.font.init()
        self.myFont = pg.font.SysFont("Starcraft", 30)
        self.label = self.myFont.render(self.txt, 1, WHITE)
        self.pos = list(pos)
        self.dim = dim
        self.col = col
        self.game = game
        self.Button = pg.Rect(self.pos, self.dim)
    def draw(self):
        pg.draw.rect(self.game.screen, self.col, self.Button)
        self.pos[0] = self.pos[0] + self.dim[0] // 2
        self.pos[1] = self.pos[1] + self.dim[1] // 2
        self.game.screen.blit(self.label, (self.pos))
    def click(self):
        pos = pg.mouse.get_pos()
        if pos[0] <= self.pos[0] + self.dim[0] and pos[0] >= self.pos[0] and pos[1] <= self.pos[1] + self.dim[1] and pos[1] >= self.pos[1]:
            menu = False
            startGame(menu)

class Game:
    def __init__(self):
        self.NotMenu = True
        pg.init()
        self.incrementMenu = 0
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.hitTime = pg.time.get_ticks()
        self.load_data()

    def load_data(self):
        #Permet de charger toute les données
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder)
        hero_folder = path.join(game_folder, 'img/hero')
        img_folder = path.join(game_folder, 'img')
        menu_folder = path.join(game_folder, 'img/menu')
        self.music_folder = path.join(game_folder, 'Soundtrack')
        generer(piece_debut, couloir_liste)
        self.map = Map(path.join(map_folder, 'map.txt'))

        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG))

        self.StartImage1 = pg.transform.scale(pg.image.load(path.join(menu_folder, SCREENIMG1)), (WIDTH, HEIGHT))
        self.StartImage2 = pg.transform.scale(pg.image.load(path.join(menu_folder, SCREENIMG2)), (WIDTH, HEIGHT))
        self.StartImage3 = pg.transform.scale(pg.image.load(path.join(menu_folder, SCREENIMG3)), (WIDTH, HEIGHT))

        self.StartImage = [self.StartImage1, self.StartImage2, self.StartImage3]

        self.sword_img = pg.image.load(path.join(img_folder, SWORD_IMG))

        self.wall_img = pg.image.load(path.join(img_folder+'/decor', WALL_IMG))
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))

        self.playerAttackRight1 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_slice left_1.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.playerAttackRight2 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_slice left_2.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.playerAttackLeft1 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_slice right_1.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.playerAttackLeft2 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_slice right_2.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.playerAttackDown1 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_slice down_1.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.playerAttackDown2 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_slice down_2.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.playerAttackUp1 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_slice up_1.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.playerAttackUp2 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_slice up_2.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))

        self.playerAttackUp = [self.playerAttackUp1, self.playerAttackUp2]
        self.playerAttackDown = [self.playerAttackDown1, self.playerAttackDown2]
        self.playerAttackRight = [self.playerAttackRight1, self.playerAttackRight2]
        self.playerAttackLeft = [self.playerAttackLeft1, self.playerAttackLeft2]

        self.playerAttacks = [self.playerAttackRight, self.playerAttackUp, self.playerAttackLeft, self.playerAttackDown]

        self.player_Move_Right = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run right_0.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Right1 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run right_1.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Right2 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run right_2.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_RightIdle = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run right_3.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Right4 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run right_4.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Right5 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run right_5.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))

        self.player_Move_Left = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run Left_0.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Left1 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run Left_1.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Left2 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run Left_2.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_LeftIdle = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run Left_3.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Left4 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run Left_4.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Left5 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run Left_5.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))

        self.player_Move_Up = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run Up_0.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Up1 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run Up_1.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Up2 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run Up_2.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Up3 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run Up_3.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Up4 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run Up_4.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))

        self.player_Move_Down = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run down_0.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Down1 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run down_1.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Down2 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run down_2.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Down3 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run down_3.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_Move_Down4 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_run down_4.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))

        self.player_idle_Down = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_idle_0.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_idle_Down1 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_idle_1.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_idle_Down2 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_idle_2.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))
        self.player_idle_Down3 = pg.transform.scale(pg.image.load(path.join(hero_folder, 'knight iso char_idle_3.png')).convert_alpha(), (TILESIZE - 10, TILESIZE - 10))

        self.playerAnimateRight = [self.player_Move_Right4, self.player_Move_Right1, self.player_Move_Right2, self.player_Move_Right4, self.player_Move_Right5]
        self.playerAnimateLeft = [self.player_Move_Left4, self.player_Move_Left1, self.player_Move_Left2, self.player_Move_Left4, self.player_Move_Left5]
        self.playerAnimateUp = [self.player_Move_Up, self.player_Move_Up1, self.player_Move_Up2, self.player_Move_Up3, self.player_Move_Up4]
        self.playerAnimateDown = [self.player_Move_Down, self.player_Move_Down1, self.player_Move_Down2, self.player_Move_Down3, self.player_Move_Down4]
        self.PlayerAnimateDownIdle = [self.player_idle_Down, self.player_idle_Down1, self.player_idle_Down2, self.player_idle_Down3, self.player_idle_Down]

    def new(self):
        # initialise toute les variables pour le début d'une nouvelle parite
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.swords = pg.sprite.Group()
        #Enumarate permet d'avoir l'indexe ET ce qu'y a à l'indexe dans une liste

        [[1, 0, 0], []]

        for row, tiles in enumerate(self.map.Data):
            Variables.GlobalWallBool.append([])
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                    Variables.GlobalWallBool[-1].append(1)
                else:
                    Variables.GlobalWallBool[-1].append(0)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    self.mob = Mob(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)


    def run(self):
        # Boucle principale du jeu, si playing = false, alors tout s'arrête
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # Mets à jours tout les sprites
        self.all_sprites.update()
        self.camera.update(self.player)
        #Permet de dessiner le grillade du jeu
        #Vérifie la collision entre les balles et les mobs
        hits = pg.sprite.groupcollide(self.mobs, self.swords, False, True)
        for hit in hits:
            hit.health -= SWORDDMG
            hit.vel = vec(0, 0)

        hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if hits:
            now2 = pg.time.get_ticks()
            if now2 - self.hitTime > Recover:
                self.hitTime = now2
                #Vérifie la collision entre le joueur et les mobs après le recovery time
                for hit in hits:
                    self.player.health -= MOBDMG
                if self.player.health <= 0:
                    self.playing = False

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("Knight Errant")
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.healthBar()

            #On décalle les objets, sans changer leur coordonnées
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #HUD APPEL
        draw_player_health(self.screen, 10, 10 , self.player.health / PLAYERLIFE)
        draw_player_powerup(self.screen, 220, 10, self.player.powerup / POWERUPBAR)
        pg.display.flip()

    def events(self):
        # Prend tout les évènements
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.show_start_screen()



    def show_start_screen(self):
        self.NotMenu = False
        Menu = True
        nowMenu = 0
        pos1 = WIDTH // 2 - 150, HEIGHT // 2 - 50
        dim = 300, 100
        while Menu:
            nowMenu += 1
##            pg.mixer.music.load(path.join(self.music_folder + '/menu', "awesomeness.wav"))
            if nowMenu >= 120:
                self.incrementMenu += 1
                nowMenu = 0
            if self.incrementMenu == 3:
                self.incrementMenu = 0
            self.screen.blit(self.StartImage[self.incrementMenu], (0, 0))
            boutton1 = Button(self, pos1, dim, TEAL, 'Start' )
            boutton1.draw()
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Menu = False
                    self.NotMenu = True
                    self.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    boutton1.click()


    def show_go_screen(self):
        pass

Variables.GlobalWallBool = []

# create the game object
g = Game()
Variables.PlayerAttackAnimation = g.playerAttacks
g.show_start_screen()
