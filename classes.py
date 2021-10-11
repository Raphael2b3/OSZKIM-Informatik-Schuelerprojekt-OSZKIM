import pygame as p
import os, re, random

""" 
Feld: 15x11 Felder
Start: (300,5)
index_wand -> x und y => 72

"""

p.init()


# TODO DEFINE PARAMETER TYPE

# Static class
class Bomberman:
    # windowsettings
    screensize = (1425, 820)
    screen = p.display.set_mode(screensize)
    fps = 120

    # design
    backgroundcolor = (96, 109, 156)
    arial20 = p.font.SysFont("Arial", 20)
    arial30 = p.font.SysFont("Arial", 30)
    nameFont = p.font.SysFont("Adobe Devanagari", 30)
    white = p.color.Color(255, 255, 255)
    blocksize = 72

    # spawnpositions
    spawn = [(350, 55), (1358, 775), (1358, 45), (350, 775)]

    # pygame objekte
    clock = p.time.Clock()
    destroyQ = []

    # aktuelle scene
    currentscene = None

    # statische Funktionen
    @staticmethod
    def RainbowFade(rgb, speed=3, brightness=200, start=0):
        r, g, b = rgb
        if r == brightness and not g >= brightness and b == start:
            g += speed
        elif g == brightness and not r <= start:
            r -= speed
        elif g == brightness and r == start and not b >= brightness:
            b += speed
        elif b == brightness and not g <= start:
            g -= speed
        elif b == brightness and not r >= brightness:
            r += speed
        elif r == brightness and b >= start and g == start:
            b -= speed
        else:
            r, g, b = 0, 255, 0
        out = ()
        for c in [r, g, b]:
            if c > brightness: c = brightness
            if c < start: c = start
            out = out.__add__((c,))
        return out

    @staticmethod
    def natural_sort(l):  # Sortiert die Bilder für die Animationen richtig
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(l, key=alphanum_key)

    @staticmethod  # generiert ein Bild aus Text informationen und positionen
    def textImage(text1, Font=arial20, color=(255, 255, 255), x=100, y=100):
        Text = Font.render(text1, False, color)
        return Text, (x, y)  # rückgaber der grafik und der position im bild


