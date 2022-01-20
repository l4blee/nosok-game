import sys

import pygame; pygame.init()

import config
from gamemap import Map
from character import Character

pygame.display.set_caption('NOSOK ADVENTURE')
screen = pygame.display.set_mode(config.SCREEN_SIZE)
screen.fill(pygame.color.Color('Black'))

clock = pygame.time.Clock()


with open('map.txt') as f:
    data = list(map(str.rstrip, f.readlines()))
    gamemap = Map(*data)

character = Character()

while 1:
    screen.fill(pygame.color.Color('Black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        character.update_state(event)
        gamemap.update(event)

    gamemap.render(screen)

    character.update()
    character.render(screen)

    pygame.display.flip()
    clock.tick(config.FPS)
