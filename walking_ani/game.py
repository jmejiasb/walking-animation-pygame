from importlib import resources

import pygame

from walking_ani.config import cfg_item
from walking_ani.fpsstats import FPSStats
from walking_ani.hero import Hero

class Game:

    def __init__(self):
        pygame.init()

        self.__screen = pygame.display.set_mode(cfg_item("game", "screen_size"), 0, 32)
        pygame.display.set_caption(cfg_item("game", "title"))

        with resources.path(cfg_item("font", "file")[0], cfg_item("font", "file")[1]) as font_file:
            font = pygame.font.Font(font_file, cfg_item("font","size"))

        self.__hero = Hero(self.__screen)

        self.__fps_stats = FPSStats(font)

        self.__running = False

    def run(self):
        self.__running = True

        last_time = pygame.time.get_ticks()
        time_since_last_update = 0
        while self.__running:
            delta_time, last_time = self.__calc_delta_time(last_time)
            time_since_last_update += delta_time
            while time_since_last_update > cfg_item("timing", "time_per_frame"):
                time_since_last_update -= cfg_item("timing","time_per_frame")
                self.__process_events()
                self.__update(cfg_item("timing","time_per_frame"))

            self.__render()

        self.__quit()

    def __process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            if event.type == pygame.KEYDOWN:
                self.__hero.handle_input(event.key, True)
            if event.type == pygame.KEYUP:
                self.__hero.handle_input(event.key, False)

    def __update(self, delta_time):
        self.__fps_stats.update(delta_time)
        self.__hero.update(delta_time)

    def __render(self):
        self.__screen.fill(cfg_item("game", "background_color"))
        self.__hero.render(self.__screen)
        self.__fps_stats.render(self.__screen)
        
        pygame.display.update()

    def __quit(self):
        self.__hero.release()
        pygame.quit()

    def __calc_delta_time(self, last):
        current = pygame.time.get_ticks()
        delta = current - last
        return delta, current

