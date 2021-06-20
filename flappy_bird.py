#!pip install pygame==2.0.1

import pygame, sys, random
from modules.game import Game
import modules.files_locations as FileLocations

pygame.init()

screen_width, screen_height = 380, 512

pygame.mouse.set_visible(0)

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(pygame.image.load(FileLocations.BIRD_MIDFLAP))

clock = pygame.time.Clock()

game = Game(screen,(screen_width, screen_height))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Exiting the game !')
            pygame.quit()
            sys.exit()
        else:
            game.listen_event(event)
    
    # Controlling The FPS 
    game.update()

    pygame.display.update()
    clock.tick(60)