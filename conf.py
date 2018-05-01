# General Parameters:
debugger = True
debugger_pro = False
debugger_planar = True
tile_size = 64
user_size = 40
sound = True
first_init = True

# Parameters Rooms:
baseSize = (40, 40)
border_limit = 4
room_number = 10

# Parameters Screen ( game.py ):
screen_size = 1080, 720
fps = 60
background_color = 155, 155, 155

# Parameters Tiles ( main.py ):
floor_image = 'assets/2d_floor_1.png'
door_open_image = 'assets/2d_door_open_1.png'
door_close_image = 'assets/2d_door_close_1.png'
root_wall_image = 'assets/2d_wall_'

# Parameters User ( user.py ):
sprite_sheet_personatge = "assets/user.png"
mides_sprite_sheet_personatge = 9, 5
posicio_personatge = screen_size[0] // 2, screen_size[1] // 2
velocity_fast = 5
velocity_low = 2

# Parameters minimap ( game.py, tile_main.py ):
tile_size_mini_map = 4 + 1
padding_mini_map = 20
position_mini_map = (screen_size[0] - padding_mini_map - baseSize[1] * tile_size_mini_map, padding_mini_map)
wall_image_minimap = 'assets/2d_wall_minimap.png'
floor_image_minimap = 'assets/2d_floor_minimap.png'
user_image_minimap = 'assets/2d_user_minimap.png'

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

# Parameters Weapon_1 ( weapon.py, game.py ):
sprite_sheet_weapon_1 = "assets/weapon_1.png"
miniature_image_weapon_1 = "assets/miniature_weapon_1.png"
size_sprite_sheet_weapon_1 = 2, 5
velocity_weapon_1 = 13.5
size_weapon_1 = 32, 32

# Note: Dispersion in degrees
dispersion_weapon_1 = 18
# Note: Time spam between two shots in seconds
time_spam_weapon_1 = 0.1


# Parameters Weapon_2 ( weapon.py, game.py ):
sprite_sheet_weapon_2 = "assets/weapon_2.png"
miniature_image_weapon_2 = "assets/miniature_weapon_2.png"
size_sprite_sheet_weapon_2 = 2, 5
velocity_weapon_2 = 18
size_weapon_2 = 32, 32

# Note: Dispersion in degrees
dispersion_weapon_2 = 5
# Note: Time spam between two shots in seconds
time_spam_weapon_2 = 0.4


# Weapon dictionary:
weapon_dict = {'weapon_1': {'sprite_sheet': sprite_sheet_weapon_1,
                            'size_sprite_sheet': size_sprite_sheet_weapon_1,
                            'velocity': velocity_weapon_1,
                            'size': size_weapon_1,
                            'dispersion': dispersion_weapon_1,
                            'time_spam': time_spam_weapon_1,
                            'miniature': miniature_image_weapon_1},
               'weapon_2': {'sprite_sheet': sprite_sheet_weapon_2,
                            'size_sprite_sheet': size_sprite_sheet_weapon_2,
                            'velocity': velocity_weapon_2,
                            'size': size_weapon_2,
                            'dispersion': dispersion_weapon_2,
                            'time_spam': time_spam_weapon_2,
                            'miniature': miniature_image_weapon_2},
            }


####################################
#           MENU AND OTHER
####################################

# General Parameters Menu:
# Note: title width and button width should be the same
size_button_menu = 400, 80
size_title_menu = 400, 200
padding_left = 20
padding_top = 20
padding_bottom = 20
# Note: padding between each button
padding_buttons = 40

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
background_loading_image = 'assets/background_loading.png'

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
dead_screen_image = 'assets/.png'
dead_screen_position = 0
dead_screen_restart_position = 0
dead_screen_menu_position = 0