# MainMenuScene
class MainMenuScene:
    #  events der scene
    ePLAYBUTTON = p.USEREVENT + 1
    eOPTIONBUTTON = p.USEREVENT + 2
    eQUITBUTTON = p.USEREVENT + 3
    eWIN = p.USEREVENT + 4
    eLOSE = p.USEREVENT + 5

    # Pfade
    pPLAYBTN_MO = "Assets/Buttons/Play/Button2.png"  # Play-Button
    pPLAYBTN = "Assets/Buttons/Play/Button1.png"

    pOPTBTN_MO = "Assets/Buttons/Optionen/ButtonOpt2.png"  # Option-Button
    pOPTBTN = "Assets/Buttons/Optionen/ButtonOpt1.png"

    pQUITBTN_MO = "Assets/Buttons/Quit/Quit2.png"  # Quit-Button
    pQUITBTN = "Assets/Buttons/Quit/Quit.png"

    pTITELANIMATION = "Assets/Animation/Titel/"  # Ordner mit Frames der Titel Animation

    buttons = {}

    def __init__(self):
        # erstellt die objekte der scene sodass man sie nicht immer wieder generieren muss
        self.gamestart = False
        self.screemimage = p.surface.Surface(p.display.get_window_size())

        # buttons
        self.buttons["play"] = Button(self.pPLAYBTN_MO, self.pPLAYBTN, Bomberman.screensize[0] / 2, 450,
                                      self.ePLAYBUTTON)
        self.buttons["option"] = Button(self.pOPTBTN_MO, self.pOPTBTN, Bomberman.screensize[0] / 2, 650,
                                        self.eOPTIONBUTTON)
        self.buttons["quit"] = Button(self.pQUITBTN_MO, self.pQUITBTN, 1220, 700, self.eQUITBUTTON)

        self.Titelbild = Animation(self.pTITELANIMATION, (955, 285), speed=10)
        self.Titelbild.rect.center = (Bomberman.screensize[0] / 2, (Bomberman.screensize[1] / 3) - 80)
        self.credits = Bomberman.textImage("© Raphael,Temesgen & Gordon", Bomberman.arial20, Bomberman.white, 0, 790)
        self.update()

    def draw(self):  # pro frame aufgerufen
        Bomberman.screen.blit(self.screemimage, self.screemimage.get_rect())
        if self.Titelbild.state < 0.2 or not self.gamestart:  # freeze wenn die animation im letzten bild ist oder
            #  noch nicht play gedrückt wurde()
            self.Titelbild.draw(self.Titelbild.rect, freeze=True)
        else:
            self.Titelbild.draw(self.Titelbild.rect)
        if self.Titelbild.state < 0.2:  # wenn die animation fertig ist
            self.changeScene()  # scene wird gewechselt

    def update(self):
        # zeichnet die gespeicherten objekte der scene für jeden frame auf
        self.screemimage.fill((0, 0, 0))  # Hintergrund füllen
        self.screemimage.blit(self.credits[0], self.credits[1])  # "copyright by temesgen gordon & raphael"
        # bestimmt wann das Titelbild gefreezed sein soll und wann nicht
        for button in self.buttons.values():
            self.screemimage.blit(button.get_currentframe(), button.rep)

    def key_press_handler(self, key_pressed):
        pass

    def event_handler(self, event):  # pro frame aufgerufen
        if event.type == self.eQUITBUTTON:  # Event: wenn der Quitbutton gedrückt wurde
            exit()
        elif event.type == self.ePLAYBUTTON:  # Event: wenn der Playbutton gedrückt wurde
            self.gamestart = True  # spielstartet
        else:
            for button in self.buttons.values():
                button.event_handler(event, self)

    def collision_detection(self):
        pass

    def changeScene(self):
        Bomberman.currentscene = InGameScene(nOfPlayers=2)  # die GameScene wird geladen, man kann mit "nOfPlayers" und
        # "nOfEnemies" angeben wie viele Spieler und gegner erstellt werden sollen


# Button Objekt
class Button:

    def __init__(self, mouseover: str, idle: str, x, y, event, size=(400, 200)):
        self.event = p.event.Event(event)
        self.image_mouseover = p.transform.scale(p.image.load(mouseover), size)
        self.image_idle = p.transform.scale(p.image.load(idle), size)
        self.rep = self.image_idle.get_rect()
        self.rep.center = (x, y)
        self.mousover = False

    def event_handler(self, event, scene: MainMenuScene):
        if self.rep.collidepoint(p.mouse.get_pos()):
            if not self.mousover:
                self.mousover = True
                scene.update()
            else:
                self.mousover = True
            if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                p.event.post(self.event)
        else:
            if self.mousover:
                self.mousover = False
                scene.update()
            else:
                self.mousover = False

    def get_currentframe(self):
        return self.image_mouseover if self.mousover else self.image_idle


