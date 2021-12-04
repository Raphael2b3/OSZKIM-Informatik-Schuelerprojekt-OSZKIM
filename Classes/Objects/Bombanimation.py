from Classes.Bomberman import Bomberman, p
from Classes.GUIElements.Map import Map


class Bombanimation:
    state = 0
    distance = 90
    thickness = 30
    vectors = {
        "top": [0, -1],  # top
        "bottom": [0, 1],  # bottom
        "left": [-1, 0],  # left
        "right": [1, 0]  # right
    }
    timeInSec = 0.3

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

        self.speed = self.distance / (self.timeInSec*Bomberman.fps)

    def draw(self):
        print(self.speed)
        self.move()
        if self.state < self.timeInSec * Bomberman.fps:
            for k in self.hitboxen.keys():
                p.draw.rect(Bomberman.screen, (215, 215, 53), self.hitboxen[k])
        else:
            return True
        self.state += 1
        return False

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
                    map.scene.gui[self.player.id].scoreimage = Bomberman.text_image(str(self.player.punkte), x=x, y=y)
            elif id == "player" and objekt.rep.colliderect(self.hitboxen[key]):
                deleted_hitboxen.append(key)
                objekt.leben -=1
                if objekt.leben <=0: objekt.dead = True
        for hitbox_key in deleted_hitboxen:
            self.hitboxen.pop(hitbox_key)

    def move(self):
        for k in self.hitboxen.keys():
            vect = self.vectors[k]
            self.hitboxen[k].topleft = (self.hitboxen[k].topleft[0] + vect[0]*self.speed,
                                        self.hitboxen[k].topleft[1] + vect[1]*self.speed)  # zukünftige hitbox

