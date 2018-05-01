# Tools
import pygame as py
from math import sqrt, atan, pi, cos, sin
import random as rd

#Configuration
import conf

class Weapon(py.sprite.Sprite):

    TRAVELLING, HIT = range(2)

    def __init__(self, image_matrix, pos, _map, params):
        super().__init__()
        
        self.state = self.TRAVELLING

        self.matrix = image_matrix
        self.count = 0
        self.nframes = len(self.matrix[0])
        
        self.image = self.matrix[self.state][0]
        self.rect = self.image.get_rect().move(pos)
        self._map = _map

        self.velocity = params[0]
        self.weapon_size = params[1]
        self.angles = params[2]
        self.dispersion = params[3]

        self.dispersion = rd.randrange( -self.dispersion, self.dispersion + 1)


    def check_collision (self, dir):
        # Note: col and row are inverted in the numpy map in respect to pygame
        col, row = self.rect.center
        col_add_map, row_add_map = dir

        # Conditions: 
        cond_0 = self._map[int((row + row_add_map + (self.weapon_size[0] + conf.tile_size) / 2) // conf.tile_size), int((col + col_add_map + (self.weapon_size[1] + conf.tile_size) / 2) // conf.tile_size)]
        cond_1 = self._map[int((row + row_add_map + (self.weapon_size[0] + conf.tile_size) / 2) // conf.tile_size), int((col + col_add_map - (self.weapon_size[1] - conf.tile_size) / 2) // conf.tile_size)]
        cond_2 = self._map[int((row + row_add_map - (self.weapon_size[0] - conf.tile_size) / 2) // conf.tile_size), int((col + col_add_map + (self.weapon_size[1] + conf.tile_size) / 2) // conf.tile_size)]
        cond_3 = self._map[int((row + row_add_map - (self.weapon_size[0] - conf.tile_size) / 2) // conf.tile_size), int((col + col_add_map - (self.weapon_size[1] - conf.tile_size) / 2) // conf.tile_size)]
        
        return any((cond_0, cond_1, cond_2, cond_3)) 


    def update(self):
        self.count = self.count + 1

        # Detect End of cycle:
        if self.count == self.nframes * 10 and self.state == self.HIT:
            return True

        elif self.count == self.nframes * 10:
            self.count = 0

        row = self.state
        col = self.count // 10        
        
        angle_deg, angle_rad = self.angles

        # Applying Dispersion:
        if self.dispersion:
            angle_deg = angle_deg + self.dispersion
            angle_rad = angle_rad + self.dispersion * ( (2 * pi) / 360 )

        # Rotate Image:
        self.image = py.transform.rotozoom(self.matrix[row][col], angle_deg, 1)
        # Note: The Weapon rotates around the same point as the old rect
        self.rect = self.image.get_rect(center=self.rect.center)

        # Mouvement forward of the Weapon:
        if self.state == self.TRAVELLING:
            col_add, row_add = ( cos( angle_rad ) * self.velocity, - sin( angle_rad ) * self.velocity )

            # Checking for collision:
            if not self.check_collision((col_add, row_add)):
                self.rect = self.rect.move(col_add, row_add)
            else:
                self.state = self.HIT

        # Hit a wall:
        elif self.state == self.HIT:
            pass
        
        # Error:
        else:
            raise ValueError('State Unknow')


class MiniatureWeapon (py.sprite.Sprite):
    def __init__ (self, _dict):
        super().__init__()
        self.image = py.image.load( _dict['miniature'] ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = conf.position_miniature
        self._dict = _dict

    def __eq__ (self, other):
        return self._dict == other