# Ingame Scene
class InGameScene:
    playerDesigns = {
        0:
            {
                "afk": "Assets/Animation/Character1/Idle Blink/",
                "walking": "Assets/Animation/Character1/Walking/"
            },
        1:
            {
                "afk": "Assets/Animation/Character2/Idle Blink/",
                "walking": "Assets/Animation/Character2/Walking/"
            }
    }

    def __init__(self, nOfPlayers=1, nOfEnemies=0):
        # erstellt objekte der scene
        self.items = []
        self.bombs = []
        self.players = []
        self.enemies = []
        self.gui = []
        self.map = Map(self)

        for i in range(nOfPlayers):
            p = Spieler(i, name=f"Spieler{i + 1}",
                        afkAnimPath=self.playerDesigns[i]["afk"],
                        walkingAnimPath=self.playerDesigns[i]["walking"])
            self.players.append(p)
            self.gui.append(Playerbox(p))
        for i in range(nOfEnemies):
            self.enemies.append(Enemie())

    # control handling
    def key_press_handler(self, keys_pressed):
        moves = [[0, 0], [0, 0]]  # Es werden für die Pfeiltasten und WASD das movement aufgenommen
        if keys_pressed[p.K_w]:
            moves[0][1] -= 1
        if keys_pressed[p.K_a]:
            moves[0][0] -= 1
        if keys_pressed[p.K_s]:
            moves[0][1] += 1
        if keys_pressed[p.K_d]:
            moves[0][0] += 1

        if keys_pressed[p.K_UP]:
            moves[1][1] -= 1
        if keys_pressed[p.K_LEFT]:
            moves[1][0] -= 1
        if keys_pressed[p.K_DOWN]:
            moves[1][1] += 1
        if keys_pressed[p.K_RIGHT]:
            moves[1][0] += 1

        if keys_pressed[p.K_ESCAPE]:
            self.map.hindernisse = []
            # self.bombs.clear()
            # Bomberman.currentscene = MainMenuScene()
        for i in range(len(self.players)):  # der input der Tasten wird in die Bewegung der Spieler umgewandelt
            self.players[i].move(moves[i])
        for e in self.enemies:
            e.move(self.map)

    def event_handler(self, event):
        if event.type == p.KEYDOWN:
            if event.key == p.K_SPACE:  # Spieler1 bombe wird geplaced wenn Space gedrückt wurde
                self.players[0].placebomb()
            elif event.key == p.K_RCTRL:  # Spieler2 Bombe rechte control knopf
                self.players[1].placebomb()

    def collision_detection(self):
        remove = []
        for wand in self.map.walls:
            for o in self.players + self.enemies + self.items:
                o.collision_detection(wand, "wand", remove, self.map)
        for hindernis in self.map.hindernisse:
            for o in self.players + self.enemies + self.items:
                o.collision_detection(hindernis, "hindernis", remove, self.map)
        for o in remove:
            if o in self.map.hindernisse:
                self.map.hindernisse.remove(o)
        if len(remove) > 0:
            self.map.update()
            for g in self.gui:
                g.update()

    # per frame
    def draw(self):
        Bomberman.backgroundcolor = Bomberman.RainbowFade(Bomberman.backgroundcolor, speed=1, start=122)
        Bomberman.screen.fill(Bomberman.backgroundcolor)  # hintergrund
        self.map.draw()  # map
        for o in self.gui + self.players + self.enemies:  # draw objects
            o.draw()


# Animationsobjekt
class Animation:
    orientation = "right"

    # zeichnet jenach state nen anderen frame
    def __init__(self, path2frames, size, speed=10):
        self.frames = []
        valid_images = [".jpg", ".gif", ".png", ".tga"]
        for f in Bomberman.natural_sort(os.listdir(path2frames)):
            ext = os.path.splitext(f)[1]
            if ext.lower() in valid_images:
                self.frames.append(p.transform.scale(p.image.load(os.path.join(path2frames, f)), size))
        self.rect = self.frames[0].get_rect()
        self.speed = speed / Bomberman.fps
        self.state = len(self.frames) - 1

    def draw(self, rect, freeze=False, x=0, y=0):
        self.rect.center = (rect.center[0] + x, rect.center[1] + y)
        Bomberman.screen.blit(self.frames[int(len(self.frames) - self.state)], self.rect)
        if not freeze:
            self.state = self.state - self.speed if self.state - self.speed >= 0 else len(self.frames) - 1

    def current_frame(self):
        return self.frames[int(len(self.frames) - self.state)]

    def flipLR(self):
        for i in range(len(self.frames)):
            self.frames[i] = p.transform.flip(self.frames[i], True, False)


