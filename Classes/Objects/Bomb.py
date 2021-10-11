from Classes.Bomberman import Bomberman, p
from Classes.Objects.Bombanimation import Bombanimation


class Bomb:
    cooldown = 2 * Bomberman.fps  # 2 sec
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
        elif self.animation.draw():
            self.player.bombs.pop(0)

