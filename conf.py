# Tools:
import pygame as py
import random as rd

# Other:
import sprite_sheets

# Debugger(s):
debugger = False
debugger_pro = False
debugger_planar = False
immortality = False

# General Parameters:
tile_size = 64
user_size = 40

user_life = 840
life_recovery = 5
life_recovery_limit = 350
life_recovery_waiting_time = 10

sound = True
percentage_boxes = 30,60
# Note: If there are 4 loading backgrounds excluding the final loading the variable ""number_levels"" == 3
number_levels = 4
wait_time = 0.5 # [sec]
allow_enemies = True

# Parameters Rooms:
room_transporter_detection_perimeter = 0.3 # [tile]
baseSize = ( 45, 45 )
border_limit = 5
room_number =  17
room_path_size = (baseSize[0] * baseSize[1]) // room_number

# Parameters Screen ( game.py ):
screen_size = 1080, 720
fps = 60
background_color = 155, 155, 155
game_background = 'assets/game_background.jpg'

# Parameters Tiles ( main.py ):
floor_image = 'assets/2d_floor_1.png'
floor_broken_image = 'assets/2d_floor_2.png'
door_open_image = 'assets/2d_door_open_1.png'
door_close_image = 'assets/2d_door_close_1.png'
root_wall_image = 'assets/2d_wall_'

static_obstacles_images = [ 'assets/obj1x1_oxid.png',
                            'assets/obj1x1_stainless.png',
                            'assets/obj1x1_oxid.png',
                            'assets/obj1x1_stainless.png',
                            'assets/obj1x1_bidon_blue.png',
                            'assets/obj1x1_bidon_blue_oxid.png',
                            'assets/obj1x1_bidon_red.png',
                            'assets/obj1x1_bidon_red_oxid.png',
                            'assets/obj1x1_bidon_green.png',
                            'assets/obj1x1_bidon_green_oxid.png']

dinamic_obtacles = {'light': [(2,6), 'assets/obj1x1_lamp.png'], 'pipeline': [(1,7), 'assets/obj3x3.png'],
                    'eyeBox': [(2,12), 'assets/obj1x1_stainless_eyes.png'],
                    'teletransporter': [(2,12), 'assets/teleport.png']}

# Parameters User ( user.py ):
sprite_sheet_personatge = "assets/user.png"
mides_sprite_sheet_personatge = 9, 8
posicio_personatge = screen_size[0] // 2, screen_size[1] // 2
velocity_fast = 5
velocity_low = 2

# Parameters minimap ( game.py, tile_main.py ):
tile_size_mini_map = 4 + 1
padding_mini_map = 20
position_mini_map = (screen_size[0] - padding_mini_map - baseSize[1] * tile_size_mini_map, padding_mini_map)
wall_image_minimap = 'assets/2d_wall_minimap.png'
obstacle_image_minimap = 'assets/2d_obstacle_minimap.png'
floor_image_minimap = 'assets/2d_floor_minimap.png'
user_image_minimap = 'assets/2d_user_minimap.png'
init_end_image_minimap = 'assets/2d_init_end_minimap.png'

