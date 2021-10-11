from Classes.Bomberman import *
from Classes.GUIElements.Map import Map
from Classes.Objects.Player import Player
from Classes.GUIElements.Playerbox import Playerbox
from Classes.Objects.Enemie import Enemie


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
            pl = Player(i, name=f"Player{i + 1}",
                        afkAnimPath=self.playerDesigns[i]["afk"],
                        walkingAnimPath=self.playerDesigns[i]["walking"])
            self.players.append(pl)
            self.gui.append(Playerbox(pl))
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
        for i in range(len(self.players)):  # der input der Tasten wird in die Bewegung der Player umgewandelt
            self.players[i].move(moves[i])
        for e in self.enemies:
            e.move(self.map)

    def event_handler(self, event):
        if event.type == p.KEYDOWN:
            if event.key == p.K_SPACE:  # Spieler1 bombe wird geplaced wenn Space gedrückt wurde
                self.players[0].placebomb()
            elif event.key == p.K_RCTRL:  # Spieler2 Bomb rechte control knopf
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
        Bomberman.backgroundcolor = Bomberman.rainbow_fade(Bomberman.backgroundcolor, speed=1, start=122)
        Bomberman.screen.fill(Bomberman.backgroundcolor)  # hintergrund
        self.map.draw()  # map
        for o in self.gui + self.players + self.enemies:  # draw objects
            o.draw()
