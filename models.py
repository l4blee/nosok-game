import pygame
import config
from utils import load_image
from enum import Enum


class Textures(Enum):
    GRASS = pygame.transform.scale(load_image('grass.png'),
                                   (config.TILE_SIZE, config.TILE_SIZE))


class Chunk:
    def __init__(self, x: int, y: int):
        self.size = config.CHUNK_SIZE
        self.x, self.y = x, y

    def render(self):
        screen = pygame.display.get_surface()
        for y in range(self.size):
            for x in range(self.size):
                screen.blit(Textures.GRASS.value,
                            ((self.x * self.size * config.TILE_SIZE) + x * config.TILE_SIZE,
                             (self.y * self.size * config.TILE_SIZE) + y * config.TILE_SIZE))
