import config as c
from button import Button
from game import Game
from image import Image
from duck import Duck
from wall import Wall
from text_object import TextObject

import pygame
import random
import time

class Rocket(Game):
    def __init__(self):
        Game.__init__(self,
                      'Rocket',
                      c.screen_width,
                      c.screen_height,
                      c.background_image,
                      c.frame_rate)
        self.start_level = False
        self.menu_buttons = []
        self.settings_buttons = []
        self.character_buttons = []
        self.character_images = []
        self.character_id = 0
        self.is_game_running = False
        self.create_objects()

    # MENU
    def create_menu(self):
        def on_play(button):
            for b in self.menu_buttons:
                self.objects.remove(b)

            self.is_game_running = True
            self.start_level = True

        def on_quit(button):
            self.game_over = True
            self.is_game_running = False
            self.game_over = True

        def on_settings(button):
            for b in self.menu_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_settings()

        def on_records(button):
            pass

        # first rendering of menu buttons
        if len(self.menu_buttons) == 0:
            for i, (text, click_handler) in \
                enumerate((('НОВАЯ ИГРА', on_play),
                           ('НАСТРОЙКИ', on_settings),
                           ('РЕКОРДЫ', on_records),
                           ('ВЫХОД', on_quit))):
                b = Button(c.menu_offset_x,
                           c.menu_offset_y + (c.menu_button_h + 50) * i,
                           c.menu_button_w,
                           c.menu_button_h,
                           text,
                           click_handler,
                           padding=5)
                self.objects.append(b)
                self.menu_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)
        # re-rendering of menu buttons
        else:
            for b in self.menu_buttons:
                self.objects.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)

    def create_duck(self):
        duck = Duck((c.screen_width - c.duck_width) // 2,
                        c.screen_height - c.duck_height * 2,
                        c.duck_width,
                        c.duck_height,
                        c.duck_color,
                        c.duck_speed,
                        self.character_id)
        self.keydown_handlers[pygame.K_LEFT].append(duck.handle)
        self.keydown_handlers[pygame.K_RIGHT].append(duck.handle)
        self.keydown_handlers[pygame.K_UP].append(duck.handle)
        self.keydown_handlers[pygame.K_DOWN].append(duck.handle)
        self.keyup_handlers[pygame.K_LEFT].append(duck.handle)
        self.keyup_handlers[pygame.K_RIGHT].append(duck.handle)
        self.duck = duck
        self.objects.append(self.duck)
    
    def create_wall(self, speed):
        self.wall = Wall(c.screen_width,
                         random.choice(range(0, c.screen_height-c.wall_height + 50, 50)),
                         c.wall_width,
                         c.wall_height,
                         c.wall_color, 
                         [-(speed), 0])
        self.objects.append(self.wall)



    def create_objects(self):
        self.create_menu()
        

    def create_game(self):
        self.create_duck()



    # SETTINGS
    def create_settings(self):
        def on_background(button):
            pass

        def on_character(button):
            for b in self.settings_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_character()

        def on_difficulty(button):
            pass

        def on_back_from_settings(button):
            for b in self.settings_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_menu()

        # first rendering of settings buttons
        if len(self.settings_buttons) == 0:
            for i, (text, click_handler) in \
                enumerate((('ФОН', on_background),
                           ('ПЕРСОНАЖ', on_character),
                           ('СЛОЖНОСТЬ', on_difficulty),
                           ('НАЗАД', on_back_from_settings))):
                b = Button(c.settings_offset_x,
                           c.settings_offset_y +
                           (c.settings_button_h + 50) * i,
                           c.settings_button_w,
                           c.settings_button_h,
                           text,
                           click_handler,
                           padding=5)
                self.objects.append(b)
                self.settings_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)
        # re-rendering of settings buttons
        else:
            for b in self.settings_buttons:
                self.objects.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)

    # CHARACTER
    def create_character(self):
        def on_face_default(button):
            self.character_id = 0

        def on_face_duck(button):
            self.character_id = 1

        def on_back_from_character(button):
            for b in self.character_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            for p in self.character_images:
                self.objects.remove(p)
            self.create_settings()

        # first rendering of character buttons
        if len(self.character_buttons) == 0:
            for i, (text, click_handler) in \
                enumerate((('КВАДРАТ', on_face_default),
                           ('УТОЧКА', on_face_duck),
                           ('НАЗАД', on_back_from_character))):
                b = Button(c.character_offset_x,
                           c.character_offset_y +
                           (c.character_button_h + 50) * i,
                           c.character_button_w,
                           c.character_button_h,
                           text,
                           click_handler,
                           padding=5)
                self.objects.append(b)
                self.character_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)

            for i, (text, file_path) in \
                enumerate((('КВАДРАТ', 'images/square.png'),
                           ('УТОЧКА', 'images/duck.png'))):
                p = Image(c.character_offset_x +
                          c.character_button_w + c.image_w,
                          c.character_offset_y +
                          (c.character_button_h + 50) * i,
                          c.image_w,
                          c.image_h,
                          file_path)

                self.objects.append(p)
                self.character_images.append(p)
        # re-rendering of character buttons
        else:
            for b in self.character_buttons:
                self.objects.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)
            for p in self.character_images:
                self.objects.append(p)

    def update(self):
        if not self.is_game_running:
            return
        if self.start_level:
            self.start_level = False
            self.create_duck()
            self.show_message('ПОЛЕТЕЛИ!', centralized=True)
            self.wall_speed = c.wall_speed_initial

        if (pygame.time.get_ticks() % 1000) in range(20):
            self.wall_speed+=c.wall_acceleration
            self.create_wall(self.wall_speed) 

        super().update()

    def show_message(self, text, color=c.button_normal_back_color, font_name='Times New Roman', font_size=40, centralized=False):
        message = TextObject(c.screen_width // 2, c.screen_height // 2, lambda: text, color, font_name, font_size)
        self.draw()
        message.draw(self.surface, centralized)
        pygame.display.update()
        time.sleep(c.message_duration)




def main():
    Rocket().run()


if __name__ == '__main__':
    main()
