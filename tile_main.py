# Tools
import pygame as py
import time
import random as rd

# Configuration:
import conf

# Static Tile
class Tile (py.sprite.Sprite):
    def __init__ (self, image):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()


# Dinamic Tile: focussed on animated obstacles
class DinamicTileLight (py.sprite.Sprite):

    ON_OFF, OFF_ON = range(2)

    def __init__ (self, image_matrix):
        super().__init__()

        # Dinamic logic:
        self.matrix = image_matrix
        self.count = 0
        self.nframes = len(self.matrix[0])
        self.state = self.ON_OFF

        self.wait = 0
        self.clock = time.time()
        self.image = self.matrix[self.state][0]
        self.rect = self.image.get_rect()


    # Dinamic logic:
    def update (self):
        if self.wait < time.time() - self.clock:
            self.count = self.count + 1
            if self.count == self.nframes * 10:
                self.count = 0
                self.state = self.ON_OFF if self.state == self.OFF_ON else self.OFF_ON

                # How many time should the lamp wait to continue it's ON_OFF process (or OFF_ON)
                self.wait = rd.randrange(10, 200) // 100
                self.clock = time.time()

            row = self.state
            col = self.count // 10

            self.image = self.matrix[row][col]

# Dinamic Tile: focussed on animated obstacles
class DinamicTilePipeline (py.sprite.Sprite):

    def __init__ (self, image_matrix):
        super().__init__()

        # Dinamic logic:
        self.matrix = image_matrix
        self.count = 0
        self.nframes = len(self.matrix[0])

        self.wait = 0
        self.clock = time.time()

        # Rotate image keeping the center
        self.image = self.matrix[0][0]
        self.rect = self.image.get_rect()

    # Dinamic logic:
    def update (self):
        self.count = self.count + 1
        if self.count == self.nframes * 10:
            self.count = 0

        col = self.count // 10
        self.image = self.matrix[0][col]

# Dinamic Tile: focussed on animated obstacles
class DinamicTileEyeBox (py.sprite.Sprite):

    CLOSE, OPEN = range(2)

    def __init__ (self, image_matrix):
        super().__init__()

        # Dinamic logic:
        self.matrix = image_matrix
        self.count = 0
        self.nframes = len(self.matrix[0])
        self.state = self.CLOSE
        self.switch = True

        self.image = self.matrix[self.state][0]
        self.rect = self.image.get_rect()

    # Dinamic logic:
    def update (self, user_pos):

        self.count = self.count + 1

        if self.state == self.CLOSE:
            if self.action(user_pos) and self.switch:
                self.state = self.OPEN
                self.switch = False
                self.count = 0

        if self.state == self.OPEN:
            if self.count == self.nframes * 10:
                self.state = self.CLOSE
                self.count = 0

        if self.count == self.nframes * 10:
            self.count = 0

        row = self.state
        col = self.count // 10

        self.image = self.matrix[row][col]

    def action (self, user_pos):

        # Position enemy sight
        cercle_row, cercle_col = self.rect.center
        perimeter = lambda x, y: (x - cercle_row )**2 + (y - cercle_col )**2
        return perimeter(user_pos[0], user_pos[1]) <= ( 2 * conf.tile_size ) ** 2

# Dinamic Tile: focussed on animated obstacles
class DinamicTeleport (py.sprite.Sprite):

    CLOSE, OPEN = range(2)

    def __init__ (self, image_matrix):
        super().__init__()

        # Dinamic logic:
        self.matrix = image_matrix
        self.count = 0
        self.nframes = len(self.matrix[0])
        self.state = self.CLOSE
        self.switch = True

        self.image = self.matrix[self.state][0]
        self.rect = self.image.get_rect()

    # Dinamic logic:
    def update (self, user_pos):

        self.count = self.count + 1

        if self.state == self.CLOSE:
            if self.action(user_pos) and self.switch:
                self.state = self.OPEN
                self.switch = False
                self.count = 0

        if self.state == self.OPEN:
            if self.count == self.nframes * 10:
                self.state = self.CLOSE
                self.count = 0

        if self.count == self.nframes * 10:
            self.count = 0

        row = self.state
        col = self.count // 10

        self.image = self.matrix[row][col]

    def action (self, user_pos):

        # Position enemy sight
        cercle_row, cercle_col = self.rect.center
        perimeter = lambda x, y: (x - cercle_row )**2 + (y - cercle_col )**2
        return perimeter(user_pos[0], user_pos[1]) <= ( conf.room_transporter_detection_perimeter * conf.tile_size ) ** 2


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
    def __init__ (self, image, orientation):
        super().__init__()
        self.image = py.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.status = 'close'
        self.orientation = orientation
        self.image = py.transform.rotozoom(self.image, (90 if self.orientation == 'row' else 0), 1)


    def change_status(self, image):
        self.image = py.image.load(image).convert_alpha()
        self.image = py.transform.rotozoom(self.image, (90 if self.orientation == 'row' else 0), 1)


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
