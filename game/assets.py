import pygame
from settings import TILE_SIZE, PIC_SIZE


class Assets:
    def __init__(self):
        self.floor = pygame.transform.scale(
            pygame.image.load("images/floor.png").convert_alpha(),
            (TILE_SIZE, TILE_SIZE)
        )
        self.wall = pygame.transform.scale(
            pygame.image.load("images/wall.png").convert_alpha(),
            (TILE_SIZE, TILE_SIZE)
        )
        self.box = pygame.transform.scale(
            pygame.image.load("images/box.png").convert_alpha(),
            (TILE_SIZE, TILE_SIZE)
        )
        self.box_on_goal = pygame.transform.scale(
            pygame.image.load("images/box_on_goal.png").convert_alpha(),
            (TILE_SIZE, TILE_SIZE)
        )
        self.goal = pygame.transform.scale(
            pygame.image.load("images/goal.png").convert_alpha(),
            (PIC_SIZE, PIC_SIZE)
        )
        self.player = pygame.transform.scale(
            pygame.image.load("images/player.png").convert_alpha(),
            (TILE_SIZE, TILE_SIZE)
        )

        self.theme = pygame.image.load("images/theme.png").convert_alpha()
        self.theme = pygame.transform.scale(
            pygame.image.load("images/theme.png").convert_alpha(),
            (TILE_SIZE * 6, TILE_SIZE * 4)
        )

