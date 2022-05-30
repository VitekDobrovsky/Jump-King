import pygame
from settings import *
from tile import Tile
from player import Player


class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()

        # groups
        self.obstacle = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        # map
        self.create_map()
        self.world_shift = 0

        self.current_x = 0

    def create_map(self):

        for row_index,row in enumerate(level_map):
            for col_index,col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if col == 'X':
                    tile = Tile((x,y),TILE_SIZE,)
                    self.obstacle.add(tile)
                if col == 'P':
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)

    def scroll_y(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x



        if player_x < WIDTH / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > WIDTH - (WIDTH / 4) and direction_x > 0:
            self.world_shift = - 8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_move_collision(self):
        player = self.player.sprite

        player.rect.x += player.direction.x * player.speed

        for sprite in self.obstacle.sprites():
            if player.rect.colliderect(sprite.rect):

                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

                elif player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right < self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_move_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.obstacle.sprites():
            if player.rect.colliderect(sprite.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def run(self):
        self.obstacle.update(self.world_shift)
        self.obstacle.draw(self.screen)

        self.player.update()
        self.player.draw(self.screen)
        self.horizontal_move_collision()
        self.vertical_move_collision()
        self.scroll_y()
