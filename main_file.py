import config as c
from button import Button
from game import Game
from image import Image
from duck import Duck
from wall import Wall
from bonus import Bonus
from text_object import TextObject
from pygame.rect import Rect

import pygame as pg
import random
import time
from collections import deque
import shelve


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
        self.difficulty_buttons = []
        self.character_images = []
        self.character_objects = []
        self.label_objects = [0] * 3
        self.character_id = 1
        self.wall_app_mode = 0
        self.mode = 'main'
        self.is_game_running = False
        self.walls_current = deque()
        self.bonuses_current = deque()
        self.lives = c.initial_lives
        self.create_objects()
        self.pause_duration = 0
        self.current_timer = 0
        self.high_score = 0
        self.last_wall_app = 0
        self.last_bonus_app = c.bonus_offset
        self.last_wall_change = 0
        self.last_bias_change = 0
        self.bias_key = [80, 1]
        self.is_final_line = 0
        self.set_high_score()

    # MENU
    def create_menu(self):
        def on_play(button):
            for b in self.menu_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)

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

        def on_continue_game(button):
            global pause_start
            self.pause_duration += pg.time.get_ticks() - pause_start
            for b in self.menu_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.is_game_running = True
            for obj in self.character_objects:
                obj.character = self.character_id
                obj.change_character()
                self.objects.append(obj)

        def on_character(button):
            for b in self.menu_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_character()

        # first rendering of menu buttons
        if len(self.menu_buttons) == 0:
            for i, (text, click_handler) in \
                enumerate((
                    ("НОВАЯ ИГРА", on_play),
                    ("НАСТРОЙКИ", on_settings),
                    ("РЕКОРДЫ", on_records),
                    ("ВЫХОД", on_quit))):
                b = Button(
                    c.menu_offset_x,
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
            if self.mode == 'main':
                for b in self.menu_buttons:
                    self.objects.append(b)
                    self.mouse_handlers.append(b.handle_mouse_event)
            elif self.mode == 'short':
                self.menu_buttons = []
                for i, (text, click_handler) in \
                    enumerate((("ВЕРНУТЬСЯ", on_continue_game),
                               ("ПЕРСОНАЖ", on_character),
                               ("ВЫХОД", on_quit))):
                    b = Button(
                        c.menu_offset_x,
                        c.menu_offset_y + (c.menu_button_h + 50) * i,
                        c.menu_button_w,
                        c.menu_button_h,
                        text,
                        click_handler,
                        padding=5)
                    self.objects.append(b)
                    self.menu_buttons.append(b)
                    self.mouse_handlers.append(b.handle_mouse_event)

    def create_duck(self):
        duck = Duck((
            c.screen_width - c.duck_width) // 2,
            c.screen_height - c.duck_height * 2,
            c.duck_width,
            c.duck_height,
            c.duck_color,
            c.duck_speed,
            self.character_id)
        self.keydown_handlers[pg.K_LEFT].append(duck.handle)
        self.keydown_handlers[pg.K_RIGHT].append(duck.handle)
        self.keydown_handlers[pg.K_UP].append(duck.handle)
        self.keydown_handlers[pg.K_DOWN].append(duck.handle)
        self.keyup_handlers[pg.K_LEFT].append(duck.handle)
        self.keyup_handlers[pg.K_RIGHT].append(duck.handle)
        self.keyup_handlers[pg.K_UP].append(duck.handle)
        self.keyup_handlers[pg.K_DOWN].append(duck.handle)
        self.duck = duck
        self.objects.append(self.duck)
        self.character_objects.append(self.duck)

    def handle_stop_game(self, key):
        global pause_start
        if self.is_game_running is True and key == pg.K_ESCAPE:
            self.is_game_running = False
            pause_start = pg.time.get_ticks()
            self.mode = 'short'
            for obj in self.character_objects:
                self.objects.remove(obj)
                # self.keydown_handlers.remove(obj.handle)
                # self.keyup_handlers.remove(obj.handle)
            self.create_menu()
        else:
            pass

    def create_wall(self, speed_x, speed_y=0):
        walls_num = random.choice([3, 3, 4, 4, 5])
        free_space = c.duck_height + random.choice(range(20, 40))
        walls_distance = []
        space_left = c.screen_height - c.wall_height * walls_num - free_space
        for i in range(walls_num):
            new_distance = random.choice(range(1, 80))
            walls_distance.append(new_distance)
        walls_distance = [
            i / sum(walls_distance) * space_left for i in walls_distance
        ]
        walls_distance.append(free_space)
        random.shuffle(walls_distance)

        for i in range(walls_num):
            space_ttl = sum(walls_distance[0:i])
            walls_ttl = c.wall_height * (i + 1)
            wall = Wall(
                c.screen_width,
                c.screen_height - space_ttl - walls_ttl,
                c.wall_width,
                c.wall_height,
                c.wall_color,
                [-(speed_x), speed_y])
            if len(self.walls_current) > c.wall_amount:
                self.objects.remove(self.walls_current[0])
                self.walls_current.popleft()
            self.walls_current.append(wall)
            self.objects.insert(0, wall)

    def create_wall_determined(self, bias_key, speed_x, speed_y=0):
        wall = Wall(c.screen_width + 50,
                    random.choice(range(c.screen_height - bias_key - 30,
                                        c.screen_height - bias_key, 10)),
                    c.wall_width,
                    c.wall_height,
                    c.wall_color,
                    [-(speed_x), 0])
        if len(self.walls_current) > c.wall_amount:
            self.walls_current.popleft()
        self.walls_current.append(wall)
        self.objects.append(wall)

        wall = Wall(c.screen_width,
                    random.choice(range(bias_key, bias_key + 30, 10)),
                    c.wall_width,
                    c.wall_height,
                    c.wall_color,
                    [-(speed_x), 0])
        if len(self.walls_current) > c.wall_amount:
            self.walls_current.popleft()
        self.walls_current.append(wall)
        self.objects.append(wall)
        # wall = Wall(c.screen_width,
        #             random.choice(range(c.screen_height - 300,
        #                                 c.screen_height - 250, 10)),
        #             c.wall_width,
        #             c.wall_height,
        #             c.wall_color,
        #             [-(speed_x), 1.4])
        # # if len(self.walls_current) > c.wall_amount:
        # #     self.walls_current.popleft()
        # self.walls_current.append(wall)
        # self.objects.append(wall)

        # wall = Wall(c.screen_width,
        #             random.choice(range(-50, 70, 10)),
        #             c.wall_width,
        #             c.wall_height,
        #             c.wall_color,
        #             [-(speed_x), 1.4])
        # # if len(self.walls_current) > c.wall_amount:
        # #     self.walls_current.popleft()
        # self.walls_current.append(wall)
        # self.objects.append(wall)

    def create_bonus(self, location_x, location_y, speed_x, speed_y=0):
        bonus_good = bool(random.randint(0, 1))
        bonus_type = (random.randint(0, 1))
        bonus = Bonus(
            location_x,
            location_y,
            c.bonus_width,
            c.bonus_height,
            c.bonus_color,
            [-(speed_x), speed_y],
            bonus_good,
            bonus_type)
        if len(self.bonuses_current) > c.bonuses_amount:
            self.bonuses_current.popleft()
        self.bonuses_current.append(bonus)
        self.objects.append(bonus)

    def create_final_line(self):
        p = Image(
                c.screen_width - 100,
                0,
                100,
                c.screen_height,
                'images/finish_line.png')
        self.finish_line = p
        self.objects.append(p)

    def create_objects(self):
        self.create_menu()

    def create_labels(self):
        self.time_label = TextObject(
                                c.time_offset,
                                c.status_offset_y,
                                lambda: f"ВРЕМЯ: {self.current_timer}",
                                c.text_color,
                                c.font_name,
                                c.font_size)
        self.objects.append(self.time_label)
        self.high_score_label = TextObject(
                                c.time_offset,
                                c.status_offset_y + c.font_size,
                                lambda: f"ЛУЧШИЙ РЕЗУЛЬТАТ: {self.high_score}",
                                c.text_color,
                                c.font_name,
                                c.font_size)
        self.objects.append(self.high_score_label)
        for i in range(3):
            self.label_objects[i] = Image(
                                c.lives_offset + (c.image_w + 20) * i,
                                c.status_offset_y,
                                c.image_w,
                                c.image_h,
                                c.heart_image)
            self.objects.append(self.label_objects[i])

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
            for b in self.settings_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_difficulty()

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
                           ('РЕЖИМ ИГРЫ', on_difficulty),
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

    def create_difficulty(self):
        def on_infinite(button):
            self.wall_app_mode = 0

        def on_until_finish(button):
            self.wall_app_mode = 1

        def on_back_from_difficulty(button):
            for b in self.difficulty_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_settings()

        # first rendering of settings buttons
        if len(self.difficulty_buttons) == 0:
            for i, (text, click_handler) in \
                enumerate((("БЕСКОНЕЧНЫЙ РЕЖИМ", on_infinite),
                           ("ДОБРАТЬСЯ ДО ФИНИША", on_until_finish),
                           ("НАЗАД", on_back_from_difficulty))):
                b = Button(c.settings_offset_x,
                           c.settings_offset_y +
                           (c.settings_button_h + 50) * i,
                           c.settings_button_w,
                           c.settings_button_h,
                           text,
                           click_handler,
                           padding=5)
                self.objects.append(b)
                self.difficulty_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)
        # re-rendering of settings buttons
        else:
            for b in self.difficulty_buttons:
                self.objects.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)

    # CHARACTER
    def create_character(self):
        def on_face_default(button):
            self.character_id = 0

        def on_face_duck(button):
            self.character_id = 1

        def on_face_horse(button):
            self.character_id = 2

        def on_back_from_character(button):
            for b in self.character_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            for p in self.character_images:
                self.objects.remove(p)
            if self.mode == 'main':
                self.create_settings()
            elif self.mode == 'short':
                self.create_menu()

        # first rendering of character buttons
        if len(self.character_buttons) == 0:
            for i, (text, click_handler) in \
                enumerate((("КВАДРАТ", on_face_default),
                           ("УТОЧКА", on_face_duck),
                           ("КОНЬ", on_face_horse),
                           ("НАЗАД", on_back_from_character))):
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
                enumerate((("КВАДРАТ", 'images/square.png'),
                           ("УТОЧКА", 'images/duck.png'),
                           ("КОНЬ", 'images/horse.png'))):
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

    def handle_collisions(self):
        def intersect(obj, duck):
            edges = dict(left=Rect(obj.left, obj.top, 1, obj.height),
                         right=Rect(obj.right, obj.top, 1, obj.height),
                         top=Rect(obj.left, obj.top, obj.width, 1),
                         bottom=Rect(obj.left, obj.bottom, obj.width, 1))
            collisions = set(
                    edge for edge,
                    rect in edges.items() if duck.bounds.colliderect(rect))
            if not collisions:
                return None

            if len(collisions) == 1:
                return list(collisions)[0]

            if 'top' in collisions:
                if duck.centery >= obj.top:
                    return 'top'
                if duck.centerx < obj.left:
                    return 'left'
                else:
                    return 'right'

            if 'bottom' in collisions:
                if duck.centery >= obj.bottom:
                    return 'bottom'
                if duck.centerx < obj.left:
                    return 'left'
                else:
                    return 'right'

        # Hit wall
        for wall in self.walls_current:
            edge = intersect(wall, self.duck)
            if not edge:
                continue

            wall.delete()
            self.lives -= 1
            if self.lives != -1:
                self.objects.remove(self.label_objects[self.lives])

        # Hit bonus
        for bonus in self.bonuses_current:
            edge = intersect(bonus, self.duck)
            if not edge:
                continue

            bonus.delete()
            if (bonus.good):
                if (bonus.type == 0) & (self.lives < 3):
                    self.lives += 1
                    self.objects.append(self.label_objects[self.lives - 1])
                elif (bonus.type == 1):
                    self.duck.change_size(
                        c.duck_width_small, 
                        c.duck_height_small)
            elif not bonus.good:
                if (bonus.type == 0) & (self.lives <= 2):
                    for i in range(self.lives):
                        self.objects.remove(self.label_objects[i])
                elif (bonus.type == 0) & (self.lives > 2):
                    self.objects.remove(self.label_objects[self.lives - 2])
                    self.objects.remove(self.label_objects[self.lives - 1])
                elif (bonus.type == 1):
                    self.duck.change_size(
                        c.duck_width_large, 
                        c.duck_height_large)
                self.lives -= 2

    def update(self):
        if not self.is_game_running:
            return
        if self.start_level:
            self.start_level = False
            self.keyup_handlers[pg.K_ESCAPE].append(self.handle_stop_game)
            self.create_duck()
            self.create_labels()
            self.show_message("ПОЛЕТЕЛИ!", centralized=True)
            self.wall_speed = c.wall_speed_initial
            self.start_time = pg.time.get_ticks()

        self.current_timer = round(
            ((pg.time.get_ticks() - self.start_time) - self.pause_duration) / 1000, 2)

        if self.wall_app_mode == 0:
            if (pg.time.get_ticks() - self.last_wall_app) >= c.walls_regularity:
                self.last_wall_app = pg.time.get_ticks()
                self.wall_speed += c.wall_acceleration
                self.create_wall(self.wall_speed)
            if (pg.time.get_ticks() - self.last_bonus_app) >= c.bonuses_regularity:
                if (pg.time.get_ticks() - self.last_wall_app) > 400:
                    self.last_bonus_app = pg.time.get_ticks()
                    self.create_bonus(
                        c.screen_width,
                        random.randint(0, c.screen_height - c.bonus_height),
                        self.wall_speed)
        elif self.wall_app_mode == 1 and self.is_final_line == 0:
            if (pg.time.get_ticks() - self.last_wall_app) >= 350:
                self.last_wall_app = pg.time.get_ticks()
                self.create_wall_determined(self.bias_key[0], self.wall_speed)
            if (pg.time.get_ticks() - self.last_bonus_app) >= c.bonuses_regularity // 2:
                self.last_bonus_app = pg.time.get_ticks()
                self.create_bonus(
                                c.screen_width,
                                random.choice(range(250, 350, 10)),
                                self.wall_speed)
            if (pg.time.get_ticks() - self.last_bias_change) >= 300:
                if self.bias_key[0] < 180 and self.bias_key[0] >= 80:
                    self.last_bias_change = pg.time.get_ticks()
                    self.bias_key[0] = self.bias_key[0] + 15 * self.bias_key[1]
                else:
                    self.bias_key[1] *= -1
                    self.bias_key[0] = self.bias_key[0] + 15 * self.bias_key[1]

        self.handle_collisions()

        if self.lives <= 0:
            self.mode = 'main'
            self.menu_buttons = []
            self.is_game_running = False
            self.result = (pg.time.get_ticks() - self.start_time) - self.pause_duration
            self.show_message(
                            str(round(self.result / 1000, 2)) + "сек",
                            centralized=True)
            self.record_high_score(round(self.result / 1000, 2))
            self.duck.delete()
            for wall in self.walls_current:
                wall.delete()
            for bonus in self.bonuses_current:
                bonus.delete()
            for live_label in self.label_objects:
                live_label.delete()
            self.lives = c.initial_lives
            self.last_bonus_app = c.bonus_offset
            self.last_wall_app = 0
            self.pause_duration = 0
            self.current_timer = 0
            if self.wall_app_mode == 1:
                self.bias_key = [80, 1]
            self.create_objects()

        if self.wall_app_mode == 1:
            if self.current_timer >= 100 and self.current_timer <= 103:
                self.is_final_line = 1
            if self.current_timer > 13:
                self.is_final_line = 0
                self.create_final_line()
                self.mode = 'main'
                self.menu_buttons = []
                self.is_game_running = False
                self.show_message(
                                'ПОБЕДА!',
                                centralized=True)
                self.duck.delete()
                self.finish_line.delete()
                for wall in self.walls_current:
                    wall.delete()
                for bonus in self.bonuses_current:
                    bonus.delete()
                for live_label in self.label_objects:
                    live_label.delete()
                self.lives = c.initial_lives
                self.last_bonus_app = c.bonus_offset
                self.last_wall_app = 0
                self.pause_duration = 0
                self.current_timer = 0
                if self.wall_app_mode == 1:
                    self.bias_key = [80, 1]
                self.create_objects()

        super().update()

    def show_message(
                    self,
                    text,
                    color=c.button_normal_back_color,
                    font_name='Times New Roman',
                    font_size=40,
                    centralized=False):
        message = TextObject(
                            c.screen_width // 2,
                            c.screen_height // 2,
                            lambda: text,
                            color,
                            font_name,
                            font_size)
        self.draw()
        message.draw(self.surface, centralized)
        pg.display.update()
        time.sleep(c.message_duration)

    def set_high_score(self):
        with shelve.open(c.high_score_file) as current_scores:
            if '1' in current_scores:
                self.high_score = current_scores['1']

    def record_high_score(self, score):
        with shelve.open(c.high_score_file) as current_scores:
            current_scores['new'] = score
            sorted_scores = sorted(list(current_scores.values()), reverse=True)
            for i in range(len(sorted_scores)):
                current_scores[str(i + 1)] = sorted_scores[i]
            del current_scores['new']
            if len(current_scores) > 10:
                del current_scores["11"]
        self.set_high_score()


def main():
    Rocket().run()


if __name__ == '__main__':
    main()
