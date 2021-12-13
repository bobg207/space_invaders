import pygame
import random
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(PLAYER_IMAGE_PATH)
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.radius = self.rect.width // 2
        self.change_x = 0  # velocity variable

    def update(self):
        self.rect.x += self.change_x

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.change_x = 4
        elif keys[pygame.K_LEFT]:
            self.change_x = -4
        else:
            self.change_x = 0

        if self.rect.right >= DISPLAY_WIDTH:
            self.rect.right = DISPLAY_WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0


class Block(pygame.sprite.Sprite):
    def __init__(self, display, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(BLOCK_WEAK)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        pygame.draw.rect(display, BLOCK_WEAK, [self.rect.x, self.rect.y,
                                               self.rect.width, self.rect.height])

    # def update(self):
    #     pass
        # if self.hit == 1:
        #     self.color = BLOCK_OK
        # elif self.hit == 2:
        #     self.color = BLOCK_WEAK
        # else:
        #     self.kill()


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, x_velo):
        self.rect.x += x_velo


class UFO(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(UFO_IMG_PATH)
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = DISPLAY_WIDTH + random.choice([10, 20, 30, 40])
        self.rect.y = 100
        self.radius = self.rect.width // 2
        self.change_x = random.randint(1, 2)  # velocity variable

    def update(self):
        self.rect.x -= self.change_x

        if self.rect.right <= 0:
            self.kill()


class Missile(pygame.sprite.Sprite):
    def __init__(self, display, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.change_y = 3
        self.image = pygame.Surface((MISSILE_WIDTH, MISSILE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        pygame.draw.rect(display, WHITE, [self.rect.x, self.rect.y,
                                          self.rect.width, self.rect.height])

    def update(self):
        self.rect.y -= self.change_y

        if self.rect.bottom <= 0:
            self.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.change_y = 2
        self.image = pygame.Surface((MISSILE_WIDTH, MISSILE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.radius = self.rect.height // 2
        pygame.draw.rect(self.image, WHITE, [self.rect.x, self.rect.y,
                                             self.rect.width, self.rect.height])

    def update(self):
        self.rect.y += self.change_y

        if self.rect.bottom >= DISPLAY_HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = EXPLOSION_LIST[0]
        self.rect = self.image.get_rect(center=center)
        # self.rect.center = center
        print(self.rect.center)
        self.frame = 0
        self.previous_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.kill_center = center

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.previous_update > self.frame_rate:
            self.previous_update = now
            self.frame += 1
        if self.frame == len(EXPLOSION_LIST):
            self.kill()
        else:
            self.image = EXPLOSION_LIST[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = self.kill_center
