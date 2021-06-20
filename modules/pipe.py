from types import FunctionType
from modules.bird import Bird
import random

from pygame import Rect, Surface, transform

# this Class controls the logic behind the Pipes
class Pipe:

    PIPE_SPEED = 2
    
    def __init__(self, screen: Surface, pipe_surface: Surface, ground_offset: int, is_red: bool =False):
        self.screen = screen
        self.altura = random.randint(150,320)

        space = 100 if is_red else 130
        self.point_value = 15 if is_red else 10

        self.pipe_surface = pipe_surface

        self.pipe_top = transform.rotate(self.pipe_surface,180)
        self.pipe_bottom_rect = self.pipe_surface.get_rect(left = screen.get_width(), top = self.altura)
        self.pipe_top_rect = self.pipe_surface.get_rect(left = screen.get_width(), bottom = self.pipe_bottom_rect.top-space)

        self.already_computed = False

        self.is_dead = False
        
    def move(self, computing_function: FunctionType) -> bool:
        self.pipe_top_rect.right -= Pipe.PIPE_SPEED
        self.pipe_bottom_rect.right -= Pipe.PIPE_SPEED

        if self.pipe_top_rect.right < 100 and not self.already_computed:
            self.already_computed = True
            computing_function(amount=self.point_value)

        if self.pipe_top_rect.right < -10:
            self.is_dead = True
            return False
        
        return True

    def draw(self):
        self.screen.blit(self.pipe_surface, self.pipe_bottom_rect)
        self.screen.blit(self.pipe_top, self.pipe_top_rect)

    def check_collision(self, bird: Bird) -> bool:
        return self.pipe_top_rect.colliderect(bird.get_rect()) or self.pipe_bottom_rect.colliderect(bird.get_rect())