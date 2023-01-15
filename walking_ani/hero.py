from importlib import resources

import pygame

from walking_ani.config import cfg_item

class Hero:

    def __init__(self, screen):

        self.__create_sprites()
        self.__hero_sprites = {
            "left": {
                "idle": self.__lists_of_sprites[10],
                "walking": self.__lists_of_sprites[11:20]
                },
            "right": {
                "idle": self.__lists_of_sprites[0],
                "walking": self.__lists_of_sprites[1:10]
                },          
            }
  
        
        self.__screen_width = screen.get_width()
        self.__screen_height = screen.get_height()


        self.__current_sprite = self.__hero_sprites["right"]["idle"]
        self.__width = self.__current_sprite.get_width()
        self.__height = self.__current_sprite.get_height()
        self.__half_width = self.__current_sprite.get_width()/2
    
        self.__is_moving_right = True
        self.__is_moving_left = False

        self.__time_since_last_frame = 0
        self.__walk_count = 0

        self.__position = pygame.math.Vector2(self.__screen_width/2 - self.__half_width, self.__screen_height - self.__height)

        self.__map_input()

    """ def handle_input(self, key, is_pressed):
        if key == self.__key_mapping["left"]:
            self.__is_moving_left= is_pressed 
        if key == self.__key_mapping["right"]:
            self.__is_moving_right= is_pressed """

    def update(self, delta_time):
        speed = pygame.math.Vector2(0.0, 0.0)

        if self.__is_moving_left:
            speed.x -= cfg_item("hero", "speed")  
            self.__walking_animation("left", delta_time)

        if self.__is_moving_right:
            speed.x += cfg_item("hero", "speed")
            self.__walking_animation("right", delta_time)

        distance = speed * delta_time

        if self.__allow_move_inside_limits(distance):
            self.__position += distance    
        else:
            self.__is_moving_right = not self.__is_moving_right
            self.__is_moving_left = not self.__is_moving_left
            self.__walk_count = 0

    def render(self, surface_dst):
        surface_dst.blit(self.__current_sprite, self.__position.xy)

    def release(self):
        pass

    def __allow_move_inside_limits(self, movement):
        new_pos = self.__position + movement

        if new_pos.x < 0 - self.__half_width or new_pos.x > self.__screen_width - self.__half_width:
            return False

        return True

    def __map_input(self):
        key_mapping = cfg_item("input", "key_mapping")
        self.__key_mapping = {}

        for k,v in key_mapping.items():
            self.__key_mapping[k] = pygame.key.key_code(v)

    def __create_sprites(self):
        self.__lists_of_sprites = []
        sprite_width = cfg_item("hero", "sprite", "width")
        sprite_height = cfg_item("hero", "sprite", "height")
        columns = cfg_item("hero", "sprite", "columns")
        
        with resources.path(cfg_item("hero", "file")[0], cfg_item("hero", "file")[1]) as spritesheet_file:
            spritesheet = pygame.image.load(spritesheet_file).convert_alpha()

        for i in range(cfg_item("hero", "sprite", "total_sprites")):
            left = sprite_width  * (i % columns)
            top = sprite_height * int(i / columns)
            self.__lists_of_sprites.append(spritesheet.subsurface(left, top, sprite_width, sprite_height))

    def __walking_animation(self, direction, delta_time):
        self.__time_since_last_frame += delta_time
        lenght_of_animation = len(self.__hero_sprites[direction]["walking"])
        time_per_animation_frame = cfg_item("timing", "time_per_frame") * cfg_item("timing", "fps") / lenght_of_animation

        if self.__time_since_last_frame > time_per_animation_frame:

            if self.__walk_count >= lenght_of_animation:
                self.__walk_count = 0
            
            self.__current_sprite = self.__hero_sprites[direction]["walking"][self.__walk_count]
            self.__walk_count += 1
            self.__time_since_last_frame = 0
        
        
