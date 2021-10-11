from Classes.Bomberman import p


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
