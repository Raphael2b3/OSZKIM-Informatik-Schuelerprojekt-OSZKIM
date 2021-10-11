from Classes.Bomberman import Bomberman, p
from Classes.Objects.Player import Player
from Classes.GUIElements.Animation import Animation


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

    def __init__(self, player: Player):
        # erstellt alle grafiken und position damit sie nicht immer wieder neue geladen werden müssen
        self.player = player
        self.y = 300 * player.id

        self.nameLabel = Bomberman.text_image(self.player.name, Bomberman.nameFont, Bomberman.white,
                                              (self.width / 2) - 70, self.y + 200)
        self.rainbowbox = p.Rect(self.x, self.y, self.width, self.height)
        self.mainbox = p.Rect(self.x + 4, self.y + 4, self.width - 10, self.height - 10)
        self.iconbox = p.Rect(self.x + 20, 20, 170, 160)
        self.icon = Animation(player.afkAnimPath, (200, 200))
        self.iconpos = p.rect.Rect(self.x, self.y + 10, 200, 200)
        self.scoreimage = Bomberman.text_image(str(self.player.punkte), x=(self.width / 2) - 70,
                                               y=220)  # (self.width/2) - 70, self.y + 400
        self.lastscore = self.player.punkte

        self.boximage = p.surface.Surface(self.mainbox.size)
        self.update()

    def draw(self):
        p.draw.rect(Bomberman.screen, self.bordercolor, self.rainbowbox, 0, self.borderthicness)  # colored Border
        Bomberman.screen.blit(self.boximage, self.mainbox)
        self.icon.draw(self.iconpos)  # icon des spielers
        self.bordercolor = Bomberman.rainbow_fade(self.bordercolor)  # bordercolor wird geändert (Regenbogen verlauf)

    def update(self):
        self.boximage.fill(self.color)

        # leben
        t = Bomberman.text_image(str(self.player.leben), Bomberman.arial30, Bomberman.white, self.width - 30, 15)
        self.boximage.blit(self.healthImage, (self.width - 80, 20))
        self.boximage.blit(t[0], t[1])  # health text

        # bomb
        t = Bomberman.text_image(str(3 - len(self.player.bombs)), Bomberman.arial30, Bomberman.white, self.width - 30,
                                 75)
        self.boximage.blit(self.bombImage, (self.width - 80, 80))
        self.boximage.blit(t[0], t[1])  # bomb Text

        # power
        t = Bomberman.text_image(str(self.player.bombpower), Bomberman.arial30, Bomberman.white, self.width - 30, 135)
        self.boximage.blit(self.strengthImage, (self.width - 80, 140))
        self.boximage.blit(t[0], t[1])  # power Text

        # speed
        t = Bomberman.text_image(str(self.player.speed), Bomberman.arial30, Bomberman.white, self.width - 30, 195)
        self.boximage.blit(self.speedImage, (self.width - 80, 195))
        self.boximage.blit(t[0], t[1])  # health Text

        self.boximage.blit(self.nameLabel[0], ((self.width / 2) - 70, 200))  # Name des Spielers

        self.boximage.blit(self.scoreimage[0], self.scoreimage[1])  # score des spielers

        p.draw.rect(self.boximage, (0, 0, 0), self.iconbox, 3, 5)  # border icon
