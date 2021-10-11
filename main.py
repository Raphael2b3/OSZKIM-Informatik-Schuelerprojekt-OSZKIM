from Classes.Bomberman import *
from Classes.Scenes.MainMenuScene import MainMenuScene


def controls_events():
    keys_pressed = p.key.get_pressed()
    Bomberman.currentscene.key_press_handler(keys_pressed)

    events = p.event.get()
    for event in events:
        if event.type == p.QUIT:
            exit()
        else:
            Bomberman.currentscene.event_handler(event)

    Bomberman.currentscene.collision_detection()


def render():
    Bomberman.currentscene.draw()
    p.display.update()


Bomberman.currentscene = MainMenuScene()

while True:
    Bomberman.clock.tick(Bomberman.fps)
    controls_events()
    render()
