from Classes.Bomberman import *
from Classes.GUIElements.Button import Button
from Classes.GUIElements.Animation import Animation
from Classes.Scenes.InGameScene import InGameScene


class MainMenuScene:
# events der scene
ePLAYBUTTON = p.USEREVENT + 1
eOPTIONBUTTON = p.USEREVENT + 2
eQUITBUTTON = p.USEREVENT + 3
eWIN = p.USEREVENT + 4
eLOSE = p.USEREVENT + 5

# Pfade
pPLAYBTN_MO = "Assets/Buttons/Play/Button2.png"  # Play-Button
pPLAYBTN = "Assets/Buttons/Play/Button1.png"

pOPTBTN_MO = "Assets/Buttons/Optionen/ButtonOpt2.png"  # Option-Button
pOPTBTN = "Assets/Buttons/Optionen/ButtonOpt1.png"

pQUITBTN_MO = "Assets/Buttons/Quit/Quit2.png"  # Quit-Button
pQUITBTN = "Assets/Buttons/Quit/Quit.png"

pTITELANIMATION = "Assets/Animation/Titel/"  # Ordner mit Frames der Titel Animation

buttons = {}

def __init__(self):
    # erstellt die objekte der scene sodass man sie nicht immer wieder generieren muss
    self.gamestart = False
    self.menu = False
    self.screenimage = p.surface.Surface(p.display.get_window_size())

    # buttons
    self.buttons["play"] = Button(self.pPLAYBTN_MO, self.pPLAYBTN, Bomberman.screensize[0] / 2, 450,
                                  self.ePLAYBUTTON)
    self.buttons["option"] = Button(self.pOPTBTN_MO, self.pOPTBTN, Bomberman.screensize[0] / 2, 650,
                                    self.eOPTIONBUTTON)
    self.buttons["quit"] = Button(self.pQUITBTN_MO, self.pQUITBTN, 1220, 700, self.eQUITBUTTON)

    self.Titelbild = Animation(self.pTITELANIMATION, (955, 285), speed=10)
    self.Titelbild.rect.center = (Bomberman.screensize[0] / 2, (Bomberman.screensize[1] / 3) - 80)
    self.credits = Bomberman.text_image("© Raphael,Temesgen & Gordon", Bomberman.arial20, Bomberman.white, 0, 790)
    self.update()

def draw(self):  # pro frame aufgerufen
    Bomberman.screen.blit(self.screenimage, self.screenimage.get_rect())
    if self.Titelbild.state < 0.2 or not self.gamestart:  # freeze wenn die animation im letzten bild ist oder
        #  noch nicht play gedrückt wurde()
        self.Titelbild.draw(self.Titelbild.rect, freeze=True)
    else:
        self.Titelbild.draw(self.Titelbild.rect)
    if self.Titelbild.state < 0.2:  # wenn die animation fertig ist
        self.changeScene("game")  # scene wird gewechselt
    if self.menu:
        self.changeScene("options")

def update(self):
    # zeichnet die gespeicherten objekte der scene für jeden frame auf
    self.screenimage.fill((0, 0, 0))  # Hintergrund füllen
    self.screenimage.blit(self.credits[0], self.credits[1])  # "copyright by temesgen gordon & raphael"
    # bestimmt wann das Titelbild gefreezed sein soll und wann nicht
    for button in self.buttons.values():
        self.screenimage.blit(button.get_currentframe(), button.rep)

def key_press_handler(self, key_pressed):
    pass

def event_handler(self, event):  # pro frame aufgerufen
    if event.type == self.eQUITBUTTON:  # Event: wenn der Quitbutton gedrückt wurde
        exit()
    elif event.type == self.ePLAYBUTTON:  # Event: wenn der Playbutton gedrückt wurde
        self.gamestart = True  # spielstartet
    elif event.type == self.eOPTIONBUTTON:  
        self.menu = True       # Menü öffnet sich
    else:
        for button in self.buttons.values():
            button.event_handler(event, self)

def collision_detection(self):
    pass

def changeScene(self, scenename):
    if scenename == "game":
        Bomberman.currentscene = InGameScene(nOfPlayers=2)  # die GameScene wird geladen, man kann mit "nOfPlayers" und
    elif scenename == "options":
        Bomberman.currentscene = SettingsScene() 
    # "nOfEnemies" angeben wie viele Player und gegner erstellt werden sollen

    
