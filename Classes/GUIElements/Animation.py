from Classes.Bomberman import Bomberman, p
import os


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

    def flip_frames(self):
        for i in range(len(self.frames)):
            self.frames[i] = p.transform.flip(self.frames[i], True, False)
