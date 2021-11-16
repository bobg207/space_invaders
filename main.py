import pygame
import random
from settings import *
from sprites import Player, Enemy, Missile


pygame.init()

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Game Title")

# Player
player_group = pygame.sprite.Group()            # create Sprite group for player
player = Player("assets/sprite_ship_3.png")     # create player object
player_group.add(player)                        # add player to its group

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    player_group.draw(screen)
    player_group.update()

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
