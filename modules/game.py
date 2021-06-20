import pygame

from typing import Tuple

from modules.bird import Bird
from modules.pipe import Pipe
from modules.gamestatus import GameStatus
import modules.files_locations as FileLocations

class Game:

    SPAWNEVENT = pygame.USEREVENT
    BIRDACTION = pygame.USEREVENT+1

    def __init__(self, screen: pygame.Surface, resolution: Tuple):
       
        self.screen = screen
        self.screen_width, self.screen_height = resolution
        self.ground_offset = self.screen_height - 50
        
        self.screen_center_x, self.screen_center_y = self.screen_width//2, ((self.screen_height-50)//2)

        self.gravity = 0.25
        self.ground_speed = 1
        
        self.background_day = pygame.image.load(FileLocations.BG_DAY).convert()
        self.background_night = pygame.image.load(FileLocations.BG_NIGHT).convert()
        
        self.game_mode_day = True
        self.background = pygame.transform.scale(self.background_day,(self.screen_width, self.screen_height))
        self.background_rect = self.background.get_rect(topleft = (0,0))

        self.floor_surface = pygame.image.load(FileLocations.FLOOR).convert()
        self.floor_surface = pygame.transform.scale(self.floor_surface, (self.screen_width, self.floor_surface.get_height()))
        self.floor_rect_1 = self.floor_surface.get_rect(topleft = (0, self.ground_offset))
        self.floor_rect_2 = self.floor_surface.get_rect(topleft = (self.screen_width, self.ground_offset))

        self.starting_surface = pygame.image.load(FileLocations.START_IMAGE).convert_alpha()
        self.start_surface_rect = self.starting_surface.get_rect(center = (self.screen_center_x, self.screen_center_y))

        self.pipe_green_surface = pygame.image.load(FileLocations.PIPE_GREEN).convert_alpha()
        self.pipe_red_surface = pygame.image.load(FileLocations.PIPE_RED).convert_alpha()

        self.game_over_surface = pygame.image.load(FileLocations.GAME_OVER).convert_alpha()
        self.game_over_rect = self.game_over_surface.get_rect(center = (self.screen_center_x, self.screen_center_y))

        self.game_font = pygame.font.SysFont(FileLocations.FONT,30)

        self.start_game()        
    
    def start_game(self):
        self.game_status = GameStatus()
        self.bird = Bird(self.screen,self.gravity)
        self.pipe_list = []
        self.__start_timer_pipes()
        self.game_is_paused = False
        self.player_points = 0
        self.pipe_count = 1
    
    def get_status(self) -> int:
        return self.game_status.status
    
    def set_status(self, status: int) -> None:
        self.game_status.set_status(status)

    def listen_event(self, event):
        if event.type == Game.SPAWNEVENT:
            if self.get_status() == 1:
                if self.pipe_count % 10 == 0:
                    self.pipe_list.append(Pipe(self.screen,self.pipe_red_surface,self.ground_offset, is_red=True))
                else: 
                    self.pipe_list.append(Pipe(self.screen,self.pipe_green_surface,self.ground_offset))
                self.pipe_count += 1
        if event.type == Game.BIRDACTION:
                if self.get_status() == 1:
                    self.bird.update_action()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.get_status() == 0:
                    self.set_status(1)
                elif self.get_status() == 1:
                    self.bird.fly()
                    self.increase_points()
            elif event.key == pygame.K_ESCAPE:
                if self.get_status() == 1:
                    self.game_is_paused = False
                    self.set_status(3)
                elif self.get_status() == 3:
                    self.game_is_paused = True
                    self.set_status(1)
            elif event.key == pygame.K_F1:
                self.game_mode_day = not self.game_mode_day
                if self.game_mode_day:
                    self.background = pygame.transform.scale(self.background_day,(self.screen_width, self.screen_height))
                else:
                    self.background = pygame.transform.scale(self.background_night,(self.screen_width, self.screen_height))
            elif event.key == pygame.K_F5:
                self.start_game()

    def update(self):
        self.__draw()

        if self.get_status() == 1:
            if self.__check_collisions():
                self.set_status(2)

    def __draw(self):
        self.screen.blit(self.background, (0,0))
        
        if self.get_status() == 0:
            self.screen.blit(self.starting_surface, self.start_surface_rect)
        elif self.get_status() == 1:
            self.bird.move()
            self.bird.draw()
            self.move_pipes()
        elif self.get_status() == 2:
            self.draw_game_over()
        elif self.get_status() == 3:
            self.bird.draw()
            self.draw_pipes()
        
        self.move_floor()

    def move_floor(self):
        
        if(self.floor_rect_1.right > 0):
            self.floor_rect_1.right -= self.ground_speed
        else:
            self.floor_rect_1.left = self.screen_width-1
        self.screen.blit(self.floor_surface, self.floor_rect_1)
        
        if(self.floor_rect_2.right > 0):
            self.floor_rect_2.right -= self.ground_speed
        else:
            self.floor_rect_2.left = self.screen_width-1
        self.screen.blit(self.floor_surface, self.floor_rect_2)

    def __check_collisions(self) -> bool:
        if self.bird.check_collision(self.ground_offset):
            print("COLIDIU")
            return True
        
        for pipe in self.pipe_list:
            if pipe.check_collision(self.bird):
                return True

        return False

    def __start_timer_pipes(self):
        pygame.time.set_timer(Game.SPAWNEVENT, 2000)

    def move_pipes(self):
        self.pipe_list = list(filter(lambda pipe: not pipe.is_dead, self.pipe_list))
        for pipe in self.pipe_list:
            if pipe.move(self.increase_points):
                pipe.draw()

    def draw_pipes(self):
        for pipe in self.pipe_list:
            pipe.draw()
    
    def increase_points(self,amount=5):
        self.player_points += amount

    def draw_game_over(self):
        self.screen.blit(self.game_over_surface, self.game_over_rect)
        
        final_game_point = self.game_font.render(f'PONTUAÇÃO: {self.player_points}', False, (0, 0, 0))
        
        self.game_font_rect = final_game_point.get_rect(midtop = self.game_over_rect.midbottom)
        self.screen.blit(final_game_point, self.game_font_rect)