# Map Objekt
class Map:
    # border values
    leftWall = 250  # wall_DistanceLeftSideFromWall
    rightWall = 30  # wall_DistanceRightFromWall
    sealing = -50  # wall_DistanceTopFromWall
    ground = 20  # wall_DistanceBottomFromWall
    mapimage_X = 290

    wall_design = p.image.load("Assets/Map/Bush2.png")  # wände links rechts
    wall_sideHitbox = (38, 70)

    wall_top_design = p.image.load("Assets/Map/Bush1.png")  # wände oben unten
    wall_topHitbox = (70, 40)

    hindernis_design = p.image.load("Assets/Map/RTS_Crate_0.png")  # wände oben unten
    hindernis_Hitbox = (70, 40)

    groundcolor = (39, 45, 64)

    def __init__(self, scene):
        self.maprect = p.rect.Rect(self.mapimage_X, 0, Bomberman.screensize[0] - self.mapimage_X,
                                   Bomberman.screensize[1])

        self.mapimage = p.surface.Surface(self.maprect.size)
        self.scene = scene
        self.walls = []
        self.hindernisse = []

        # erstellt den boden
        self.bodenplatten = []
        for i in range(15):
            for j in range(11):
                self.bodenplatten.append(
                    p.Rect(320 + (i * 72) - self.mapimage_X, 20 + (j * 72), Wall.width, Wall.height))

        # region Erstellt die Wände
        size = (Wall.width + 100, Wall.height + 60)
        for i in range(int(Bomberman.screensize[1] / Wall.height) + 1):
            y = -30 + (i * Wall.height)
            self.walls.append(
                Wall(self.wall_design, size, self.wall_sideHitbox, (self.leftWall - 20, y), x_offset=self.mapimage_X))
            self.walls.append(
                Wall(self.wall_design, size, self.wall_sideHitbox, (Bomberman.screensize[0] - self.rightWall - 60, y),
                     x_offset=self.mapimage_X))

        size = (Wall.width + 50, Wall.height + 40)
        for i in range(int(Bomberman.screensize[0] / Wall.width)):
            y = self.leftWall + (i * Wall.width) + 25
            self.walls.append(
                Wall(self.wall_top_design, size, self.wall_topHitbox, (y, self.sealing), x_offset=self.mapimage_X))
            self.walls.append(Wall(self.wall_top_design, size, self.wall_topHitbox,
                                   (y, (Bomberman.screensize[1] - self.ground) - 30), x_offset=self.mapimage_X))
        # endregion

        # random walls
        for x in range(1, 15, 2):
            for y in range(1, 11, 2):
                self.hindernisse.append(
                    Wall(self.hindernis_design, (100, 100), self.hindernis_Hitbox, (300 + x * 72, 40 + y * 72),
                         x_offset=self.mapimage_X))

        self.mapimage = self.mapimage.convert_alpha()
        self.update()

    def draw(self):
        Bomberman.screen.blit(self.mapimage, self.maprect)

    def update(self):
        self.mapimage.fill((0, 0, 0, 0))
        # malt den boden
        for plate in self.bodenplatten:
            p.draw.rect(self.mapimage, self.groundcolor, plate)
        # malt die wände
        for o in self.walls + self.hindernisse:
            self.mapimage.blit(o.design, o.rep)


