from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *

SCREEN_WIDTH = 350
SCREEN_HEIGHT = 600
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 200

Clock = pygame.time.Clock()


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('redbird-upflap.png').convert_alpha(),
                       pygame.image.load('redbird-midflap.png').convert_alpha(),
                       pygame.image.load('redbird-downflap.png').convert_alpha()]

        self.speed = SPEED
        self.angle = 0

        self.current_image = 0

        self.image = pygame.image.load('redbird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2 - 12
        self.rect[1] = SCREEN_HEIGHT / 2 - 12

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = pygame.transform.rotate(self.images[self.current_image], self.angle)

        self.speed += GRAVITY
        self.rect[1] += self.speed
        self.angle -= 5
        if self.angle <= -35:
            self.angle = -35

    def bump(self):
        self.speed = -(SPEED + 2)
        self.angle = 45


class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

class Pipe(pygame.sprite.Sprite):

    def __init__(self, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.load.image('pipe-green.png')
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def is_bird_off_screen(sprite):
    return sprite.rect[1] < 0

def collide(group1, group2):
    return pygame.sprite.groupcollide(group1, group2, False, False, pygame.sprite.collide_mask)

def gameOver():
    GAME_OVER = pygame.image.load('gameover.png')
    screen.blit(GAME_OVER, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 30))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)


def game():
    while True:
        Clock.tick(24)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bird.bump()

        screen.blit(BACKGROUND, (0, 0))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDTH - 20)
            ground_group.add(new_ground)

        if is_bird_off_screen(bird_group.sprites()[0]):
            gameOver()
            pygame.time.wait(1000)
            break

        bird_group.update()
        ground_group.update()

        bird_group.draw(screen)
        ground_group.draw(screen)

        if collide(bird_group, ground_group):
            gameOver()
            pygame.time.wait(1000)
            break

        pygame.display.update()


game()
