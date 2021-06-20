import sys, random
from typing import List, Tuple

from pygame import Rect, Surface, image, transform, time, USEREVENT
import modules.game as game
import modules.files_locations as FileLocation

class Bird:

    def __init__(self, screen: Surface, gravity: int):
        self.gravity = gravity

        self.screen = screen
        
        self.bird_moviment = 0
        self.action = 0

        self.bird_upflap = image.load(FileLocation.BIRD_UPFLAP).convert_alpha()
        self.bird_midflap = image.load(FileLocation.BIRD_MIDFLAP).convert_alpha()
        self.bird_downflap = image.load(FileLocation.BIRD_DOWNFLAP).convert_alpha()
        self.actions = [ self.bird_upflap,self.bird_midflap,self.bird_downflap]
        self.bird_surface = self.actions[0]
        self.bird_rect = self.bird_surface.get_rect(center = (100, 256))
        self.__fly_action_timer()


    def check_collision(self, ground_offset: int) -> bool:
        if self.bird_rect.top <= 0:
            print("bateu no topo !")
            return True
        
        if self.bird_rect.bottom >= ground_offset:
            print('Caiu no Chão 1')
            return True

        return False

    def draw(self):
        self.screen.blit(transform.rotozoom(self.bird_surface,-self.bird_moviment * 3,1),self.bird_rect)
    
    def move(self):
        self.bird_moviment += self.gravity
        self.bird_rect.centery += self.bird_moviment

    def fly(self):
        self.bird_moviment = 0
        self.bird_moviment -= 6
    
    def get_rect(self) -> Rect:
        return self.bird_rect
    
    def update_action(self):
        if self.action < 2:
            self.action += 1
        else:
            self.action = 0
        self.bird_surface = self.actions[self.action]

    def __fly_action_timer(self):
        time.set_timer(game.Game.BIRDACTION, 200)