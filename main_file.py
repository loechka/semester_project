"""Main game file.

Contain Rocket class and handle game running process.
"""
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
import gettext
import os.path
import sys

datapath = os.path.dirname(sys.argv[0])
lang_ru = gettext.translation('game', languages=['ru'], localedir=os.path.join(datapath, 'po'))
lang_en = gettext.translation('game', languages=['en'], localedir=os.path.join(datapath, 'po'))
lang_en.install()


class Rocket(Game):
    """
    Rocket class, based on Game class.

    Contains the game itself.
    """

    def __init__(self):
        """Init Rocket class object with certain features."""
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
        self.record_buttons = []
        self.language_buttons = []
        self.records_texts = []
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
        self.last_star_app = c.star_offset
        self.last_size_change = 0
        self.last_wall_change = 0
        self.last_bias_change_up = c.bias_up_offset
        self.last_bias_change_down = c.bias_down_offset
        self.bias_key = [80, 1, 80, 1]
        self.exist_stars = 0
        self.is_final_line = 0
        self.score = list()
        self.language_id = 'en'
        self.lang_change = False
        self.set_high_score()

    # MENU
    def create_menu(self):
        """Create game menu."""
        def on_play(button):
            """Handle pressing NEW GAME button in main menu."""
            for b in self.menu_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)

            self.is_game_running = True
            self.start_level = True

        def on_new(button):
            """Handle pressing NEW GAME button during game."""
            for b in self.menu_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
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
            self.is_game_running = True
            self.start_level = True

        def on_main_menu(button):
            """Handle pressing MAIN MEN button."""
            pass

        def on_quit(button):
            """Handle pressing QUIT button."""
            self.game_over = True
            self.is_game_running = False
            self.game_over = True

        def on_settings(button):
            """Handle pressing SETTINGS button."""
            for b in self.menu_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_settings()

        def on_records(button):
            """Handle pressingHIGH SCORES button."""
            for b in self.menu_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_records()

        def on_continue_game(button):
            """Handle pressing CONTINUE button."""
            global pause_start
            self.pause_duration += pg.time.get_ticks() - pause_start
            for b in self.menu_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.is_game_running = True

        # first rendering of menu buttons
        if len(self.menu_buttons) == 0:
            for i, (text, click_handler) in \
                enumerate((
                    (_("NEW GAME"), on_play),
                    (_("SETTINGS"), on_settings),
                    (_("HIGH SCORES"), on_records),
                    (_("QUIT"), on_quit))):
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
                    enumerate(((_("CONTINUE"), on_continue_game),
                               (_("NEW GAME"), on_new),
                               (_("MAIN MENU"), on_main_menu))):
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
        """Create game character on screen and set keyboard events handling."""
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
        """Handle pressing Esc key."""
        global pause_start
        if self.is_game_running is True and key == pg.K_ESCAPE:
            self.is_game_running = False
            pause_start = pg.time.get_ticks()
            self.mode = 'short'
            self.create_menu()
        else:
            pass

    def create_wall(self, speed_x: int, speed_y: int = 0):
        """Create a layer of walls.

        Create a layer of walls with a random amount of objects.
        Set free spaces between walls in a special way that allows
        game character to fly by. Create and refresh a set of existing walls.

        Keyword arguments:
        :param speed_x: horisontal speed
        :param speed_y: vertical speed (default 0)
        """
        walls_num = random.choice([3, 3, 4, 4, 5])
        free_space = c.duck_height + random.choice(range(20, 40))
        walls_distance = []
        space_left = c.screen_height - c.wall_height * walls_num - free_space
        for i in range(walls_num):
            new_distance = random.choice(range(5, 80))
            walls_distance.append(new_distance)
        walls_distance = [
            i / sum(walls_distance) * space_left for i in walls_distance
        ]
        walls_distance.append(free_space)
        random.shuffle(walls_distance)

        for i in range(walls_num):
            space_ttl = sum(walls_distance[0:i+1])
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

    def create_wall_determined_down(self, bias_key: int, speed_x: int, speed_y: int = 0):
        wall = Wall(c.screen_width + 50,
                    random.choice(range(c.screen_height - bias_key - 30,
                                        c.screen_height - bias_key, 5)),
                    c.wall_width,
                    c.wall_height,
                    c.wall_color,
                    [-(speed_x), speed_y])
        if len(self.walls_current) > c.wall_amount * 2:
            self.objects.remove(self.walls_current[0])
            self.walls_current.popleft()
        if self.is_final_line == 0:
            self.walls_current.append(wall)
            self.objects.append(wall)

    def create_wall_determined_up(self, bias_key: int, speed_x: int, speed_y: int = 0):
        wall = Wall(c.screen_width,
                    random.choice(range(bias_key - 30, bias_key + 30 - 30, 5)),
                    c.wall_width,
                    c.wall_height,
                    c.wall_color,
                    [-(speed_x), speed_y])
        if len(self.walls_current) > c.wall_amount * 2:
            self.objects.remove(self.walls_current[0])
            self.walls_current.popleft()
        if self.is_final_line == 0:
            self.walls_current.append(wall)
            self.objects.append(wall)
        

    def create_bonus(
                    self,
                    location_x: int,
                    location_y: int,
                    speed_x: int,
                    one_type: str = 'default'):
        """Create a bonus in game window.

        Creates a bonus of one of determined types randomly.

        Keyword arguments:
        :param location_x: left coordinate
        :param location_y: top coordinate
        :param speed_x: horisontal speed
        :param speed_y: vertical speed (default 0)
        """
        bonus_good = bool(random.randint(0, 1))
        bonus_type = (random.randint(0, 1))
        bonus = Bonus(
            location_x,
            location_y,
            c.bonus_width,
            c.bonus_height,
            c.bonus_color,
            [-(speed_x), 0],
            one_type,
            bonus_good,
            bonus_type)
        if len(self.bonuses_current) > c.bonuses_amount:
            self.objects.remove(self.bonuses_current[0])
            self.bonuses_current.popleft()
        self.bonuses_current.append(bonus)
        self.objects.append(bonus)

    def create_final_line(self):
        """Create final line image."""
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
        """Create timer and high score on the top of game window."""
        self.time_label = TextObject(
                                c.time_offset,
                                c.status_offset_y,
                                lambda: _("TIME") + f": {self.current_timer}",
                                c.text_color,
                                c.font_name,
                                c.font_size)
        self.objects.append(self.time_label)
        self.high_score_label = TextObject(
                                c.time_offset,
                                c.status_offset_y + c.font_size,
                                lambda: _("HIGH SCORE") + f": {self.high_score}",
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
        """Create settings menu."""
        def on_character(button):
            """Handle pressing CHARACTER button."""
            for b in self.settings_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_character()

        def on_difficulty(button):
            """Handle pressing GAME MODE button."""
            for b in self.settings_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_difficulty()

        def on_language(button):
            """Handle pressing LANGUAGE button."""
            for b in self.settings_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_language()

        def on_back_from_settings(button):
            """Handle pressing RETURN from settings button."""
            for b in self.settings_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_menu()

        # first rendering of settings buttons
        if len(self.settings_buttons) == 0:
            for i, (text, click_handler) in \
                enumerate(((_("CHARACTER"), on_character),
                           (_("GAME MODE"), on_difficulty),
                           (_("LANGUAGE"), on_language),
                           (_("RETURN"), on_back_from_settings))):
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

    def create_records(self):
        """Create high scores table and menu."""
        def on_back_from_records(button):
            for b in self.record_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            for b in self.records_texts:
                self.objects.remove(b)
            self.record_buttons = []
            self.records_texts = []
            self.create_menu()

        def drop_records(button):
            """Handle pressing RESET button."""
            with shelve.open(c.high_score_file) as current_scores:
                for i in range(1, 11):
                    if str(i) in current_scores:
                        del current_scores[str(i)]
                self.high_score = 0
            for b in self.records_texts:
                self.objects.remove(b)
            self.records_texts = []

        with shelve.open(c.high_score_file) as current_scores:
            for i in range(1, 6):
                if str(i) in current_scores:
                    obj = TextObject(
                            c.settings_offset_x,
                            c.settings_offset_y + 50 * (i - 1),
                            lambda: f"{str(current_scores[str(i)])}" + _(" sec"),
                            c.text_color,
                            c.font_name,
                            c.font_size,
                            1)
                    self.records_texts.append(obj)
                    self.objects.append(obj)

        for i, (text, click_handler) in \
            enumerate((
                        (_("RESET"), drop_records),
                        (_("RETURN"), on_back_from_records))):
            b = Button(
                        c.settings_offset_x,
                        c.settings_offset_y +
                        50 * 5 + (c.settings_button_h + 50) * i,
                        c.settings_button_w,
                        c.settings_button_h,
                        text,
                        click_handler,
                        padding=5)
            self.objects.append(b)
            self.record_buttons.append(b)
            self.mouse_handlers.append(b.handle_mouse_event)

    def create_language(self):
        """Create language switching menu."""
        def on_eng(button):
            """Handle pressing ENGLISH button."""
            self.set_language('en')

        def on_rus(button):
            """Handle pressing RUSSIAN button."""
            self.set_language('ru')

        def on_back_from_language(button):
            """Handle pressing RETURN from language settings button."""
            for b in self.language_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_settings()

        # first rendering of settings buttons
        if self.lang_change:
            self.lang_change = False
            self.language_buttons = []
        if len(self.language_buttons) == 0:
            for i, (text, click_handler) in \
                enumerate(((_("ENGLISH"), on_eng),
                           (_("RUSSIAN"), on_rus),
                           (_("APPLY"), on_back_from_language))):
                b = Button(c.settings_offset_x,
                           c.settings_offset_y +
                           (c.settings_button_h + 50) * i,
                           c.settings_button_w,
                           c.settings_button_h,
                           text,
                           click_handler,
                           padding=5)
                self.objects.append(b)
                self.language_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)
        # re-rendering of settings buttons
        else:
            for b in self.language_buttons:
                self.objects.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)

    def create_difficulty(self):
        """Create difficulty switching menu."""
        def on_infinite(button):
            """Handle pressing ENDLESS button."""
            self.wall_app_mode = 0

        def on_until_finish(button):
            """Handle pressing REACH FINISH button."""
            self.wall_app_mode = 1

        def on_back_from_difficulty(button):
            """Handle pressing RETURN from difficulty menu button."""
            for b in self.difficulty_buttons:
                self.objects.remove(b)
                self.mouse_handlers.remove(b.handle_mouse_event)
            self.create_settings()

        # first rendering of settings buttons
        if len(self.difficulty_buttons) == 0:
            for i, (text, click_handler) in \
                enumerate(((_("ENDLESS"), on_infinite),
                           (_("REACH FINISH"), on_until_finish),
                           (_("RETURN"), on_back_from_difficulty))):
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
        """Create character switching menu."""
        def on_face_default(button):
            """Handle pressing SQUARE button."""
            self.character_id = 0

        def on_face_duck(button):
            """Handle pressing DUCK button."""
            self.character_id = 1

        def on_face_horse(button):
            """Handle pressing HORSE button."""
            self.character_id = 2

        def on_back_from_character(button):
            """Handle pressing RETURN from character switching menu."""
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
                enumerate(((_("SQUARE"), on_face_default),
                           (_("DUCK"), on_face_duck),
                           (_("HORSE"), on_face_horse),
                           (_("RETURN"), on_back_from_character))):
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
                enumerate(((_("SQUARE"), 'images/square.png'),
                           (_("DUCK"), 'images/duck.png'),
                           (_("HORSE"), 'images/horse.png'))):
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
        """Handle game objects collisions.

        Such as game character hitting walls and collecting bonuses.
        """
        def intersect(obj, duck):
            """Check intersection of game character and other object.

            Keyword arguments:
            :param obj: one of game objects
            :param duck: game character object
            """
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
                    self.last_size_change = pg.time.get_ticks()
            elif not bonus.good:
                if (bonus.type == 0):
                    if (self.lives <= 2):
                        for i in range(self.lives):
                            self.objects.remove(self.label_objects[i])
                    else:
                        self.objects.remove(self.label_objects[self.lives - 2])
                        self.objects.remove(self.label_objects[self.lives - 1])
                    self.lives -= 2
                elif (bonus.type == 1):
                    self.duck.change_size(
                        c.duck_width_large,
                        c.duck_height_large)
                    self.last_size_change = pg.time.get_ticks()

    def finish_procedures(self, wall_app_mode):
        self.mode = 'main'
        self.is_game_running = False
        self.menu_buttons = []
        if wall_app_mode == 0:
            self.set_high_score()
            self.result = (pg.time.get_ticks() - self.start_time) - self.pause_duration
            self.show_message(
                            str(round(self.result / 1000, 2)) + _("sec"),
                            centralized=True)
            self.record_high_score(round(self.result / 1000, 2))
        else:
            self.show_message(
                                _("YOU WIN!"),
                                centralized=True)
            self.finish_line.delete()
            self.last_star_app = c.star_offset
            self.exist_stars = 0
            self.last_bias_change_up = c.bias_up_offset
            self.last_bias_change_down = c.bias_down_offset
            self.bias_key = [80, 1, 80, 1]
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
        self.create_objects()


    def update(self):
        if not self.is_game_running:
            return
        if self.start_level:
            self.start_level = False
            self.keyup_handlers[pg.K_ESCAPE].append(self.handle_stop_game)
            self.create_duck()
            self.create_labels()
            self.show_message(_("LET'S GO!"), centralized=True, start=True)
            self.wall_speed = c.wall_speed_initial
            self.start_time = pg.time.get_ticks()

        self.current_timer = round(
            ((pg.time.get_ticks() - self.start_time) - self.pause_duration) / 1000, 2)

        if self.wall_app_mode == 0:
            if (pg.time.get_ticks() - self.last_wall_app) >= c.walls_regularity:
                self.last_wall_app = pg.time.get_ticks()
                self.wall_speed += c.wall_acceleration
                if not ((self.wall_speed % 1) > (1 - c.wall_acceleration)):
                    self.create_wall(self.wall_speed)
            if (pg.time.get_ticks() - self.last_bonus_app) >= c.bonuses_regularity:
                if (pg.time.get_ticks() - self.last_wall_app) > c.bonus_offset:
                    self.last_bonus_app = pg.time.get_ticks()
                    self.create_bonus(
                        c.screen_width,
                        random.randint(0, c.screen_height - c.bonus_height),
                        self.wall_speed)
        elif self.wall_app_mode == 1 and self.is_final_line == 0:
            if (pg.time.get_ticks() - self.last_wall_app) >= c.walls_regularity_finish:
                self.last_wall_app = pg.time.get_ticks()
                self.create_wall_determined_up(self.bias_key[0], self.wall_speed)
                self.create_wall_determined_down(self.bias_key[2], self.wall_speed)
            if (pg.time.get_ticks() - self.last_bonus_app) >= c.bonuses_regularity_finish\
                and (pg.time.get_ticks() - self.last_star_app) >= 200:
                self.last_bonus_app = pg.time.get_ticks()
                self.create_bonus(
                                c.screen_width,
                                random.choice(range(250, 350, 5)),
                                self.wall_speed,
                                'bomb')
            
            if (pg.time.get_ticks() - self.last_star_app) >= ((c.game_duration - 20) // 4) * 1000 \
                and (pg.time.get_ticks() - self.last_bonus_app) >= 300: 
                if self.exist_stars < c.stars_max and random.randint(0, 1):
                    self.last_star_app = pg.time.get_ticks()
                    self.exist_stars+=1
                    self.create_bonus(
                                    c.screen_width,
                                    random.choice(range(250, 350, 2)),
                                    self.wall_speed,
                                    'star')
            
            
            if (pg.time.get_ticks() - self.last_bias_change_up) >= 200:
                if self.bias_key[0] < 180 and self.bias_key[0] >= 80:
                    self.last_bias_change_up = pg.time.get_ticks()
                    self.bias_key[0] = self.bias_key[0] + 15 * self.bias_key[1]
                else:
                    self.bias_key[1] *= -1
                    self.bias_key[0] = self.bias_key[0] + 15 * self.bias_key[1]

            if (pg.time.get_ticks() - self.last_bias_change_down) >= 170:
                if self.bias_key[2] < 180 and self.bias_key[2] >= 80:
                    self.last_bias_change_down = pg.time.get_ticks()
                    self.bias_key[2] = self.bias_key[2] + 12 * self.bias_key[3]
                else:
                    self.bias_key[3] *= -1
                    self.bias_key[2] = self.bias_key[2] + 12 * self.bias_key[3]

        self.handle_collisions()
        if (pg.time.get_ticks() - self.last_size_change) >= 10000:
            self.duck.change_size(c.duck_width, c.duck_height)

        if self.lives <= 0:
            self.finish_procedures(self.wall_app_mode)

        if self.wall_app_mode == 1:
            if self.current_timer >= c.game_duration and self.current_timer <= c.game_duration + 10:
                self.is_final_line = 1
            if self.current_timer > c.game_duration + 10:
                self.is_final_line = 0
                self.create_final_line()
                self.finish_procedures(self.wall_app_mode)

        super().update()

    def show_message(
                    self,
                    text: str,
                    color: tuple = c.button_normal_back_color,
                    font_name: str = 'Times New Roman',
                    font_size: int = 40,
                    centralized: bool = False,
                    start: bool = False):
        """Show message on screen.

        Keyword Arguments:
        :param text: message text
        :param color: message text color
        :param font_name: message text font (default 'Times New Roman')
        :param font_size: message text size (default 40)
        :param centralized: is message centralized (default False)
        :param start: is it a start message (default False)
        """
        message = TextObject(
                            c.screen_width // 2,
                            c.screen_height // 2 - 50,
                            lambda: text,
                            color,
                            font_name,
                            font_size)
        rules1 = TextObject(
                            c.screen_width // 3 - 50,
                            c.screen_height // 5 * 3,
                            lambda: _(" - USE ARROW KEYS"),
                            color,
                            font_name,
                            20)
        rules2 = TextObject(
                            c.screen_width // 3 - 50,
                            c.screen_height // 5 * 3 + 30,
                            lambda: _(" - AVOID WALLS AND BOMBS"),
                            color,
                            font_name,
                            20)
        rules3 = TextObject(
                            c.screen_width // 3 - 50,
                            c.screen_height // 5 * 3 + 60,
                            lambda: _(" - COLLECT STARS"),
                            color,
                            font_name,
                            20)
        self.draw()
        message.draw(self.surface, centralized)
        if start:
            rules1.draw(self.surface, False)
            rules2.draw(self.surface, False)
            rules3.draw(self.surface, False)
        pg.display.update()
        time.sleep(c.message_duration)

    def set_high_score(self):
        """Set new high score."""
        with shelve.open(c.high_score_file) as current_scores:
            if '1' in current_scores:
                self.high_score = current_scores['1']

    def record_high_score(self, score: float):
        """Record best 10 results in a special file.

        Keyword Arguments:
        :param score: new game score
        """
        with shelve.open(c.high_score_file) as current_scores:
            current_scores['new'] = score
            sorted_scores = sorted(list(current_scores.values()), reverse=True)
            for i in range(len(sorted_scores)):
                current_scores[str(i + 1)] = sorted_scores[i]
            del current_scores['new']
            if len(current_scores) > 10:
                del current_scores['11']
        self.set_high_score()

    def set_language(self, id_new: str):
        """Set game language.

        Keyword Arguments:
        :param id_new: new language id ('ru' or 'en')
        """
        lang_curr = self.language_id
        self.language_id = id_new
        if id_new == 'ru':
            lang_ru.install()
        elif id_new == 'en':
            lang_en.install()
        if self.language_id != lang_curr:
            self.lang_change = True
            self.menu_buttons = []
            self.settings_buttons = []
            self.character_buttons = []
            self.difficulty_buttons = []
            self.record_buttons = []


def main():
    Rocket().run()


if __name__ == '__main__':
    main()
