# Tools
import pygame as py
from math import sqrt, atan, pi, cos, sin
import time
import numpy as np
from scipy.interpolate import interp1d
import uuid
import networkx as nx
import random as rd

#Configuration
import conf

# Others:
import sprite_sheets
from weapon import Weapon


class Enemy(py.sprite.Sprite):

    # Inicialitza els states. Són nombres enters.
    STOP, PATROL, ATTACK, FOLLOW, WAITING, DEAD, DAMAGE = range(7)

    def __init__(self, image_matrix, pos, _map, M_Graph, params, doors):
        super().__init__()

        # General Parameters:
        self._id = uuid.uuid4()
        self.state = np.random.choice([self.PATROL, self.STOP], p = [0.4, 0.6])
        self.life = params[4]
        self.size = params[5]
        self.desfase = params[6]
        self.doors = doors

        # Varables enemy image:
        self.matrix = image_matrix
        self.count = 0
        self.nframes = len(self.matrix[0])
        self.image = py.transform.rotozoom(self.matrix[self.state][0], rd.randrange(0,360) + self.desfase, 1)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.dead_state_update = True
        self.damage_animation_count = 0

        # Varables for enemy paths:
        self.curved_coord = None
        self._map = _map
        self.M_Graph = M_Graph
        self.velocity = params[1] # default => 17
        self.follow_perimeter = params[3]
        self.follow_perimeter_secondary = params[7]

        # Variables for enemy weapons:
        self.attack_spam = time.time()
        self.first = True
        self.selected_weapon = params[0]
        self.attack_perimeter = params[2]
        self.weapon = conf.weapon_dict[ self.selected_weapon ]


    def update(self, user_pos, enemies_pos):

        perimeter = lambda x, y: (x - door.rect.center[1] )**2 + (y - door.rect.center[0] )**2

        for door in self.doors:
            # Open the door:
            if perimeter(self.rect.center[1], self.rect.center[0]) <= ( 1 * conf.tile_size ) ** 2:
                door.change_status(conf.door_open_image)
                self._map[ door.rect.center[1] // conf.tile_size, door.rect.center[0] // conf.tile_size ] = 0
                door.status = 'open'
                break

        # Note: Future use in enemy path finding logic
        self.user_pos = user_pos

        # Enemy sprite logic:
        self.count = self.count + 1
        if self.count == self.nframes * 10:
            self.count = 0

        # Looking for the new enemy state
        self.change_state( user_pos )

        row = self.state
        col = self.count // 10

        #####################
        #   DAMAGE STATE
        #####################

        if self.state == self.DAMAGE:

            self.damage_animation_count += 1
            row = self.state

            # Rotate Image:
            angle_deg, angle_rad = self.get_angle(user_pos)
            self.image = py.transform.rotozoom(self.matrix[row][col], angle_deg + self.desfase, 1)

            # Note: The enemy rotates around the same point as the old rect
            self.rect = self.image.get_rect(center=self.rect.center)

            if self.damage_animation_count > 8:
                self.state = self.ATTACK
                self.damage_animation_count = 0

            # While the enemy is been attacked he's allowed to defend himself
            # Verify if there is any object in the way: (obstacles, walls, enemies):
            if self.object_in_the_way(user_pos):

                # Fisrt Shot:
                if self.first:
                    self.first = False
                    self.attack_spam = time.time()

                    angle_deg, angle_rad = self.get_angle(user_pos)

                    return Weapon(self.weapon['matrix'], self.rect.center, self._map, [ self.weapon['velocity'], self.weapon['size'], [angle_deg, angle_rad], self.weapon['dispersion'], self.weapon['damage'], self.weapon['damage_end'] ], self._id)

                # Next Shot
                elif time.time() - self.attack_spam >= self.weapon['time_spam']:
                    self.attack_spam = time.time()

                    angle_deg, angle_rad = self.get_angle(user_pos)

                    return Weapon(self.weapon['matrix'], self.rect.center, self._map, [ self.weapon['velocity'], self.weapon['size'], [angle_deg, angle_rad], self.weapon['dispersion'], self.weapon['damage'], self.weapon['damage_end'] ], self._id)




        #####################
        #   DEAD STATE
        #####################

        elif self.state == self.DEAD and self.dead_state_update:

            # Rotate Image:
            angle_deg, angle_rad = self.get_angle(user_pos)
            self.image = py.transform.rotozoom(self.matrix[row][col], angle_deg + self.desfase, 1)

            # Note: The enemy rotates around the same point as the old rect
            self.rect = self.image.get_rect(center=self.rect.center)

            # Do not change angle ever again.
            self.dead_state_update = False


        #####################
        #   FOLLOW STATE
        #####################

        elif self.state == self.FOLLOW:

            if not self.curved_coord:

                # Calcule ""from"" and ""_to"":
                _from = [ coord // conf.tile_size for coord in self.rect.center][::-1]
                _to =  [ coord // conf.tile_size for coord in user_pos][::-1]

                # Replace ""_to"" by the last ""_to"" position known
                if  _to not in self.M_Graph:
                    _to = self._to

                try:
                    self.path = self.M_Graph.find_path(_from, _to)[:4]
                    self.curved_coord = self.get_curved_path()
                    self._to = _to
                except:
                    return None
                    #self.curved_coord = [tuple(coord / conf.tile_size for coord in self.rect.center)]

            self.next_pos = self.curved_coord.pop(0)
            self.next_pos = [coord * conf.tile_size for coord in self.next_pos][::-1]

            # Rotate Image:
            angle_deg, angle_rad = self.get_angle(user_pos)
            self.image = py.transform.rotozoom(self.matrix[row][col], angle_deg + self.desfase, 1)

            # Note: The enemy rotates around the same point as the old rect
            self.rect = self.image.get_rect(center=self.rect.center)

            # Taking into account only the ennemies with more privileges than the current enemy were are studying:
            self.privilege = [item[0] for item in enemies_pos].index(self._id)

            # Note: If no other enemy is in the position then:
            if not any( self.action(self.next_pos, enemy[1], enemy[2]) for enemy in enemies_pos[:self.privilege] if enemy[0] != self._id):

                # No checking for collision is required because the enemy path is already taken from a none collision path function
                col_add, row_add = ( self.next_pos[0] - self.rect.center[0], self.next_pos[1] - self.rect.center[1])
                self.rect = self.rect.move(col_add, row_add)

            # Someone in position already rerun secuence:
            else:
                self.state = self.WAITING

            # While the enemy is moving he will be allowed to defend himself
            # Note: Because of the movement of the enemy the shots will take longer
            if self.object_in_the_way(user_pos):

                # Fisrt Shot:
                if self.first:
                    self.first = False
                    self.attack_spam = time.time()

                    angle_deg, angle_rad = self.get_angle(user_pos)

                    return Weapon(self.weapon['matrix'], self.rect.center, self._map, [ self.weapon['velocity'], self.weapon['size'], [angle_deg, angle_rad], self.weapon['dispersion'], self.weapon['damage'], self.weapon['damage_end'] ], self._id)

                # Next Shot
                elif time.time() - self.attack_spam >= self.weapon['time_spam'] + conf.enemy_movement_penalty:
                    self.attack_spam = time.time()

                    angle_deg, angle_rad = self.get_angle(user_pos)

                    return Weapon(self.weapon['matrix'], self.rect.center, self._map, [ self.weapon['velocity'], self.weapon['size'], [angle_deg, angle_rad], self.weapon['dispersion'], self.weapon['damage'], self.weapon['damage_end'] ], self._id)



        #####################
        #   WAITING STATE
        #####################

        elif self.state == self.WAITING:

            # Rotate Image:
            angle_deg, angle_rad = self.get_angle(user_pos)
            self.image = py.transform.rotozoom(self.matrix[row][col], angle_deg + self.desfase, 1)

            # Note: The enemy rotates around the same point as the old rect
            self.rect = self.image.get_rect(center=self.rect.center)

            # Note: If no other enemy is in the position then:
            if not any( self.action(self.next_pos, enemy[1], enemy[2]) for enemy in enemies_pos[:self.privilege] if enemy[0] != self._id):

                # No checking for collision is required because the enemy path is already taken from a none collision path function
                col_add, row_add = ( self.next_pos[0] - self.rect.center[0], self.next_pos[1] - self.rect.center[1])
                self.rect = self.rect.move(col_add, row_add)
                self.state = self.FOLLOW

            # Someone in position already rerun secuence:
            else:
                self.state = self.WAITING


        #####################
        #   ATTACK STATE
        #####################

        elif self.state == self.ATTACK:

            # Rotate Image:
            angle_deg, angle_rad = self.get_angle(user_pos)
            self.image = py.transform.rotozoom(self.matrix[row][col], angle_deg + self.desfase, 1)

            # Note: The enemy rotates around the same point as the old rect
            self.rect = self.image.get_rect(center=self.rect.center)

            # Verify if there is any object in the way: (obstacles, walls, enemies):
            if self.object_in_the_way(user_pos):

                # Fisrt Shot:
                if self.first:
                    self.first = False
                    self.attack_spam = time.time()

                    angle_deg, angle_rad = self.get_angle(user_pos)

                    return Weapon(self.weapon['matrix'], self.rect.center, self._map, [ self.weapon['velocity'], self.weapon['size'], [angle_deg, angle_rad], self.weapon['dispersion'], self.weapon['damage'], self.weapon['damage_end'] ], self._id)

                # Next Shot
                elif time.time() - self.attack_spam >= self.weapon['time_spam']:
                    self.attack_spam = time.time()

                    angle_deg, angle_rad = self.get_angle(user_pos)

                    return Weapon(self.weapon['matrix'], self.rect.center, self._map, [ self.weapon['velocity'], self.weapon['size'], [angle_deg, angle_rad], self.weapon['dispersion'], self.weapon['damage'], self.weapon['damage_end'] ], self._id)


        #####################
        #   PATROL STATE
        #####################

        elif self.state == self.PATROL:

            if not self.curved_coord:

                # Calcule ""from"" and ""_to"":
                _from = [ coord // conf.tile_size for coord in self.rect.center][::-1]
                _to = rd.choice(list(self.M_Graph.M.neighbors( self.M_Graph._map_list[_from[0]][_from[1]] ) ) )
                _to = rd.choice(list(self.M_Graph.M.neighbors( self.M_Graph._map_list[_to.row][_to.col] ) ) )
                _to = rd.choice(list(self.M_Graph.M.neighbors( self.M_Graph._map_list[_to.row][_to.col] ) ) )

                try:
                    self.path = self.M_Graph.find_path(_from, _to)[:4]
                    self.curved_coord = self.get_curved_path()
                    self._to = _to
                except:
                    return None
                    #self.curved_coord = [tuple(coord / conf.tile_size for coord in self.rect.center)]

            self.next_pos = self.curved_coord.pop(0)
            self.next_pos = [coord * conf.tile_size for coord in self.next_pos][::-1]

            # Rotate Image:
            angle_deg, angle_rad = self.get_angle(self.next_pos)
            self.image = py.transform.rotozoom(self.matrix[row][col], angle_deg + self.desfase, 1)

            # Note: The enemy rotates around the same point as the old rect
            self.rect = self.image.get_rect(center=self.rect.center)

            # No checking for collision is required because the enemy path is already taken from a none collision path function
            col_add, row_add = ( self.next_pos[0] - self.rect.center[0], self.next_pos[1] - self.rect.center[1])
            self.rect = self.rect.move(col_add, row_add)


    """
    Check for object in the way of two points:
    """
    def object_in_the_way (self, user_pos):

        # Get points:
        _from = [ coord // conf.tile_size for coord in self.rect.center][::-1]
        _to =  [ coord // conf.tile_size for coord in user_pos][::-1]

        try:
            lenght = nx.shortest_path_length(self.M_Graph.M, source=self.M_Graph._map_list[_from[0]][_from[1]], target=self.M_Graph._map_list[_to[0]][_to[1]], weight='weight')
        except:
            return False

        # Get ideal lenght between the two points
        row_1, col_1 = _from
        row_2, col_2 = _to

        # Execption cases:
        if row_1 == row_2:
            appro_lenght = (col_1 - col_2) * (1 / sqrt(2))
            return appro_lenght == lenght

        if col_1 == col_2:
            appro_lenght = (row_1 - row_2) * (1 / sqrt(2))
            return appro_lenght == lenght

        rows = (row_1, row_2)
        cols = (col_1, col_2)

        if abs((row_1 - row_2) / (col_1 - col_2)) > 1:
            row_1 = cols[0]; row_2 = cols[1]
            col_2 = rows[0]; col_2 = rows[1]

        rows = (row_1, row_2)
        cols = (col_1, col_2)

        row_1 = min(rows)
        col_1 = min(cols)

        row_2 = max(rows)
        col_2 = max(cols)

        appro_lenght = abs(row_1 - row_2) * 1 + abs(abs(col_2 - col_1) - abs(row_1 - row_2)) * (1 / sqrt(2))

        return appro_lenght == lenght


    def change_state(self, user_pos):

        old_state = self.state

        if self.life <= 0 and self.dead_state_update:
                self.state = self.DEAD

        # Basic mouvement:
        elif self.state == self.PATROL:
            if self.action(user_pos, self.rect.center, self.follow_perimeter * conf.tile_size):
                if self.object_in_the_way(user_pos):
                    self.state = self.FOLLOW
            if self.action(user_pos, self.rect.center, self.follow_perimeter_secondary * conf.tile_size):
                self.state = self.FOLLOW

        elif self.state == self.STOP:
            if self.action(user_pos, self.rect.center, self.follow_perimeter * conf.tile_size):
                if self.object_in_the_way(user_pos):
                    self.state = self.FOLLOW
            if self.action(user_pos, self.rect.center, self.follow_perimeter_secondary * conf.tile_size):
                self.state = self.FOLLOW

        elif self.state == self.FOLLOW:
            if self.action(user_pos, self.rect.center, self.attack_perimeter * conf.tile_size):
                self.state = self.ATTACK
            if not self.action(user_pos, self.rect.center, self.follow_perimeter * 1.4 * conf.tile_size):
                self.state =  np.random.choice([self.PATROL, self.STOP], p = [0.4, 0.6])

        elif self.state == self.ATTACK:
            if not self.action(user_pos, self.rect.center, self.attack_perimeter * conf.tile_size):
                self.state = self.FOLLOW

        elif self.state == self.WAITING:
            pass # Waiting the more privileged enemies to move

        elif self.state == self.DEAD:
            pass # You are dead you cannot move or do anything

        elif self.state == self.DAMAGE:
            pass

        else:
            raise ValueError('Transició {} desconeguda'.format(transicio))

        # Set counter to 0:
        if self.state != old_state:
            self.count = 0


    """
    Returns True is "user" in sight of "enemy" in the caseof the "follow" state
    Returns True is "user" in attack zone of "enemy" in the caseof the "attack" state
    """
    def action (self, user_pos, cercle_detection, cercle_perimeter):

        # Position enemy sight
        cercle_row, cercle_col = cercle_detection

        perimeter = lambda x, y: (x - cercle_row )**2 + (y - cercle_col )**2

        return perimeter(user_pos[0], user_pos[1]) <= ( cercle_perimeter ) ** 2


    """
    Get angle between user and enemy
    """
    def get_angle(self, user_pos):
        # Lenght of triangle sides:
        opp = ( user_pos[1] - self.rect.center[1] )
        adj = ( user_pos[0] - self.rect.center[0] )

        # Handle indeterminations of "tan" function:
        try:
            angle = atan( abs( opp / adj ) )

            # left / bottom:
            if adj < 0 and opp >= 0:
                angle = angle + pi

            # right / bottom:
            elif adj > 0 and opp >= 0:
                angle = abs(angle - pi/2) + 1.5 * pi

            # left / top:
            elif adj < 0 and opp < 0:
                angle = abs(angle - pi/2) + 0.5 * pi

            # right / top:
            elif adj > 0 and opp < 0:
                pass

        except:
            if adj == 0 and opp >= 0:
                angle = pi * 1.5
            elif adj == 0 and opp < 0:
                angle = pi * .5

        return (angle * (360/(2*pi)), angle)


    """
    Get the path in multiple points and a curved direction
    """
    def get_curved_path (self):
        pts = np.array(self.path)
        x, y = pts.T
        i = np.arange(len(pts))

        # 5x the original number of points
        interp_i = np.linspace(0, i.max(), self.velocity * i.max())

        xi = interp1d(i, x, kind='cubic')(interp_i)
        yi = interp1d(i, y, kind='cubic')(interp_i)

        return list(zip(xi, yi))