# Charactere
class Spieler:
    # eigenschaften
    speed = 5
    punkte = 0
    leben = 3
    bombcooldown = 0
    bombpower = 1
    movingstate = "afk"
    vector = [0, 0]
    # design
    offset = [0, -10]
    size = (100, 100)
    hitbox = (33, 40)

    def __init__(self, id, name, afkAnimPath="Assets/Animation/Character1/Idle Blink/",
                 walkingAnimPath="Assets/Animation/Character1/Walking/"):
        # erstellt einzig artige eigenschaften
        self.walkingAnimPath = walkingAnimPath
        self.afkAnimPath = afkAnimPath
        self.id = id
        self.walking_animation = Animation(self.walkingAnimPath, self.size)
        self.walking_animation.orientation = "right"
        self.afk_animation = Animation(self.afkAnimPath, self.size)
        self.name = name
        x, y = Bomberman.spawn[id]  # positioniert den spieler an seinen Spawnpunkt
        self.rep = p.rect.Rect(x, y, self.hitbox[0], self.hitbox[1])
        self.rep.center = Bomberman.spawn[id]
        self.bombs = []

    def collision_detection(self, objekt, id, remove, map: Map):
        if id in ["wand", "hindernis"]:
            if objekt.hitbox.colliderect(self.rep):
                p.draw.rect(Bomberman.screen, (122, 122, 0), self.rep)
                p.draw.rect(Bomberman.screen, (122, 0, 122), objekt.hitbox)
                self.move([-self.vector[0], -self.vector[1]])
        for bomb in self.bombs:
            bomb.collision_detection(objekt, id, remove, map)

    def move(self, vect):  # collision
        self.vector = vect
        if vect == [0, 0]: self.movingstate = "afk"
        if vect[0] > 0: self.movingstate = "right"
        if vect[0] < 0: self.movingstate = "left"
        self.rep.topleft = (
            self.rep.topleft[0] + vect[0] * self.speed, self.rep.topleft[1] + vect[1] * self.speed)  # zukünftige hitbox

    def placebomb(self):
        if self.bombcooldown == 0 and len(self.bombs) < 3:  # wenn noch bomben übrig sind
            self.bombs.append(Bombe(self.rep.center, self))

    def draw(self):
        self.walkAnim()
        for bomb in self.bombs:
            bomb.draw()
        if len(self.bombs) == 3 and self.bombcooldown == 0:
            self.bombcooldown = 2 * Bomberman.fps
        elif self.bombcooldown > 0:
            self.bombcooldown -= 1

    def walkAnim(self):
        if self.movingstate == "afk":
            self.afk_animation.draw(self.rep, y=self.offset[1])  # afk animation wird gezeichnet
        else:
            if self.walking_animation.orientation == self.movingstate:
                self.walking_animation.draw(self.rep, y=self.offset[1])  # lauf animation wird gezeichnet
            else:
                self.walking_animation.orientation = self.movingstate
                self.walking_animation.flipLR()
                self.afk_animation.flipLR()
                self.walking_animation.draw(self.rep, y=self.offset[1])


class Enemie:
    design = p.image.load("Assets/Scam/player.png")

    def __init__(self, s=2):
        self.rep = p.draw.circle(Bomberman.screen, (200, 123, 113), (50, 50), 20)
        self.speed = s
        self.moving = False

    def get_new_pos(self):  # berechnet den vektor richtung Spieler 1
        a = Bomberman.currentscene.players[0].rep.bottomright
        b = self.rep.center
        v = (a[0] - b[0], a[1] - b[1])
        if self.speed > (v[0] ** 2 + v[1] ** 2) ** 0.5:
            return a

        if v != (0, 0):
            k = (self.speed ** 2 / (v[0] ** 2 + v[1] ** 2)) ** (1 / 2)
        else:
            return [0, 0]
        return [k * v[0], k * v[1]]

    def move(self, map):
        vect = self.get_new_pos()
        self.moving = vect != [0, 0]  # Spieler bewegt sich wenn der vector nicht 0 ist.

        z = self.rep  # kopiert hitbox
        z.topleft = (z.topleft[0] + vect[0] * self.speed, z.topleft[1] + vect[1] * self.speed)  # zukünftige hitbox
        br = False  # unterbricht nicht folgenden schleife
        for i in range(self.speed):  # geht so weit bis er eine Wand trifft.
            if br: break  # schleife wird unterbrochen wenn in der folgenden schleife keine collision gefunden wurde
            br = True
            for wall in map.walls:
                if wall.hitbox.colliderect(z):  # Wenn: zukunfts position ist in wand
                    z.topleft = (z.topleft[0] - vect[0], z.topleft[1] - vect[1])  # die Strecke wird verkleinert
                    br = False  # collision wurde gefunden
                    break
        self.rep = z  # eigene position wird geupdated

    def draw(self):
        p.draw.circle(Bomberman.screen, (123, 123, 123), self.rep.center, 20)


