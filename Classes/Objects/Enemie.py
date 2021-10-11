from Classes.Bomberman import Bomberman, p


class Enemie:
    design = p.image.load("Assets/Scam/player.png")

    def __init__(self, s=2):
        self.rep = p.draw.circle(Bomberman.screen, (200, 123, 113), (50, 50), 20)
        self.speed = s
        self.moving = False

    def get_new_pos(self):  # berechnet den vektor richtung Player 1
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
        self.moving = vect != [0, 0]  # Player bewegt sich wenn der vector nicht 0 ist.

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