# Parameters lifebar ( game.py, tile_main.py ):
lifebar_image = 'assets/2d_lifebar.png'
lifebar_background_image = 'assets/2d_background_lifebar.png'
lifebar_size = 280, 70
lifebar_background_size = 80, 80
padding_lifebar = 20
position_lifebar = ( lifebar_background_size[0]  , screen_size[1] - padding_lifebar - lifebar_size[1] - (lifebar_background_size[1] - lifebar_size[1]) // 2)
position_lifebar_background = ( 0, screen_size[1] - padding_lifebar - lifebar_background_size[1])


####################################
#           WEAPONS
####################################

# Parameters for all weapons:
miniature_size = 65, 65
position_miniature = (lifebar_background_size[0] - miniature_size[0]) // 2, screen_size[1] - padding_lifebar - (lifebar_background_size[1] - miniature_size[1]) // 2 - miniature_size[1]

# Weapon dictionary:
weapon_dict = {'weapon_1': {'sprite_sheet': 'assets/weapon_1_bullet.png',
                            'size_sprite_sheet': (2, 18),
                            'velocity': 18,
                            'size': (16, 16),
                            'dispersion': 5,
                            'time_spam': .4,
                            'miniature': 'assets/miniature_weapon_1.png',
                            'damage': 50,
                            'damage_end' : 6},
               'weapon_2': {'sprite_sheet': 'assets/weapon_2_bullet.png',
                            'size_sprite_sheet': (2, 14),
                            'velocity': 13.5,
                            'size': (16, 16),
                            'dispersion': 18,
                            'time_spam': .1,
                            'miniature': 'assets/miniature_weapon_2.png',
                            'damage': 35,
                            'damage_end' : 9},
                'weapon_3': {'sprite_sheet': 'assets/weapon_3_bullet.png',
                             'size_sprite_sheet': (2, 12) ,
                             'velocity': 12,
                             'size': (32, 32) ,
                             'dispersion': 5,
                             'time_spam': 0.7,
                             'miniature': 'assets/miniature_weapon_3.png',
                             'damage': 100,
                             'damage_end' : 12},
                'weapon_4': {'sprite_sheet': 'assets/weapon_4_bullet.png',
                             'size_sprite_sheet': (2, 8) ,
                             'velocity': 24,
                             'size': (16, 16) ,
                             'dispersion': 3,
                             'time_spam': 0.05,
                             'miniature': 'assets/miniature_weapon_4.png',
                             'damage': 8,
                             'damage_end' : 5},
                'weapon_5': {'sprite_sheet': 'assets/weapon_5_bullet.png',
                             'size_sprite_sheet': (2, 9) ,
                             'velocity': 28,
                             'size': (32, 32) ,
                             'dispersion': 0,
                             'time_spam': 0.9,
                             'miniature': 'assets/miniature_weapon_5.png',
                             'damage': 230,
                             'damage_end' : 5}
            }

# Calculating all the weapon matrices once:
for weapon in weapon_dict:
    im = py.image.load(weapon_dict[weapon]['sprite_sheet'])
    im = sprite_sheets.crea_matriu_imatges(im, *weapon_dict[weapon]['size_sprite_sheet'])
    weapon_dict[weapon]['matrix'] = im

del(im)

####################################
#           MENU AND OTHER
####################################

# General Parameters Menu:
# Note: title width and button width should be the same
size_button_menu = 400, 80
size_title_menu = 400, 200
padding_left = 20
padding_top = 20
padding_bottom = 40
# Note: padding between each button
padding_buttons = 30

# Note: Position are all refered to "topleft"

# Background:
# Note: Background image should be screen size
background_menu_image = "assets/background_menu.png"
background_menu_title_image = "assets/background_title.png"
position_menu_title = padding_left, padding_top

# Start Button:
start_image = 'assets/start_button.png'
position_start = padding_left, screen_size[1] - padding_bottom - size_button_menu[1] - 3 * (size_button_menu[1] + padding_buttons)

# Controls Button:
controls_image = 'assets/controls_button.png'
position_controls = padding_left, screen_size[1] - padding_bottom - size_button_menu[1] - 2 * (size_button_menu[1] + padding_buttons)
background_controls_image = 'assets/background_controls.png'

# Setting Button:
settings_image = 'assets/settings_button.png'
position_settings = padding_left, screen_size[1] - padding_bottom - size_button_menu[1] - (size_button_menu[1] + padding_buttons)
background_settings_image = 'assets/background_settings.png'

# Mute / Unmute:
mute_image = 'assets/mute.png'
unmute_image = 'assets/unmute.png'
size_mute_unmute = 100, 100
# Note: This image is going to be centered / self.rect.center
position_mute_unmute = screen_size[0] // 2, screen_size[1] // 2

# Quit Button:
quit_image = 'assets/quit_button.png'
position_quit = padding_left, screen_size[1] - padding_bottom - size_button_menu[1]

# Loading Screen:
background_loading_image = ['assets/background_loading_0.png', 'assets/background_loading_1.png', 'assets/background_loading_2.png', 'assets/background_loading_3.png', 'assets/background_loading_final.png']
if len(background_loading_image) - 1 != number_levels:
    raise ValueError ('""background_loading_images"" list of images doesn\'t add up with ""number_levels"" int variable')

# Secondary Background:
# Note: Position rect.center in those cases
padding = (600 - 4 * size_button_menu[1]) / 5
secondary_background_size = 500, 600
secondary_background_position = screen_size[0] // 2, screen_size[1] // 2
secondary_background_image = 'assets/secondary_background.png'

secondary_background_continue_position = screen_size[0] // 2, (screen_size[1] - secondary_background_size[1]) // 2 + ( 0.5 * size_button_menu[1] + padding)
secondary_background_continue_image = 'assets/continue_button.png'

secondary_background_restart_position = screen_size[0] // 2, (screen_size[1] - secondary_background_size[1]) // 2 + ( 1.5 * (size_button_menu[1]) + 2 * padding)
secondary_background_restart_image = 'assets/restart_button.png'

secondary_background_menu_position = screen_size[0] // 2, (screen_size[1] - secondary_background_size[1]) // 2 + ( 2.5 * size_button_menu[1] + 3 * padding)
secondary_background_menu_image = 'assets/menu_button.png'

secondary_background_quit_position = screen_size[0] // 2, (screen_size[1] - secondary_background_size[1]) // 2 + ( 3.5 * size_button_menu[1] + 4 * padding)
# We will use the same button for the Quit Button

# Dead Screen:
dead_screen_image = 'assets/secondary_background_deadscreen.png'
dead_screen_position = screen_size[0] // 2, screen_size[1] // 2 - 52
dead_screen_restart_position = screen_size[0] // 2, screen_size[1] // 2 + 50
dead_screen_menu_position = screen_size[0] // 2, screen_size[1] // 2 - 50


####################################
#           ENEMIES
####################################

# Note: Security area is a parameter that defines the additional space between enemies
security_area = 15

# Note: This varaible is penalty applied to enemies in movement, unity [sec]
enemy_movement_penalty = 1.4

# Note: The unit of the perimeter distance must be in tiles
enemy_dict = {'enemy_1': {  'sprite_sheet': 'assets/android_red.png',
                            'velocity': 27,
                            'selected_weapon': 'weapon_2',
                            'size_sprite_sheet': (7, 7),
                            'attack_perimeter': 3.5,
                            'follow_perimeter': 5,
                            'follow_perimeter_secondary': 1.4,
                            'life': 200,
                            'size': 40,
                            'desfase': 90,
                            'weight': 20,
                            'probability': 0.2},

            'enemy_2': {    'sprite_sheet': 'assets/android_regular.png',
                            'velocity': 21,
                            'selected_weapon': 'weapon_1',
                            'size_sprite_sheet': (7, 7),
                            'attack_perimeter': 4,
                            'follow_perimeter': 7,
                            'follow_perimeter_secondary': 1.4,
                            'life': 100,
                            'size': 40,
                            'desfase': 90,
                            'weight': 15,
                            'probability': 0.57},

            'enemy_3': {    'sprite_sheet': 'assets/dog.png',
                            'velocity': 13,
                            'selected_weapon': 'weapon_4',
                            'size_sprite_sheet': (7, 6),
                            'attack_perimeter': 5,
                            'follow_perimeter': 9,
                            'follow_perimeter_secondary': 1.4,
                            'life': 70,
                            'size': 40,
                            'desfase': 90,
                            'weight': 10,
                            'probability': 0.2},

            'enemy_4': {    'sprite_sheet': 'assets/gaia_clone.png',
                            'velocity': 30,
                            'selected_weapon': 'weapon_5',
                            'size_sprite_sheet': (7, 20),
                            'attack_perimeter': 5,
                            'follow_perimeter': 7,
                            'follow_perimeter_secondary': 1.4,
                            'life': 500,
                            'size': 40,
                            'desfase': 90,
                            'weight': 30,
                            'probability': 0.03 }}

# Note: This list needs to add 1
probablity_enemies = [0.2, 0.57, 0.2, 0.03]
probablity_enemies = [enemy_dict[enemy]['probability'] for enemy in enemy_dict.keys()]

enemy_density = 0.2

# Loading sprite matrix:
for enemy in enemy_dict:
    im = py.image.load(enemy_dict[enemy]['sprite_sheet'])
    enemy_dict[enemy]['sprite'] = sprite_sheets.crea_matriu_imatges(im, *enemy_dict[enemy]['size_sprite_sheet'])
del(im)
