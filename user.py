# Tools
import pygame as py
from math import sqrt, atan, pi, cos, sin
import time
import uuid

#Configuration
import conf

# Others:
from weapon import Weapon
import sprite_sheets

class Character(py.sprite.Sprite):

    # Inicialitza els estats. Són nombres enters.
    AVALL, ESQUERRA, DRETA, AMUNT, STOP, AMUNT_DRETA, AMUNT_ESQUERRA, AVALL_DRETA, AVALL_ESQUERRA = range(9)
    # Inicialitza les transicions
    VES_AVALL, VES_ESQUERRA, VES_DRETA, VES_AMUNT, VES_STOP, VES_AMUNT_DRETA, VES_AMUNT_ESQUERRA, VES_AVALL_DRETA, VES_AVALL_ESQUERRA = range(9)

    def __init__(self, matriu_imatges, pos, _map, doors):
        super().__init__()
        # Defineix l'estat inicial
        self.estat = self.STOP
        self.llista_im = matriu_imatges
        self.count = 0
        self.nframes = len(self.llista_im[0])
        self.image = self.llista_im[self.estat][0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self._map = _map
        self._id = uuid.uuid4()

        self.velocity = conf.velocity_fast
        self.attack = False
        self.attack_spam = time.time()
        self.first = True
        self.selected_weapon = 0
        self.inventory_weapons = list(conf.weapon_dict.keys())

        self.doors = doors
        self.open = False
        self.life = float(conf.user_life)


    def check_collision (self, dir):
        # Note: col and row are inverted in the numpy map in respect to pygame
        col, row = self.rect.center
        col_add_map, row_add_map = dir

        # Conditions:
        cond_0 = self._map[int((row + row_add_map + (conf.user_size + conf.tile_size) / 2) // conf.tile_size), int((col + col_add_map + (conf.user_size + conf.tile_size) / 2) // conf.tile_size)]
        cond_1 = self._map[int((row + row_add_map + (conf.user_size + conf.tile_size) / 2) // conf.tile_size), int((col + col_add_map - (conf.user_size - conf.tile_size) / 2) // conf.tile_size)]
        cond_2 = self._map[int((row + row_add_map - (conf.user_size - conf.tile_size) / 2) // conf.tile_size), int((col + col_add_map + (conf.user_size + conf.tile_size) / 2) // conf.tile_size)]
        cond_3 = self._map[int((row + row_add_map - (conf.user_size - conf.tile_size) / 2) // conf.tile_size), int((col + col_add_map - (conf.user_size - conf.tile_size) / 2) // conf.tile_size)]

        return any((cond_0, cond_1, cond_2, cond_3))


    def update(self, mouse):
        self.count = self.count + 1
        if self.count == self.nframes * 10:
            self.count = 0

        fila = self.estat
        columna = self.count // 10

        # States:
        if not mouse == conf.posicio_personatge:

            # Rotate Image:
            angle_deg, angle_rad = self.get_angle(mouse)
            self.image = py.transform.rotozoom(self.llista_im[fila][columna], angle_deg, 1)
            # Note: The player rotates around the same point as the old rect
            self.rect = self.image.get_rect(center=self.rect.center)

            # Note: False -> The mouvement DOES depend on the players orientation.
            #       True  -> The mouvement DOES NOT depend on the players orientation.
            if (True):
                angle_rad = pi/2

            # Basic States:
            if self.estat == self.AMUNT:
                col_add, row_add = ( cos( angle_rad ) * self.velocity, - sin( angle_rad ) * self.velocity )
                if not self.check_collision((0, row_add)):
                    self.rect = self.rect.move(0, row_add)
                if not self.check_collision((col_add, 0)):
                    self.rect = self.rect.move(col_add, 0)

            elif self.estat == self.AVALL:
                col_add, row_add = ( cos( angle_rad + pi) * self.velocity, - sin( angle_rad + pi) * self.velocity )
                if not self.check_collision((0, row_add)):
                    self.rect = self.rect.move(0, row_add)
                if not self.check_collision((col_add, 0)):
                    self.rect = self.rect.move(col_add, 0)

            elif self.estat == self.DRETA:
                col_add, row_add = ( cos( angle_rad + 1.5 * pi) * self.velocity, - sin( angle_rad  + 1.5 * pi) * self.velocity )
                if not self.check_collision((0, row_add)):
                    self.rect = self.rect.move(0, row_add)
                if not self.check_collision((col_add, 0)):
                    self.rect = self.rect.move(col_add, 0)

            elif self.estat == self.ESQUERRA:
                col_add, row_add = ( cos( angle_rad + pi / 2) * self.velocity, - sin( angle_rad  + pi / 2) * self.velocity )
                if not self.check_collision((0, row_add)):
                    self.rect = self.rect.move(0, row_add)
                if not self.check_collision((col_add, 0)):
                    self.rect = self.rect.move(col_add, 0)

            elif self.estat == self.STOP:
                pass

            # Advanced States:
            elif self.estat == self.AVALL_DRETA:
                # Down:
                col_add, row_add = ( (1 / sqrt(2) ) * cos( angle_rad + pi) * self.velocity, - (1 / sqrt(2) ) * sin( angle_rad + pi) * self.velocity )
                if not self.check_collision((0, row_add)):
                    self.rect = self.rect.move(0, row_add)
                if not self.check_collision((col_add, 0)):
                    self.rect = self.rect.move(col_add, 0)
                # Right:
                col_add, row_add = ( (1 / sqrt(2) ) * cos( angle_rad + 1.5 * pi) * self.velocity, - (1 / sqrt(2) ) *sin( angle_rad  + 1.5 * pi) * self.velocity )
                if not self.check_collision((0, row_add)):
                    self.rect = self.rect.move(0, row_add)
                if not self.check_collision((col_add, 0)):
                    self.rect = self.rect.move(col_add, 0)

            elif self.estat == self.AVALL_ESQUERRA:
                # Down:
                col_add, row_add = ( (1 / sqrt(2) ) * cos( angle_rad + pi) * self.velocity, - (1 / sqrt(2) ) * sin( angle_rad + pi) * self.velocity )
                if not self.check_collision((0, row_add)):
                    self.rect = self.rect.move(0, row_add)
                if not self.check_collision((col_add, 0)):
                    self.rect = self.rect.move(col_add, 0)
                # Left:
                col_add, row_add = ( (1 / sqrt(2) ) * cos( angle_rad + pi / 2) * self.velocity, - (1 / sqrt(2) ) * sin( angle_rad  + pi / 2) * self.velocity )
                if not self.check_collision((0, row_add)):
                    self.rect = self.rect.move(0, row_add)
                if not self.check_collision((col_add, 0)):
                    self.rect = self.rect.move(col_add, 0)

            elif self.estat == self.AMUNT_DRETA:
                # Up:
                col_add, row_add = ( (1 / sqrt(2) ) * cos( angle_rad ) * self.velocity, - (1 / sqrt(2) ) * sin( angle_rad ) * self.velocity )
                if not self.check_collision((0, row_add)):
                    self.rect = self.rect.move(0, row_add)
                if not self.check_collision((col_add, 0)):
                    self.rect = self.rect.move(col_add, 0)

                # Right:
                col_add, row_add = ( (1 / sqrt(2) ) * cos( angle_rad + 1.5 * pi) * self.velocity, - (1 / sqrt(2) ) * sin( angle_rad  + 1.5 * pi) * self.velocity )
                if not self.check_collision((0, row_add)):
                    self.rect = self.rect.move(0, row_add)
                if not self.check_collision((col_add, 0)):
                    self.rect = self.rect.move(col_add, 0)

            elif self.estat == self.AMUNT_ESQUERRA:
                # Up:
                col_add, row_add = ( (1 / sqrt(2) ) * cos( angle_rad ) * self.velocity, - (1 / sqrt(2) ) * sin( angle_rad ) * self.velocity )
                if not self.check_collision((0, row_add)):
                    self.rect = self.rect.move(0, row_add)
                if not self.check_collision((col_add, 0)):
                    self.rect = self.rect.move(col_add, 0)

                # Left:
                col_add, row_add = ( (1 / sqrt(2) ) * cos( angle_rad + pi / 2) * self.velocity, - (1 / sqrt(2) ) * sin( angle_rad  + pi / 2) * self.velocity )
                if not self.check_collision((0, row_add)):
                    self.rect = self.rect.move(0, row_add)
                if not self.check_collision((col_add, 0)):
                    self.rect = self.rect.move(col_add, 0)

            else:
                raise ValueError('State Unknow')

        # Weapons mechanism:
        if self.attack:

            # Note: Select the Weapon we are gonna use
            weapon = conf.weapon_dict[ self.inventory_weapons[self.selected_weapon] ]

            # Fisrt Shot:
            if self.first:
                self.first = False
                self.attack_spam = time.time()

                angle_deg, angle_rad = self.get_angle(mouse)

                return Weapon(weapon['matrix'], self.rect.center, self._map, [ weapon['velocity'], weapon['size'], [angle_deg, angle_rad], weapon['dispersion'], weapon['damage'], weapon['damage_end'] ], self._id)

            # Next Shot
            elif time.time() - self.attack_spam >= weapon['time_spam']:
                self.attack_spam = time.time()

                angle_deg, angle_rad = self.get_angle(mouse)

                return Weapon(weapon['matrix'], self.rect.center, self._map, [ weapon['velocity'], weapon['size'], [angle_deg, angle_rad], weapon['dispersion'], weapon['damage'], weapon['damage_end'] ], self._id)

        # Door Change status:
        if self.open:

            perimeter = lambda x, y: (x - door.rect.center[1] )**2 + (y - door.rect.center[0] )**2

            for door in self.doors:

                # Open the door:
                if perimeter(self.rect.center[1], self.rect.center[0]) <= ( 2 * conf.tile_size ) ** 2 and perimeter(self.rect.center[1], self.rect.center[0]) >= ( 0.75 * conf.tile_size ) ** 2:
                    if door.status == 'close':
                        door.change_status(conf.door_open_image)
                        self._map[ door.rect.center[1] // conf.tile_size, door.rect.center[0] // conf.tile_size ] = 0
                        door.status = 'open'
                        break
                    elif door.status == 'open':
                        door.change_status(conf.door_close_image)
                        self._map[ door.rect.center[1] // conf.tile_size, door.rect.center[0] // conf.tile_size ] = 1
                        door.status = 'close'
                        break

                # Don't open the door:
                else:
                    pass

            self.open = False


    # Change of selected weapon:
    def change_weapon (self):
        if self.selected_weapon < len(self.inventory_weapons) - 1:
            self.selected_weapon += 1
        else:
            self.selected_weapon = 0

    # Open a door:
    def open_door (self):
        return

    def canvia_estat(self, transicio=None):
        estat_anterior = self.estat

        # Basic mouvement:
        if transicio == self.VES_AMUNT:
            self.estat = self.AMUNT
        elif transicio == self.VES_AVALL:
            self.estat = self.AVALL
        elif transicio == self.VES_DRETA:
            self.estat = self.DRETA
        elif transicio == self.VES_ESQUERRA:
            self.estat = self.ESQUERRA
        elif transicio == self.VES_STOP:
            self.estat = self.STOP

        # Advanced mouvement:
        elif transicio == self.VES_AVALL_DRETA:
            self.estat = self.AVALL_DRETA
        elif transicio == self.VES_AVALL_ESQUERRA:
            self.estat = self.AVALL_ESQUERRA
        elif transicio == self.VES_AMUNT_DRETA:
            self.estat = self.AMUNT_DRETA
        elif transicio == self.VES_AMUNT_ESQUERRA:
            self.estat = self.AMUNT_ESQUERRA

        else:
            raise ValueError('Transició {} desconeguda'.format(transicio))

        # Set counter to 0:
        if self.estat != estat_anterior:
            self.count = 0


    def get_angle(self, mouse):
        # Lenght of triangle sides:
        opp = ( mouse[1] - conf.posicio_personatge[1] )
        adj = ( mouse[0] - conf.posicio_personatge[0] )

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
