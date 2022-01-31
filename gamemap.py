import config
from utils import load_image

import pygame
from enum import Enum


class Textures(Enum):
    ALIASES = {
        '#': 'GRASS',
        '.': 'DIRT'
    }

    GRASS = pygame.transform.scale(load_image('tiles/grass.png'),
                                   (config.TILE_SIZE, config.TILE_SIZE))
    DIRT = pygame.transform.scale(load_image('tiles/dirt.png'),
                                  (config.TILE_SIZE, config.TILE_SIZE))


class Tile(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, texture, *args):
        super().__init__(*args)

        self.image = texture.value
        self.rect = texture.value.get_rect()

        self.size = config.TILE_SIZE
        self.x, self.y = x, y

        self.rect = self.rect.move(x * self.size, y * self.size)

    def __repr__(self):
        return f'Tile(x={self.x}, y={self.y}, t={self.texture.name})'


class Chunk:
    def __init__(self, x: int, y: int, *tiles: list[Tile]):
        self.tiles = pygame.sprite.Group(*tiles)

        self.size = config.CHUNK_SIZE
        self.x, self.y = x, y

    def render(self, screen, offset_x, offset_y):
        for tile in self.tiles:
            coords = (self.x * self.size * config.TILE_SIZE + tile.x * tile.size + offset_x,
                      self.y * self.size * config.TILE_SIZE + tile.y * tile.size + offset_y)

            if 0 - config.TILE_SIZE // 2 < coords[0] < config.SCREEN_SIZE[0] or\
                    0 - config.TILE_SIZE // 2 < coords[1] < config.SCREEN_SIZE[1]:
                screen.blit(tile.image, coords)

    def __repr__(self):
        return f'Chunk(x={self.x}, y={self.y})'


class Map:
    def __init__(self, *data):
        self.offset_x, self.offset_y = 0, 0
        self.map: list[Chunk] = self.load_data(*data)

    def load_data(self, *data):
        chunks = []
        chunk_block = []
        for index, row in enumerate(data):
            chunk_steps = []
            for i in range(len(row) // config.CHUNK_SIZE):
                chunk_step = row[i * config.CHUNK_SIZE:(i + 1) * config.CHUNK_SIZE]
                chunk_steps.append(chunk_step)
            chunk_block.append(chunk_steps)

            # If block is completed
            if (index + 1) % config.CHUNK_SIZE == 0 and index > 0:
                chunks_total = []
                for i in range(len(chunk_block[0])):
                    chunk = []
                    for j in chunk_block:
                        chunk.append(j[i])

                    chunks_total.append(chunk)
                chunk_block = []

                chunk_row = []
                for chunk_y, str_chunk in enumerate(chunks_total):
                    tiles = []
                    for y, row in enumerate(str_chunk):
                        for x, str_tile in enumerate(row):
                            tile = Tile(x,
                                        y,
                                        eval(f'Textures.{Textures.ALIASES.value[str_tile]}'))
                            tiles.append(tile)

                    chunk = Chunk(chunk_y, len(chunks), *tiles)
                    chunk_row.append(chunk)

                chunks.append(chunk_row)

        return chunks

    def render(self, screen):
        for row in self.map:
            for chunk in row:
                chunk.render(screen, self.offset_x, self.offset_y)

    def update(self, event: pygame.event.Event):
        x, y = 0, 0

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            y = 1
        elif pressed[pygame.K_s]:
            y = -1

        if pressed[pygame.K_a]:
            x = 1
        elif pressed[pygame.K_d]:
            x = -1

        self.offset_x += x * config.STEP
        self.offset_y += y * config.STEP


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(config.SCREEN_SIZE)
    screen.fill(pygame.color.Color('Black'))

    with open('map.txt') as f:
        data = list(map(str.rstrip, f.readlines()))
        gamemap = Map(*data)

    for row in gamemap.map:
        for chunk in row:
            chunk.render(screen)

    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
