from Classes.Bomberman import Bomberman, p
from Classes.Objects.Wall import Wall


# Map Objekt
class Map:
    # border values
    leftWall = 250  # wall_DistanceLeftSideFromWall
    rightWall = 30  # wall_DistanceRightFromWall
    sealing = -50  # wall_DistanceTopFromWall
    ground = 20  # wall_DistanceBottomFromWall
    mapimage_X = 290

    wall_side_design = p.image.load("Assets/Map/Bush2.png")  # wände links rechts
    wall_sideHitbox = (38, 70)

    wall_top_design = p.image.load("Assets/Map/Bush1.png")  # wände oben unten
    wall_topHitbox = (70, 40)

    barrier_design = p.image.load("Assets/Map/RTS_Crate_0.png")  # wände oben unten
    barrier_hitbox = (73, 73)

    wall_design = p.image.load("Assets/Scam/theREALbox.png")  # wände oben unten
    wall_hitbox = (73, 73)

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
                Wall(self.wall_side_design, size, self.wall_sideHitbox, (self.leftWall - 20, y), x_offset=self.mapimage_X))
            self.walls.append(
                Wall(self.wall_side_design, size, self.wall_sideHitbox, (Bomberman.screensize[0] - self.rightWall - 60, y),
                     x_offset=self.mapimage_X))

        size = (Wall.width + 50, Wall.height + 40)
        for i in range(int(Bomberman.screensize[0] / Wall.width)):
            y = self.leftWall + (i * Wall.width) + 25
            self.walls.append(
                Wall(self.wall_top_design, size, self.wall_topHitbox, (y, self.sealing), x_offset=self.mapimage_X))
            self.walls.append(Wall(self.wall_top_design, size, self.wall_topHitbox,
                                   (y, (Bomberman.screensize[1] - self.ground) - 30), x_offset=self.mapimage_X))
        # endregion

        # undestroyable walls...
        for x in range(1, 15, 2):
            for y in range(1, 11, 2):
                self.walls.append(
                    Wall(self.wall_design, (70, 70), self.barrier_hitbox, (320 + x * 72, 20 + y * 72),
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
