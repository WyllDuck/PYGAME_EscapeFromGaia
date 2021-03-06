# Tools:
import pygame as py
from pygame.locals import *
from pgu import engine

# Configuration:
import conf

# Others:
from other_states import Menu, DeadScreen, Settings, Loading, Controls, Pause
from gaming_state import Gaming

# Class Game
class Game(engine.Game):

    def __init__(self):
        super().__init__()
        self.screen = py.display.set_mode(conf.screen_size, SWSURFACE)
        self.crono = py.time.Clock()
        self._init_state_machine()
        self.count = 0

    # Creates and stores all states as attributes
    def _init_state_machine(self):

        self.first_init = True

        self.MENU = Menu(self)
        self.GAMING = Gaming(self)
        self.LOADING = Loading(self)
        self.DEADSCREEN = DeadScreen(self)
        self.CONTROLS = Controls(self)
        self.SETTINGS = Settings(self)
        self.PAUSE = Pause(self)
        self.FINAL = Loading(self)

    # Calls the main loop with the initial state.
    def run(self):
        super().run(self.MENU, self.screen)

    # Tick is called once per frame. It shoud control de timing.
    def tick(self):
        self.crono.tick(conf.fps)   # Limits the maximum FPS

    # New State on the game
    def change_state(self, transition = None):

        # Menu releated States
        if self.state is self.MENU and transition == 'START':
            new_state = self.LOADING
            self.LOADING.update_loading(self.count)

        elif self.state is self.MENU and transition == 'CONTROLS':
            new_state = self.CONTROLS
        elif self.state is self.MENU and transition == 'SETTINGS':
            new_state = self.SETTINGS

        # Gaming releated states:
        elif self.state is self.GAMING and transition == 'GAMEOVER':
            new_state = self.DEADSCREEN
            self.count = 0
        elif self.state is self.GAMING and transition == 'PAUSE':
            new_state = self.PAUSE
        elif self.state is self.GAMING and transition == 'NEXT_LEVEL':
            new_state = self.LOADING
            self.count += 1
            self.LOADING.update_loading(self.count)
        elif self.state is self.GAMING and transition == 'MISSION_ACCOMPLISHED':
            new_state = self.FINAL
            self.first_init = True
            self.FINAL.update_loading(self.count)

        # Loading releated states:
        elif self.state is self.LOADING:
            new_state = self.GAMING
            self.GAMING.init()

        # Final releated states:
        elif self.state is self.FINAL:
            new_state = self.MENU
            self.count = 0
            self.MENU.init()

        # Pause releated states:
        elif self.state is self.PAUSE and transition == 'CONTINUE':
            new_state = self.GAMING
        elif self.state is self.PAUSE and transition == 'RESTART':
            new_state = self.LOADING
            self.count = 0
            self.LOADING.update_loading(self.count)
        elif self.state is self.PAUSE and transition == 'MENU':
            new_state = self.MENU
            self.MENU.init()

        # Controls releated states:
        elif self.state is self.CONTROLS:
            new_state = self.MENU

        # Settings releated states:
        elif self.state is self.SETTINGS:
            new_state = self.MENU

        # Dead Screen releated states:
        elif self.state is self.DEADSCREEN and transition == 'RESTART':
            new_state = self.LOADING
            self.LOADING.update_loading(self.count)
        elif self.state is self.DEADSCREEN and transition == 'MENU':
            new_state = self.MENU

        else:
            raise ValueError ('Unknow state or transition')

        print('number of levels pass: {}'.format(self.count))

        return new_state


# Main Program
def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
