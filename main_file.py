import pygame
from pygame.rect import Rect

import config as c
from button import Button
from game import Game
from text_object import TextObject

class Rocket(Game):
    def __init__(self):
        Game.__init__(self, 'Rocket', c.screen_width, c.screen_height, c.frame_rate)
        self.start_level = False
        self.menu_buttons = []
        self.is_game_running = False
        self.create_objects()

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
            self.create_settings()
            pass;
        
        def on_records(button):
            pass;

        for i, (text, click_handler) in enumerate((('НОВАЯ ИГРА', on_play), ('НАСТРОЙКИ', on_settings), ('РЕКОРДЫ', on_records), ('ВЫХОД', on_quit))):
            b = Button(c.menu_offset_x,
                       c.menu_offset_y + (c.menu_button_h + 5) * i,
                       c.menu_button_w,
                       c.menu_button_h,
                       text,
                       click_handler,
                       padding=5)
            self.objects.append(b)
            self.menu_buttons.append(b)
            self.mouse_handlers.append(b.handle_mouse_event)

    def create_objects(self):
        self.create_menu()

    def create_settings(self):
        def on_background(button):
            pass;

        def on_character(button):
            pass;

        def on_difficulty(button):
            pass;
        
        def on_back_from_settings(button):
            pass;

        for i, (text, click_handler) in enumerate((('ФОН', on_background), ('ПЕРСОНАЖ', on_character), ('СЛОЖНОСТЬ', on_difficulty), ('НАЗАД', on_back_from_settings))):
            b = Button(c.menu_offset_x,
                       c.menu_offset_y + (c.menu_button_h + 5) * i,
                       c.menu_button_w,
                       c.menu_button_h,
                       text,
                       click_handler,
                       padding=5)
            self.objects.append(b)
            self.menu_buttons.append(b)
            self.mouse_handlers.append(b.handle_mouse_event)


def main():
    Rocket().run()

if __name__ == '__main__':
    main()
