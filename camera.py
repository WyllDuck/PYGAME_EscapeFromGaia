# Tools
import pygame as py

# Configuration: 
import conf

class Camera (object):
    def __init__ (self, width, height):
        self.camera = py.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    
    # Apply mouvement from target: 
    def apply (self, entity):
        return entity.rect.move(self.camera.topleft)
    
    # Change the value of the tiles:
    def update (self, target):
        x = - target.rect.x + int(conf.screen_size[0] / 2)
        y = - target.rect.y + int(conf.screen_size[1] / 2)
        self.camera = py.Rect(x, y, self.width, self.height)