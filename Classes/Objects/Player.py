from Classes.Bomberman import Bomberman, p
from Classes.GUIElements.Animation import Animation
from Classes.GUIElements.Map import Map
from Classes.Objects.Bomb import Bomb


# Charactere
class Player:
    # eigenschaften
    speed = 2
    punkte = 0
    leben = 3
    bombcooldown = 0
    bombpower = 1
    movingstate = "afk"
    dead = False
    vector = [0, 0]
    # design
    offset = [0, -10]
    size = (100, 100)
    hitbox = (33, 40)
    
    def __init__(self, id, name, afkAnimPath="Assets/Animation/Character1/Idle Blink/",
                 walkingAnimPath="Assets/Animation/Character1/Walking/",walkingAnimPath="Assets/Animation/Character1/Dying/"):
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
                self.movingstate = "left" if self.movingstate == "right" and self.movingstate != "afk" else "right"
        elif id == "player":
            for bomb in objekt.bombs:
                bomb.collision_detection(self, "player", remove ,map)
        for bomb in self.bombs:
            bomb.collision_detection(objekt, id, remove, map)
            

    def move(self, vect):  # collision
        self.vector = vect
        if vect == [0, 0]: self.movingstate = "afk"
        if vect[0] > 0: self.movingstate = "right"
        if vect[0] < 0: self.movingstate = "left"
        self.rep.topleft = (
            self.rep.topleft[0] + vect[0] * self.speed, self.rep.topleft[1] + vect[1] * self.speed)  # zukünftige hitbox

    def placebomb(self, scene):
        if self.bombcooldown == 0 and len(self.bombs) < 3:  # wenn noch bomben übrig sind
            self.bombs.append(Bomb(self.rep.center, self))
            scene.gui[self.id].update()


    def draw(self):
        self.walkAnim()
        for bomb in self.bombs:
            bomb.draw()
        if len(self.bombs) == 3 and self.bombcooldown == 0:
            self.bombcooldown = 2 * Bomberman.fps
        elif self.bombcooldown > 0:
            self.bombcooldown -= 1

    def walkAnim(self):
        if not self.dead:
            if self.movingstate == "afk":
                self.afk_animation.draw(self.rep, y=self.offset[1])  # afk animation wird gezeichnet
            else:
                if self.walking_animation.orientation == self.movingstate:
                    self.walking_animation.draw(self.rep, y=self.offset[1])  # lauf animation wird gezeichnet
                else:
                    self.walking_animation.orientation = self.movingstate
                    self.walking_animation.flip_frames()
                    self.afk_animation.flip_frames()
                    self.walking_animation.draw(self.rep, y=self.offset[1])
        else:
            pass

