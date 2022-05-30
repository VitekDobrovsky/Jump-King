import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()

        self.image = pygame.image.load('../graphics/character/idle/1.png')
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'idle'
        self.facing_right = True

        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_ground:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.x > 0 and self.status != 'jump':
            self.status = 'right'
        elif self.direction.x < 0 and self.status != 'jump':
            self.status = 'left'
        elif self.direction.y > 0 and self.status != 'idle':
            self.status = 'fall'
        else:
            self.status = 'idle'

    def animate(self):
        path = '../graphics/character/idle/1.png'

        self.frame_index += self.animation_speed
        if self.frame_index >= 6:
            self.frame_index = 0

        if self.status == 'right':
            path = RUN_FRAMES[int(self.frame_index)]
        elif self.status == 'left':
            path = RUN_FRAMES[int(self.frame_index)]
        elif self.status == 'fall':
            path = '../graphics/character/fall/fall.png'
        elif self.status == 'jump':
            path = JUMP_FRAMES[int(self.frame_index)]
        elif self.status == 'idle':
            path = IDLE_FRAMES[int(self.frame_index)]

        self.image = pygame.image.load(path)
        if not self.facing_right:
            fliped_image = pygame.transform.flip(self.image,True,False)
            self.image = fliped_image

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def update(self):
        self.input()
        self.get_status()
        self.animate()
