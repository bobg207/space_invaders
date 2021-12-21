import pygame
import random

pygame.init()

# create color constants
WHITE = (255, 255, 255)
RED = (87, 9, 9)
GREEN = (12, 148, 37)
BLUE = (2, 0, 94)
BLACK = (0, 0, 0)
BLOCK_GOOD = (218, 237, 9)
BLOCK_OK = (252, 132, 3)
BLOCK_WEAK = (252, 53, 3)

# Fonts
SML_FONT = pygame.font.Font("assets/unifont.ttf", 32)
MED_FONT = pygame.font.Font("assets/unifont.ttf", 38)
LRG_FONT = pygame.font.Font("assets/unifont.ttf", 72)
LRG_FONT_BLD = pygame.font.Font("assets/unifont.ttf", 44,
                                bold = pygame.font.Font.bold)

# width by height
FPS = 50
DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 1000

# missiles
MISSILE_WIDTH = 4
MISSILE_HEIGHT = 15
MISSILE_DELAY = 500

# bombs
BOMB_WIDTH = 2
BOMB_HEIGHT = 10
BOMB_DELAY = 750

# blocks
BLOCK_WIDTH = 7
BLOCK_HEIGHT = 7
GAP = DISPLAY_WIDTH // 10
print(GAP)
LENGTH = DISPLAY_WIDTH // 10
print(LENGTH)

# ufo's
UFO_BOMB_DELAY = 1500

# images
RED_ALIEN = "assets/red.png"
GREEN_ALIEN = "assets/green.png"
YELLOW_ALIEN = "assets/yellow.png"
PLAYER_IMAGE_PATH = "assets/player.png"
UFO_IMG_PATH = "assets/ufo.png"

EXPLOSION_LIST = []
for i in range(8):
    image_path = pygame.image.load(f"assets/explosion/sprite_{i}.png")
    EXPLOSION_LIST.append(image_path)

SHEILD = [
    "  xxxxxxx",
    " xxxxxxxxx",
    "xxxxxxxxxxx",
    "xxxxxxxxxxx",
    "xxx     xxx",
    "xx       xx"
]
