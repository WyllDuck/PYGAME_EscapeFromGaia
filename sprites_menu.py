# Tools:
import pygame as py

# Configuration:
import conf


class Background (py.sprite.Sprite):
    def __init__ (self, image):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)

class Button (py.sprite.Sprite):
    def __init__ (self, image, pos, name):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.name = name

    # Verify if the button has been click:
    def click (self, mouse):
        if self.rect.topleft[0] <= mouse[0] and mouse[0] <= self.rect.topleft[0] + conf.size_button_menu[0] and self.rect.topleft[1] <= mouse[1] and mouse[1] <= self.rect.topleft[1] + conf.size_button_menu[1]:
            return True
        else:
            return False

# Note: The only diference between  the two Buttons is the position of the rect
class SecondaryButton (py.sprite.Sprite):
    def __init__ (self, image, pos, name):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.name = name

    # Verify if the button has been click:
    def click (self, mouse):
        if self.rect.topleft[0] <= mouse[0] and mouse[0] <= self.rect.topleft[0] + conf.size_button_menu[0] and self.rect.topleft[1] <= mouse[1] and mouse[1] <= self.rect.topleft[1] + conf.size_button_menu[1]:
            return True
        else:
            return False


class Title (py.sprite.Sprite):
    def __init__ (self, image, pos):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update (self):
        return

        # Note: Try to make a title in movement

class MuteUnmute (py.sprite.Sprite):
    def __init__ (self, mute_image, unmute_image, pos):
        super().__init__()
        self.images = [mute_image, unmute_image]
        self.count = 0
        self.image = py.image.load(self.images[self.count]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos

    # Verify if the button has been click:
    def click (self, mouse):
        if self.rect.topleft[0] <= mouse[0] and mouse[0] <= self.rect.topleft[0] + conf.size_mute_unmute[0] and self.rect.topleft[1] <= mouse[1] and mouse[1] <= self.rect.topleft[1] + conf.size_mute_unmute[1]:
            return self.change_status()
        else:
            pass

    # Note: This method changes the variable "sound" in the " conf.py " file and the picture also
    def change_status (self):
        if self.count == 0:
            self.count = 1
            self.image = py.image.load(self.images[self.count]).convert_alpha()
        elif self.count == 1:
            self.count = 0
            self.image = py.image.load(self.images[self.count]).convert_alpha()


class SecondaryBackground (py.sprite.Sprite):
    def __init__ (self, image, pos):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