class Playerbox:
    x = 0
    y = 0
    width = 290
    height = 250
    bordercolor = (255, 0, 0)
    color = (25, 25, 36)
    borderthicness = 0

    # icons werden vorausgeladen
    healthImage = p.transform.scale(p.image.load("Assets/Symbols/heart.png"), (30, 30))
    bombImage = p.transform.scale(p.image.load("Assets/Items/bomb100.png"), (30, 30))
    strengthImage = p.transform.scale(p.image.load("Assets/Symbols/strength.png"), (30, 30))
    speedImage = p.transform.scale(p.image.load("Assets/Symbols/pngwing.png"), (40, 40))

    def __init__(self, player: Spieler):
        # erstellt alle grafiken und position damit sie nicht immer wieder neue geladen werden müssen
        self.player = player
        self.y = 300 * player.id

        self.nameLabel = Bomberman.textImage(self.player.name, Bomberman.nameFont, Bomberman.white,
                                             (self.width / 2) - 70,
                                             self.y + 200)
        self.rainbowbox = p.Rect(self.x, self.y, self.width, self.height)
        self.mainbox = p.Rect(self.x + 4, self.y + 4, self.width - 10, self.height - 10)
        self.iconbox = p.Rect(self.x + 20, 20, 170, 160)
        self.icon = Animation(player.afkAnimPath, (200, 200))
        self.iconpos = p.rect.Rect(self.x, self.y + 10, 200, 200)
        self.scoreimage = Bomberman.textImage(str(self.player.punkte), x=(self.width / 2) - 70,
                                              y=220)  # (self.width/2) - 70, self.y + 400
        self.lastscore = self.player.punkte

        self.boximage = p.surface.Surface(self.mainbox.size)
        self.update()

    def draw(self):
        p.draw.rect(Bomberman.screen, self.bordercolor, self.rainbowbox, 0, self.borderthicness)  # colored Border
        Bomberman.screen.blit(self.boximage, self.mainbox)
        self.icon.draw(self.iconpos)  # icon des spielers
        self.bordercolor = Bomberman.RainbowFade(self.bordercolor)  # bordercolor wird geändert (Regenbogen verlauf)

    def update(self):
        self.boximage.fill(self.color)

        # leben
        t = Bomberman.textImage(str(self.player.leben), Bomberman.arial30, Bomberman.white, self.width - 30,
                                15)
        self.boximage.blit(self.healthImage, (self.width - 80, 20))
        self.boximage.blit(t[0], t[1])  # health text

        # bomb
        t = Bomberman.textImage(str(3 - len(self.player.bombs)), Bomberman.arial30, Bomberman.white, self.width - 30,
                                75)
        self.boximage.blit(self.bombImage, (self.width - 80, 80))
        self.boximage.blit(t[0], t[1])  # bomb Text

        # power
        t = Bomberman.textImage(str(self.player.bombpower), Bomberman.arial30, Bomberman.white, self.width - 30,
                                135)
        self.boximage.blit(self.strengthImage, (self.width - 80, 140))
        self.boximage.blit(t[0], t[1])  # power Text

        # speed
        t = Bomberman.textImage(str(self.player.speed), Bomberman.arial30, Bomberman.white, self.width - 30,
                                195)
        self.boximage.blit(self.speedImage, (self.width - 80, 195))
        self.boximage.blit(t[0], t[1])  # health Text

        self.boximage.blit(self.nameLabel[0], ((self.width / 2) - 70, 200))  # Name des Spielers

        self.boximage.blit(self.scoreimage[0], self.scoreimage[1])  # score des spielers

        p.draw.rect(self.boximage, self.bordercolor, self.iconbox, 3, 5)  # border icon


