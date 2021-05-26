
screen_width = 800
screen_height = 600
background_image = 'images/background.png'
character_images = {0: 'images/square.png', 1: 'images/duck.png', 2:'images/horse.png'}
wall_image = 'images/block.png'
star_image = 'images/bonus_star.png'
bomb_image = 'images/bonus_bomb.png'
heart_image = 'images/bonus_heart.png'
frame_rate = 90

status_offset_y = 5
time_offset = 350
lives_offset = 600

text_color = (255, 255, 0)
initial_lives = 3
# lives_right_offset = 85
# lives_offset = screen_width - lives_right_offset
score_offset = 5

font_name = 'Arial'
font_size = 20

effect_duration = 20
# sounds_effects = dict(
#     brick_hit='sound_effects/brick_hit.wav',
#     effect_done='sound_effects/effect_done.wav',
#     paddle_hit='sound_effects/paddle_hit.wav',
#     level_complete='sound_effects/level_complete.wav',
# )

message_duration = 2

button_text_color = (255, 255, 255),
button_normal_back_color = (0, 139, 139)
button_hover_back_color = (238, 99, 99)
button_pressed_back_color = (205, 85, 85)

menu_offset_x = 200
menu_offset_y = 100
menu_button_w = 400
menu_button_h = 50

settings_offset_x = 200
settings_offset_y = 100
settings_button_w = 400
settings_button_h = 50

character_offset_x = 200
character_offset_y = 100
character_button_w = 400
character_button_h = 50

image_w = 50
image_h = 50

duck_width = 70
duck_height = 70
duck_width_large = 80
duck_height_large = 80
duck_width_small = 30
duck_height_small = 30
duck_color = (255, 255, 255)
duck_speed = 6

wall_height = 100
wall_width = 40
wall_color = (255, 255, 255)
wall_speed_initial = 3
wall_acceleration = 0.05
wall_amount = 20
walls_regularity = 1500

bonus_height = 30
bonus_width = 30
bonus_color = (255, 0, 0)
bonuses_amount = 5
bonuses_regularity = 7000

offset = 10

high_score_file = 'score.txt'