import pygame
from enum import Enum
from PIL import Image, ImageOps

SCALE = 1.7


class Orientation(Enum):
    RIGHT = 0
    LEFT = 1


class State(Enum):
    IDLE = 0
    WALK = 1


class Character:
    def __init__(self):
        self.state: State = State['IDLE']
        self.orientation: Orientation = Orientation['RIGHT']
        self.tick: float = 0

        self.load()

    def load(self):
        path = 'assets/character/'

        # Loading assets for idle state
        idle = Image.open(f'{path}Idle.png').convert('RGBA')
        side = idle.height

        steps = idle.width // side
        idle_states_right, idle_states_left = [], []
        for i in range(steps):
            img = idle.crop((side * i, 0, side * (i + 1), side))
            img = img.resize((int(side * SCALE), int(side * SCALE)))

            idle_states_right.append(
                pygame.image.frombuffer(img.tobytes(),
                                        img.size,
                                        img.mode)
            )

            img = ImageOps.mirror(img)

            idle_states_left.append(
                pygame.image.frombuffer(img.tobytes(),
                                        img.size,
                                        img.mode)
            )

        # Loading assets for walking state
        walk = Image.open(f'{path}Walk.png').convert('RGBA')
        side = walk.height

        steps = walk.width // side
        walk_states_right, walk_states_left = [], []
        for i in range(steps):
            img = walk.crop((side * i, 0, side * (i + 1), side))
            img = img.resize((int(side * SCALE), int(side * SCALE)))

            walk_states_right.append(
                pygame.image.fromstring(img.tobytes(),
                                        img.size,
                                        img.mode)
                )

            img = ImageOps.mirror(img)

            walk_states_left.append(
                pygame.image.frombuffer(img.tobytes(),
                                        img.size,
                                        img.mode)
            )

        self.walk_states_right = walk_states_right
        self.walk_states_left = walk_states_left

        self.idle_states_right = idle_states_right
        self.idle_states_left = idle_states_left

    def update_state(self, event):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w] or pressed[pygame.K_a] or\
                pressed[pygame.K_s] or pressed[pygame.K_d]:
            state = State['WALK']

            if pressed[pygame.K_d] or pressed[pygame.K_a]:
                orient = ['RIGHT', 'LEFT'][pressed[pygame.K_a]]
                self.orientation = Orientation[orient]
        else:
            state = State['IDLE']

        if state != self.state:
            self.tick = 0

        self.state = state

    def update(self):
        self.tick += 1 / 10
        self.tick %= len(
            eval(f'self.{self.state.name.lower()}'
                 '_states_'
                 f'{self.orientation.name.lower()}')
        )

    def render(self, screen):
        image = eval(f'self.{self.state.name.lower()}'
                     '_states_'
                     f'{self.orientation.name.lower()}')[int(self.tick)]
        image.set_colorkey(image.get_at((0, 0)))

        screen.blit(
            image,
            (screen.get_width() // 2 - image.get_width() // 2,
             screen.get_height() // 2 - image.get_height() // 2)
        )
