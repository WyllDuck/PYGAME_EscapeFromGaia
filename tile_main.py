# Tools
import pygame as py

# Configuration: 
import conf

class Tile (py.sprite.Sprite):
    def __init__ (self, image):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()


class TileMiniMap (py.sprite.Sprite):
    def __init__ (self, image):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()


class UserMiniMap (py.sprite.Sprite):
    def __init__ (self, image):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

    # Update position of user in minimap
    def update (self, pos):
        # Note: "col" and "row" are inverted in Pygame in reference to Numpy
        col, row = pos
        col = col // conf.tile_size
        row = row // conf.tile_size
        self.rect.center = (col * conf.tile_size_mini_map + conf.position_mini_map[0], row * conf.tile_size_mini_map + conf.position_mini_map[1])


class Door (py.sprite.Sprite):
    def __init__ (self, image):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.status = 'close'

    def change_status(self, image):
        self.image = py.image.load(image).convert_alpha()


class Lifebar (py.sprite.Sprite):
    def __init__ (self, image):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = conf.position_lifebar

    def update (self, damage = 1):
         self.rect = self.rect.move( -damage, 0)


class LifebarBackground (py.sprite.Sprite):
    def __init__ (self, image):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = conf.position_lifebar_background