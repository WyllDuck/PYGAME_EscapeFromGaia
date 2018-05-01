# Tools
import pygame as py
from pygame.locals import *
from pgu import engine

# Configuration:
import conf
import sprite_sheets

#Others:
from run import run
from map2D_gen import map_painter
from tile_main import Tile, TileMiniMap, UserMiniMap, Door, LifebarBackground, Lifebar
from user import Character
from tile_type import type_detector
from camera import Camera
from weapon import MiniatureWeapon

####################################
#           GAME
####################################

class Gaming(engine.State):

    def init(self):
        P_Graph, R_Graph, doors = run()
        _map = map_painter( P_Graph )

        # Tiles:
        self.tile_group = py.sprite.Group()
        self.mini_map = py.sprite.Group()

        # User Minimap:
        self.user_minimap = UserMiniMap(conf.user_image_minimap)

        # Lifebar:
        self.lifebar = Lifebar(conf.lifebar_image)
        self.lifebar_background = LifebarBackground(conf.lifebar_background_image)

        # Weapons:
        self.weapon_group = py.sprite.Group()

        # Miniature Weapon:
        self.miniature_weapon = MiniatureWeapon( conf.weapon_dict['weapon_1'] )

        # Doors:
        self.door_group = py.sprite.Group()

        for row in range(len(_map)):
            for col in range(len(_map[row, :])):

                # Floor Tile:
                if _map[row, col] == 0:
                    tile = Tile(conf.floor_image)
                    tile.rect.center = (col * conf.tile_size, row * conf.tile_size)
                    self.tile_group.add(tile)

                    # Minimap:
                    tile_minimap = TileMiniMap(conf.floor_image_minimap)
                    tile_minimap.rect.center = (col * conf.tile_size_mini_map + conf.position_mini_map[0], row * conf.tile_size_mini_map + conf.position_mini_map[1])
                    self.mini_map.add(tile_minimap)

                # Internal Wall Tile / Edge Tile / External Wall Tile:
                elif _map[row, col] == 1:
                    _type = type_detector((row, col), _map)
                    if not _type:
                        ValueError ('No type for this tile {}:{} (row, col)'.format(row, col))
                        _type = -1

                    # Note: Creating Wall Tile specific to type / "_type"
                    image = '{}{}.png'.format(conf.root_wall_image,_type + 1)
                    tile = Tile(image)
                    tile.rect.center = (col * conf.tile_size, row * conf.tile_size)
                    self.tile_group.add(tile)

                    # Minimap:
                    tile_minimap = TileMiniMap(conf.wall_image_minimap)
                    tile_minimap.rect.center = (col * conf.tile_size_mini_map + conf.position_mini_map[0], row * conf.tile_size_mini_map + conf.position_mini_map[1])
                    self.mini_map.add(tile_minimap)

        # Doors
        for door in doors:
            tile = Door(conf.door_close_image)
            tile.rect.center = (door.col * conf.tile_size ,door.row * conf.tile_size)
            self.door_group.add(tile)

        # User
        im = py.image.load(conf.sprite_sheet_personatge)
        self.grup = py.sprite.Group() # grup de Sprites
        mat_im = sprite_sheets.crea_matriu_imatges(im, *conf.mides_sprite_sheet_personatge)
        self.heroi = Character( mat_im, conf.posicio_personatge, _map, self.door_group)
        self.grup.add(self.heroi)

        # Camera:
        self.camera = Camera(conf.screen_size[0], conf.screen_size[1])


    # The paint method is called once.  If you call repaint(), it
    # will be called again.
    def paint(self,screen):
        self.update(screen)

    # Every time an event occurs, event is called.  If the event
    # method returns a value, it will become the new state.
    def event(self,event):

        if event.type == KEYDOWN or event.type == KEYUP:
            key = py.key.get_pressed()

            w,a,s,d,shift,space,e,q,esc = (key[py.K_w], key[py.K_a], key[py.K_s], key[py.K_d], key[py.K_LSHIFT], key[K_SPACE], key[K_e], key[K_q], key[K_ESCAPE])

            # Mouvement:
            if any((w,s,a,d)):

                # Firts we test advenced mouvements
                if all((w,d)):
                    self.heroi.canvia_estat(self.heroi.VES_AMUNT_DRETA)
                elif all((w,a)):
                    self.heroi.canvia_estat(self.heroi.VES_AMUNT_ESQUERRA)
                elif all((s,d)):
                    self.heroi.canvia_estat(self.heroi.VES_AVALL_DRETA)
                elif all((s,a)):
                    self.heroi.canvia_estat(self.heroi.VES_AVALL_ESQUERRA)

                # If none of above statements are true we test basic mouvements
                elif w:
                    self.heroi.canvia_estat(self.heroi.VES_AMUNT)
                elif s:
                    self.heroi.canvia_estat(self.heroi.VES_AVALL)
                elif d:
                    self.heroi.canvia_estat(self.heroi.VES_DRETA)
                elif a:
                    self.heroi.canvia_estat(self.heroi.VES_ESQUERRA)

            else:
                self.heroi.canvia_estat(self.heroi.VES_STOP)

            # Actions:
            #   Speed:
            if shift:
                self.heroi.velocity = conf.velocity_low
            else:
                self.heroi.velocity = conf.velocity_fast

            #   Attack:
            if space:
                self.lifebar.update(20)
                self.heroi.attack = True
            else:
                self.heroi.attack = False

            # Change Weapon:
            if e:
                self.heroi.change_weapon()

            # Open Door:
            if q:
                self.heroi.open = True
            else:
                self.heroi.open = False

            # Pause Menu:
            if esc:
                return self.game.change_state('PAUSE')


    # Loop is called once a frame.  It should contain all the logic.
    # If the loop method returns a value it will become the new state.
    def loop(self):
        weapon = self.heroi.update(py.mouse.get_pos())
        if weapon:
            self.weapon_group.add(weapon)

        # Detect end on cycle of a weapon:
        for weapon in self.weapon_group:
            _del = weapon.update()
            if _del:
                self.weapon_group.remove(weapon)

        # Weapon miniature on Lifebar Background:
        if not self.miniature_weapon == conf.weapon_dict[ self.heroi.inventory_weapons[self.heroi.selected_weapon] ]:
            self.miniature_weapon = MiniatureWeapon( conf.weapon_dict[ self.heroi.inventory_weapons[self.heroi.selected_weapon] ] )

        self.camera.update(self.heroi)
        self.user_minimap.update(self.heroi.rect.center)
        self.door_group.update()

    # Update is called once a frame. It should update the display.
    def update(self,screen):
        screen.fill(conf.background_color)

        # Tiles
        for sprite in self.tile_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

        # Doors
        for sprite in self.door_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

        # User
        for sprite in self.grup:
            screen.blit(sprite.image, self.camera.apply(sprite))

        # Weapon
        for sprite in self.weapon_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

        # Minimap
        #   Tiles
        self.mini_map.draw(screen)
        #   User
        screen.blit(self.user_minimap.image, self.user_minimap.rect)

        # Lifebar
        screen.blit(self.lifebar.image, self.lifebar.rect)
        screen.blit(self.lifebar_background.image, self.lifebar_background.rect)

        # Weapon Miniature:
        screen.blit(self.miniature_weapon.image, self.miniature_weapon.rect)

        py.display.flip()
