# Tools
import pygame as py
from pygame.locals import *
from pgu import engine
import numpy as np
import random as rd
import time
import uuid

# Configuration:
import conf
import sprite_sheets

#Others:
from run import run
from tile_main import Tile, TileMiniMap, UserMiniMap, Door, LifebarBackground, Lifebar, DinamicTileLight, DinamicTilePipeline, DinamicTileEyeBox, DinamicTeleport
from user import Character
from tile_type import type_detector
from camera import Camera
from weapon import MiniatureWeapon
from enemy import Enemy
from sprites_menu import Background

####################################
#           GAME
####################################

class Gaming(engine.State):

    def init(self):

        P_Graph, R_Graph, M_Graph, doors, _map, room_init, room_end = run(debugger = conf.debugger)

        # Saving variables:
        self.room_end = room_end
        self.M_Graph = M_Graph
        self.R_Graph = R_Graph
        self.switch = False

        # Note: After X time of not receiving any damage health will be recorvered to some Y level at Z speed
        self.time_damage = time.time()

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

        # Enemies:
        self.enemy_group = py.sprite.Group()

        # Dynamic Obstacles:
        self.dynamic_group = py.sprite.Group()

        # Dynamic Obstacles (with ""user_pos""):
        self.dynamic_user_group = py.sprite.Group()

        # Loading [ Light // Pipeline ] Obstacle matrix for further use in the program:
        im = py.image.load(conf.dinamic_obtacles['light'][1])
        mat_im_light = sprite_sheets.crea_matriu_imatges(im, *conf.dinamic_obtacles['light'][0])

        im = py.image.load(conf.dinamic_obtacles['pipeline'][1])
        mat_im_pipeline = sprite_sheets.crea_matriu_imatges(im, *conf.dinamic_obtacles['pipeline'][0])

        im = py.image.load(conf.dinamic_obtacles['eyeBox'][1])
        mat_im_eyeBox = sprite_sheets.crea_matriu_imatges(im, *conf.dinamic_obtacles['eyeBox'][0])

        im = py.image.load(conf.dinamic_obtacles['teletransporter'][1])
        mat_im_teletransporter = sprite_sheets.crea_matriu_imatges(im, *conf.dinamic_obtacles['teletransporter'][0])

        del(im)

        # Background Image:
        self.game_background = Background(conf.game_background)

        for row in range(len(_map)):
            for col in range(len(_map[row, :])):

                # Floor Tile:
                if _map[row, col] == 0:
                    tile = Tile(conf.floor_image if np.random.choice(2, 1, p=[0.1, 0.9])[0] == 1 else conf.floor_broken_image )
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

                # Obstacles
                elif _map[row, col] in [2,3,4,5,10,-1]:
                    if _map[row, col] == 2:
                        tile = Tile(rd.choice(conf.static_obstacles_images))
                        tile.rect.center = (col * conf.tile_size, row * conf.tile_size)
                        self.tile_group.add(tile)

                    elif _map[row, col] == 3:
                        tile = DinamicTileLight(mat_im_light)
                        tile.rect.center = (col * conf.tile_size, row * conf.tile_size)
                        self.dynamic_group.add(tile)

                    elif _map[row, col] == 4:
                        tile = DinamicTileEyeBox(mat_im_eyeBox)
                        tile.rect.center = (col * conf.tile_size, row * conf.tile_size)
                        self.dynamic_user_group.add(tile)

                    elif _map[row, col] == 5:
                        tile = DinamicTilePipeline(mat_im_pipeline)
                        tile.rect.center = (col * conf.tile_size, row * conf.tile_size)
                        self.dynamic_group.add(tile)

                    # Here we add the initial and final platform:
                    elif _map[row, col] == -1:
                        tile = DinamicTileEyeBox(mat_im_teletransporter)
                        tile.rect.center = (col * conf.tile_size, row * conf.tile_size)
                        self.dynamic_user_group.add(tile)
                        _map[row, col] = 0

                    elif _map[row, col] == 10:
                        tile = Tile(conf.floor_image if np.random.choice(2, 1, p=[0.1, 0.9])[0] == 1 else conf.floor_broken_image )
                        tile.rect.center = (col * conf.tile_size, row * conf.tile_size)
                        self.tile_group.add(tile)

                    # Minimap:
                    # Note: Here we need to handle the -1 tag of ""room_init"" and ""room_end""
                    if _map[row, col] != 0:
                        tile_minimap = TileMiniMap(conf.obstacle_image_minimap)
                        tile_minimap.rect.center = (col * conf.tile_size_mini_map + conf.position_mini_map[0], row * conf.tile_size_mini_map + conf.position_mini_map[1])
                        self.mini_map.add(tile_minimap)

                    else:
                        tile_minimap = TileMiniMap(conf.init_end_image_minimap)
                        tile_minimap.rect.center = (col * conf.tile_size_mini_map + conf.position_mini_map[0], row * conf.tile_size_mini_map + conf.position_mini_map[1])
                        self.mini_map.add(tile_minimap)


        # Doors
        for door in doors:
            tile = Door(conf.door_close_image, door.orientation)
            tile.rect.center = (door.col * conf.tile_size ,door.row * conf.tile_size)
            self.door_group.add(tile)

        # User
        im = py.image.load(conf.sprite_sheet_personatge)
        self.grup = py.sprite.Group() # grup de Sprites
        mat_im = sprite_sheets.crea_matriu_imatges(im, *conf.mides_sprite_sheet_personatge)

        self.heroi = Character( mat_im, tuple(coord * conf.tile_size for coord in room_init.center)[::-1], _map, self.door_group)
        self.grup.add(self.heroi)

        # Camera:
        self.camera = Camera(conf.screen_size[0], conf.screen_size[1])

        # Enemies:
        if conf.allow_enemies:

            for room in self.R_Graph.R.nodes():

                # Note: We don't want to have enemies in the initial and final rooms
                if room == room_end or room == room_init:
                    continue

                enemies = list(conf.enemy_dict.keys())
                enemies_number = room.size * conf.enemy_density

                while enemies_number > 0:

                    # Chose random position:
                    row, col = np.where( _map[room.topleft.row: room.bottomleft.row, room.topleft.col: room.topright.col] == 0 )
                    i = np.random.randint(len(row))
                    row, col = (row[i] + room.topleft.row, col[i] +  room.topleft.col)
                    del(i)
                    position = [row * conf.tile_size, col * conf.tile_size][::-1]

                    # Chose random enemy:
                    enemy = conf.enemy_dict[np.random.choice(enemies, p = conf.probablity_enemies)]

                    # Count enemy weight in room density:
                    enemies_number -= enemy['weight']

                    enemy_params = [enemy['selected_weapon'], enemy['velocity'],  enemy['attack_perimeter'],  enemy['follow_perimeter'], enemy['life'], enemy['size'], enemy['desfase'], enemy['follow_perimeter_secondary']]
                    enemy = Enemy(enemy['sprite'], position, _map, M_Graph, enemy_params, self.door_group)
                    self.enemy_group.add( enemy )


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

        # Go to next level:
        if self.action(self.heroi.rect.center) and not self.switch:
            self.switch = True
            self.clock = time.time()
            self.heroi.canvia_estat(self.heroi.VES_STOP)

        if self.switch:
            self.heroi.canvia_estat(self.heroi.VES_STOP)
            if time.time() - self.clock >= conf.wait_time:
                if self.game.count != conf.number_levels - 1:
                    return self.game.change_state('NEXT_LEVEL')
                else:
                    return self.game.change_state('MISSION_ACCOMPLISHED')

    # Subfunction:
    def action (self, user_pos):

        # Position user next level trap
        cercle_row, cercle_col = [coord * conf.tile_size for coord in self.room_end.center]
        perimeter = lambda x, y: (x - cercle_row )**2 + (y - cercle_col )**2
        return perimeter(user_pos[1], user_pos[0]) <= ( conf.room_transporter_detection_perimeter * conf.tile_size ) ** 2


    # Loop is called once a frame.  It should contain all the logic.
    # If the loop method returns a value it will become the new state.
    def loop(self):

        enemies_remove = dict()
        enemies_pos = list( (sprite._id, sprite.rect.center, sprite.size ) for sprite in self.enemy_group if sprite.state != sprite.DEAD)

        weapon = self.heroi.update(py.mouse.get_pos())
        if weapon:
            self.weapon_group.add(weapon)

        # Detect end on cycle of a weapon:
        for weapon in self.weapon_group:
            _del = weapon.update(enemies_pos, self.heroi.rect.center, self.heroi._id)

            # Note: This if statement is true is the user shots a weapon to an enemy
            if type(_del) == uuid.UUID and weapon.active_damage and weapon._id == self.heroi._id:
                if _del in enemies_remove:
                    enemies_remove[ _del ].append(weapon.damage)
                else:
                    enemies_remove[ _del ] = [weapon.damage]
                weapon.active_damage = False

            # Note: This if statement is true is the enemy shots to the user:
            elif type(_del) == uuid.UUID and weapon.active_damage and weapon._id != self.heroi._id:
                if not conf.immortality:
                    move_lifebar = int((conf.lifebar_size[0] / conf.user_life) * weapon.damage)
                    self.heroi.life -=  (conf.user_life / conf.lifebar_size[0]) * move_lifebar
                    weapon.active_damage = False
                    self.lifebar.update( move_lifebar )
                    self.time_damage = time.time()

            # Note: This if statement is true is the weapon ends he's life cycle
            elif type(_del) == bool:
                self.weapon_group.remove(weapon)

            # Nothing happens:
            elif type(_del) == type(None):
                pass
            else:
                pass

        # Weapon miniature on Lifebar Background:
        if not self.miniature_weapon == conf.weapon_dict[ self.heroi.inventory_weapons[self.heroi.selected_weapon] ]:
            self.miniature_weapon = MiniatureWeapon( conf.weapon_dict[ self.heroi.inventory_weapons[self.heroi.selected_weapon] ] )

        self.camera.update(self.heroi)
        self.user_minimap.update(self.heroi.rect.center)
        self.door_group.update()

        # Enemies:
        for enemy in self.enemy_group:

            # Damage enemies:
            if enemy._id in enemies_remove.keys():
                enemy.life -= sum(enemies_remove[enemy._id])
                enemy.state = enemy.DAMAGE

            enemies_pos = list( (sprite._id, sprite.rect.center, sprite.size + conf.security_area ) for sprite in self.enemy_group if sprite.state != sprite.DEAD )
            weapon = enemy.update( self.heroi.rect.center, enemies_pos)

            if weapon:
                self.weapon_group.add(weapon)

        # Dynamic Obstacles:
        self.dynamic_group.update()

        # Dynamic Obstacles (with ""user_pos""):
        self.dynamic_user_group.update(self.heroi.rect.center)

        # Health Recover Mecanism:
        if time.time() - self.time_damage > conf.life_recovery_waiting_time and self.heroi.life < conf.life_recovery_limit:
            move_lifebar = int((conf.lifebar_size[0] / conf.user_life) * conf.life_recovery)
            self.heroi.life +=  (conf.user_life / conf.lifebar_size[0]) * move_lifebar
            self.lifebar.update( - move_lifebar)


    # Update is called once a frame. It should update the display.
    def update(self,screen):

        screen.fill(conf.background_color)

        # Background Image:
        screen.blit(self.game_background.image, self.game_background.rect)

        # Tiles
        for sprite in self.tile_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

        # Dynamic Obstacles:
        for sprite in self.dynamic_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

        # Dynamic Obstacles (with ""user_pos""):
        for sprite in self.dynamic_user_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

        # Doors
        for sprite in self.door_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

        # Enemies
        # Note: Dead enemies must be printed first
        for sprite in self.enemy_group:
            if sprite.state == sprite.DEAD:
                screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.enemy_group:
            if sprite.state != sprite.DEAD:
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

        # Dead Screen logic:
        if self.heroi.life <= 0:
            return self.game.change_state('GAMEOVER')
