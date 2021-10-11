import pygame as p
import re
"""from Classes.GUIElements.Animation import Animation
from Classes.GUIElements.Button import Button
from Classes.GUIElements.Map import Map
from Classes.GUIElements.Playerbox import Playerbox
from Classes.Objects.Bombanimation import Bombanimation
from Classes.Scenes.InGameScene import InGameScene
"""

p.init()


class Bomberman:
    # windowsettings
    screensize = (1425, 820)
    screen = p.display.set_mode(screensize)
    fps = 120

    # design
    backgroundcolor = (96, 109, 156)
    arial20 = p.font.SysFont("Arial", 20)
    arial30 = p.font.SysFont("Arial", 30)
    nameFont = p.font.SysFont("Adobe Devanagari", 30)
    white = p.color.Color(255, 255, 255)
    blocksize = 72

    # spawnpositions
    spawn = [(350, 55), (1358, 775), (1358, 45), (350, 775)]

    # pygame objekte
    clock = p.time.Clock()
    destroyQ = []

    # aktuelle scene
    currentscene = None

    # statische Funktionen
    @staticmethod
    def rainbow_fade(rgb, speed=3, brightness=200, start=0):
        r, g, b = rgb
        if r == brightness and not g >= brightness and b == start:
            g += speed
        elif g == brightness and not r <= start:
            r -= speed
        elif g == brightness and r == start and not b >= brightness:
            b += speed
        elif b == brightness and not g <= start:
            g -= speed
        elif b == brightness and not r >= brightness:
            r += speed
        elif r == brightness and b >= start and g == start:
            b -= speed
        else:
            r, g, b = 0, 255, 0
        out = ()
        for c in [r, g, b]:
            if c > brightness: c = brightness
            if c < start: c = start
            out = out.__add__((c,))
        return out

    @staticmethod
    def natural_sort(l):  # Sortiert die Bilder für die Animationen richtig
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(l, key=alphanum_key)

    @staticmethod  # generiert ein Bild aus Text informationen und positionen
    def text_image(text1, font=arial20, color=(255, 255, 255), x=100, y=100):
        Text = font.render(text1, False, color)
        return Text, (x, y)  # rückgaber der grafik und der position im bild
