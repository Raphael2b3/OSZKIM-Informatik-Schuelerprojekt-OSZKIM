from Classes.Bomberman import *
from Classes.GUIElements.Button import Button
from Classes.GUIElements.Animation import Animation
from Classes.Scenes.InGameScene import InGameScene


  

# MainMenuScene
class SettingsScene:
    #  events der scene
    ePLAYERNO   = p.USEREVENT + 1
    eSOUND      = p.USEREVENT + 2
    #eBACKBUTTON = p.USEREVENT + 3
    #ePLAYERNO_1 = p.USEREVENT + 4
    #ePLAYERNO_2 = p.USEREVENT + 5
    #ePLAYERNO_3 = p.USEREVENT + 6
    #ePLAYERNO_4 = p.USEREVENT + 7

    pPLAYNOM = "Assets/Scam/option1.png"
    
    pSOUNDBTN_MO = "Assets/Scam/option2.png"
    pSOUNDBTN = "Assets/Scam/option2.png"
    
    #p.BACKBTN_MO = "Assets/Buttons/Play/###"
    #p.BACKBTN = "Assets/Buttons/Play/###"
    
    #p.PLAYERNO1_MO = "Assets/Buttons/Play/###"
    #p.PLAYERNO1 = "Assets/Buttons/Play/###"
    
    #p.PLAYERNO2_MO = "Assets/Buttons/Play/###"
    #p.PLAYERNO2 = "Assets/Buttons/Play/###"
    
    #p.PLAYERNO3_MO = "Assets/Buttons/Play/###"
    #p.PLAYERNO3 = "Assets/Buttons/Play/###"
    
    #p.PLAYERNO4_MO = "Assets/Buttons/Play/###"
    #p.PLAYERNO4 = "Assets/Buttons/Play/###" 
    buttons = {}

    def __init__(self):
        self.screenimage = p.surface.Surface(p.display.get_window_size())

        # buttons
        self.buttons["sound"] = Button(self.pSOUNDBTN_MO, self.pSOUNDBTN, Bomberman.screensize[0] / 2, 450,
                                      self.eSOUND)
        self.buttons["playernumber"] = Button(self.pPLAYNOM, self.pPLAYNOM, Bomberman.screensize[0] / 2, 650, self.ePLAYERNO)
        
        #self.buttons["back"] = Button(self.pBACKBTN_MO, self.pBACKBTN, Bomberman.screensize[0] / 2, 650,
                                        #self.eBACKBUTTON)
        #self.buttons["playerno.1"] = Button(self.pPLAYERNO_1MO, self.pPLAYERNO1, Bomberman.screensize[0] / 2, 650,
                                        #self.ePLAYERNO1)
        #self.buttons["playerno.2"] = Button(self.pPLAYERNO_2MO, self.pPLAYERNO2, Bomberman.screensize[0] / 2, 650,
                                        #self.ePLAYERNO2)
        #self.buttons["playerno.3"] = Button(self.pPLAYERNO_3MO, self.pPLAYERNO3, Bomberman.screensize[0] / 2, 650,
                                        #self.ePLAYERNO3)
        #self.buttons["playerno.1"] = Button(self.pPLAYERNO_4MO, self.pPLAYERNO4, Bomberman.screensize[0] / 2, 650,
                                        #self.ePLAYERNO4)
        self.update()

    def draw(self):
        # pro frame aufgerufen
        Bomberman.backgroundcolor = Bomberman.rainbow_fade(Bomberman.backgroundcolor, speed=1, start=122)
        Bomberman.screen.fill(Bomberman.backgroundcolor)

    def update(self):
        # zeichnet die gespeicherten objekte der scene für jeden frame auf
        self.screenimage.fill((0, 0, 0))  # Hintergrund füllen
        # bestimmt wann das Titelbild gefreezed sein soll und wann nicht
        for button in self.buttons.values():
            self.screenimage.blit(button.get_currentframe(), button.rep)

    def key_press_handler(self, key_pressed):
        pass

    def event_handler(self, event):  # pro frame aufgerufen
        pass

    def collision_detection(self):
        pass

    def changeScene(self):
        pass
        #Bomberman.currentscene = InGameScene(nOfPlayers=2)  # die GameScene wird geladen, man kann mit "nOfPlayers" und
        # "nOfEnemies" angeben wie viele Player und gegner erstellt werden sollen