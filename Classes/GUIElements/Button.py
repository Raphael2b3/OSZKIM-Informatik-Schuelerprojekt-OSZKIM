from Classes.Bomberman import p


# Button Objekt
class Button:

    def __init__(self, mouseover: str, idle: str, x, y, event, size=(400, 200)):
        self.event = p.event.Event(event)
        self.image_mouseover = p.transform.scale(p.image.load(mouseover), size)
        self.image_idle = p.transform.scale(p.image.load(idle), size)
        self.rep = self.image_idle.get_rect()
        self.rep.center = (x, y)
        self.mousover = False

    def event_handler(self, event, scene):
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
