# Tools
import pygame as py
from pygame.locals import *
from pgu import engine

# Configuration:
import conf
import sprite_sheets

# Others:
from sprites_menu import Background, Button, Title, MuteUnmute, SecondaryBackground, SecondaryButton


####################################
#           MENU
####################################

class Menu (engine.State):

    def init(self):

        # Background:
        self.background = Background( conf.background_menu_image )

        # Background Title:
        self.title = Title( conf.background_menu_title_image, conf.position_menu_title )

        # Button Group:
        self.button_group = py.sprite.Group()

        # Buttons:
        self.start = Button( conf.start_image if self.game.first_init else conf.secondary_background_continue_image, conf.position_start, 'START'  )
        self.button_group.add(self.start)
        self.controls = Button( conf.controls_image, conf.position_controls, 'CONTROLS' )
        self.button_group.add(self.controls)
        self.settings = Button( conf.settings_image, conf.position_settings, 'SETTINGS' )
        self.button_group.add(self.settings)
        self.quit = Button( conf.quit_image, conf.position_quit, 'QUIT' )
        self.button_group.add(self.quit)

    # Paint Screen
    def paint(self,screen):
        self.update(screen)

    # Handle User Actions
    def event(self,event):

        # Note: 1 == LEFT button in mouse
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            mouse = py.mouse.get_pos()
            for button in self.button_group:
                if button.click( mouse ):
                    if button.name == 'QUIT':
                        exit()
                    else:
                        self.game.first_init = False
                        return self.game.change_state(button.name)

    # Update Screen
    def loop(self):

        # Button Group:
        self.button_group.update()

        # Title:
        self.title.update()

    # Update Screen
    def update(self,screen):

        # Background:
        screen.blit(self.background.image, self.background.rect)
        screen.blit(self.title.image, self.title.rect)

        # Button Group:
        self.button_group.draw(screen)

        py.display.flip()


####################################
#       SETTINGS SCREEN
####################################

class Settings (engine.State):

    def init(self):

        # Background:
        self.background = Background( conf.background_settings_image )

        # Buttons:
        self.mute_unmute = MuteUnmute( conf.mute_image, conf.unmute_image, conf.position_mute_unmute )

    # Paint Screen
    def paint(self,screen):
        self.update(screen)

    # Handle User Actions
    def event(self,event):
        if event.type == KEYDOWN and event.key == py.K_ESCAPE:
            return self.game.change_state()

        # Note: 1 == LEFT button in mouse
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            if self.mute_unmute.click( py.mouse.get_pos() ):
                conf.sound = not conf.sound

    # Update Screen
    def loop(self):
        return

    # Update Screen
    def update(self,screen):

        # Background:
        screen.blit(self.background.image, self.background.rect)

        # Button:
        screen.blit(self.mute_unmute.image, self.mute_unmute.rect)

        py.display.flip()


####################################
#     YOU ARE DEAD! / SCREEN
####################################

class DeadScreen (engine.State):

    def init(self):

        # Secondary Background:
        self.secondaryBackground = SecondaryBackground( conf.dead_screen_image, conf.dead_screen_position )

        # Button Group:
        self.button_group = py.sprite.Group()

        # Buttons:
        self.restart = SecondaryButton( conf.secondary_background_restart_image, conf.dead_screen_restart_position, 'RESTART' )
        self.button_group.add(self.restart)
        self.menu = SecondaryButton( conf.secondary_background_menu_image, conf.dead_screen_menu_position, 'MENU' )
        self.button_group.add(self.menu)

    # Paint Screen
    def paint(self,screen):
        self.update(screen)

    # Handle User Actions
    def event(self,event):

        # Note: 1 == LEFT button in mouse
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            mouse = py.mouse.get_pos()
            for button in self.button_group:
                if button.click( mouse ):
                    return self.game.change_state(button.name)

    # Update Screen
    def loop(self):
        return

    # Update Screen
    def update(self,screen):

        # Secondary Background:
        screen.blit(self.secondaryBackground.image, self.secondaryBackground.rect)

        # Button Group:
        for sprite in self.button_group:
            screen.blit(sprite.image, sprite.rect)

        py.display.flip()


####################################
#       CONTROLS SCREEN
####################################

class Controls (engine.State):

    def init(self):

        # Background:
        self.background = Background( conf.background_controls_image )

    # Paint Screen
    def paint(self,screen):
        self.update(screen)

    # Handle User Actions
    def event(self,event):
        if event.type == KEYDOWN and event.key == py.K_ESCAPE:
            return self.game.change_state()

    # Update Screen
    def loop(self):
        return

    # Update Screen
    def update(self,screen):

        # Background:
        screen.blit(self.background.image, self.background.rect)

        py.display.flip()


####################################
#       LOADING SCREEN
####################################

class Loading (engine.State):

    def init(self):

        # Background:
        self.background = Background( conf.background_loading_image[0] )

    # Paint Screen
    def paint(self,screen):
        self.update(screen)

    # Handle User Actions
    def event(self,event):
        if event.type == KEYDOWN and event.key == py.K_SPACE:
            return self.game.change_state()

    # Update Screen
    def loop(self):
        return

    # Update loading image backgroud:
    def update_loading(self, count):
        self.background = Background( conf.background_loading_image[count] )

    # Update Screen
    def update(self,screen):

        # Background:
        screen.blit(self.background.image, self.background.rect)

        py.display.flip()


####################################
#       PAUSE SCREEN
####################################

class Pause(engine.State):

    def init(self):

        # Secondary Background:
        self.secondaryBackground = SecondaryBackground( conf.secondary_background_image, conf.secondary_background_position )

        # Button Group:
        self.button_group = py.sprite.Group()

        # Buttons:
        self._continue = SecondaryButton( conf.secondary_background_continue_image, conf.secondary_background_continue_position, 'CONTINUE' )
        self.button_group.add(self._continue)
        self.restart = SecondaryButton( conf.secondary_background_restart_image, conf.secondary_background_restart_position, 'RESTART' )
        self.button_group.add(self.restart)
        self.menu = SecondaryButton( conf.secondary_background_menu_image, conf.secondary_background_menu_position, 'MENU' )
        self.button_group.add(self.menu)
        self.quit = SecondaryButton( conf.quit_image, conf.secondary_background_quit_position, 'QUIT' )
        self.button_group.add(self.quit)

    # Paint Screen
    def paint(self,screen):
        self.update(screen)

    # Handle User Actions
    def event(self,event):

        # Note: 1 == LEFT button in mouse
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            mouse = py.mouse.get_pos()
            for button in self.button_group:
                if button.click( mouse ):
                    if button.name == 'QUIT':
                        exit()
                    else:
                        return self.game.change_state(button.name)

        # Verify is someone clicks the PAUSE KEY / P or ESC :SecondaryButton
        if event.type == KEYDOWN:
            if event.key == py.K_ESCAPE:
                return self.game.change_state('CONTINUE')

    # Update Screen
    def loop(self):

        # Button Group:
        self.button_group.update()

    # Update Screen
    def update(self,screen):

        # Secondary Background:
        screen.blit(self.secondaryBackground.image, self.secondaryBackground.rect)

        # Button Group:
        for sprite in self.button_group:
            screen.blit(sprite.image, sprite.rect)

        py.display.flip()
