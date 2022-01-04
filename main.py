import pygame; pygame.init()
import sys
from math import ceil
import config
import gamemap
from character import Character

pygame.display.set_caption('NOSOK ADVENTURE')
screen = pygame.display.set_mode(config.SCREEN_SIZE)
screen.fill(pygame.color.Color('Black'))

clock = pygame.time.Clock()

chunk_pix_size = config.CHUNK_SIZE * config.TILE_SIZE
chunks_amount = [ceil(i / chunk_pix_size) for i in config.SCREEN_SIZE]
del chunk_pix_size

chunks = []
for x in range(chunks_amount[0]):
    for y in range(chunks_amount[1]):
        chunks.append(gamemap.Chunk(x, y))

character = Character()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        character.update_state(event)

    for i in chunks:
        i.render(screen)

    character.update()
    character.render(screen)

    pygame.display.flip()
   
    clock.tick(config.FPS)