class Wall:  # wand objekt
    width = 70
    height = 70

    def __init__(self, design, size, hitbox, position, x_offset=0, y_offset=0):
        # generiert die hitboxen und grafiken
        self.hitbox = p.rect.Rect(position[0], position[1], hitbox[0], hitbox[1])
        self.design = p.transform.scale(design, size)
        self.rep = self.design.get_rect()
        self.rep.topleft = position[0] - x_offset, position[1] - y_offset
        self.hitbox.center = self.rep.center[0] + x_offset, self.rep.center[1] + y_offset


class Bombe:
    # TODO MAKE FPS ADAPTABLE
    cooldown = 5 * Bomberman.fps / 10
    design = p.transform.scale(p.image.load("Assets/Items/bomb100.png"), (50, 50))

    def __init__(self, position, player):
        self.player = player
        self.rep = self.design.get_rect()
        self.rep.center = position
        self.animation = Bombanimation(position, player)

    def collision_detection(self, objekt, id, remove, map):
        if self.cooldown == 0:
            self.animation.collision_detection(objekt, id, remove, map)

    def draw(self):
        if self.cooldown > 0:
            Bomberman.screen.blit(self.design, self.rep)
            self.cooldown -= 1
        elif self.animation.state < self.animation.timeInSec * Bomberman.fps:
            self.animation.draw()
        else:
            self.player.bombs.pop(0)


class Bombanimation:
    state = 0
    speed = 10
    thickness = 30
    vectors = {
        "top": [0, -1],  # top
        "bottom": [0, 1],  # bottom
        "left": [-1, 0],  # left
        "right": [1, 0]  # right
    }
    timeInSec = 1

    def __init__(self, position, player):
        self.player = player
        self.position = x, y = position
        self.hitboxen = {
            "top": p.rect.Rect(x, y, self.thickness, self.thickness),  # top
            "bottom": p.rect.Rect(x, y, self.thickness, self.thickness),  # bottom
            "left": p.rect.Rect(x, y, self.thickness, self.thickness),  # left
            "right": p.rect.Rect(x, y, self.thickness, self.thickness)  # right
        }
        for k in ["top", "bottom", "left", "right"]:
            self.hitboxen[k].center = position

    def draw(self):

        self.move()
        if self.state < self.timeInSec * Bomberman.fps:
            for k in self.hitboxen.keys():
                p.draw.rect(Bomberman.screen, (215, 215, 53), self.hitboxen[k])
        self.state += 1

    def collision_detection(self, objekt, id, remove, map: Map):
        deleted_hitboxen = []
        for key in self.hitboxen.keys():
            if id == "wand" and objekt.hitbox.colliderect(self.hitboxen[key]):  # Wenn: zukunfts position ist in wand
                deleted_hitboxen.append(key)

            elif id == "hindernis" and objekt.hitbox.colliderect(
                    self.hitboxen[key]):  # Wenn: zukunfts position ist in wand
                if objekt not in remove:
                    remove.append(objekt)
                    self.player.punkte += 10
                    x, y = map.scene.gui[self.player.id].scoreimage[1]
                    map.scene.gui[self.player.id].scoreimage = Bomberman.textImage(str(self.player.punkte), x=x, y=y)

        for hitbox_key in deleted_hitboxen:
            self.hitboxen.pop(hitbox_key)

    def move(self):
        for k in self.hitboxen.keys():
            vect = self.vectors[k]
            self.hitboxen[k].topleft = (self.hitboxen[k].topleft[0] + vect[0] * self.speed,
                                        self.hitboxen[k].topleft[1] + vect[1] * self.speed)  # zukünftige hitbox
