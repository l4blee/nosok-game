import logging
import pygame; pygame.init()
import config
import models
import sys
from math import ceil

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s:'
                           '\t%(message)s',
                    datefmt='%y.%b.%Y %H:%M:%S')

logger = logging.getLogger('main')

screen = pygame.display.set_mode(config.SCREEN_SIZE)
screen.fill(pygame.color.Color('Black'))

clock = pygame.time.Clock()

chunk_pix_size = config.CHUNK_SIZE * config.TILE_SIZE
chunks_amount = [ceil(i / chunk_pix_size) for i in config.SCREEN_SIZE]
del chunk_pix_size

chunks = []
for x in range(chunks_amount[0]):
    for y in range(chunks_amount[1]):
        chunks.append(models.Chunk(x, y))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for i in chunks:
        i.render()

    pygame.display.flip()
    clock.tick(config.FPS)
