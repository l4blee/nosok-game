from enum import Enum
import pygame
from PIL import Image


class State(Enum):
    IDLE = 0
    WALK = 1


class Character:
    def __init__(self):
        self.state: State = State['IDLE']
        self.tick: float = 0

        self.load()

    def load(self):
        # Loading assets for idle state
        idle = Image.open(r'assets\char\Idle.png').convert('RGB')
        side = idle.height

        steps = idle.width // side
        idle_states = []
        for i in range(steps):
            img = idle.crop((side * i, 0, side * (i + 1), side))
            img = img.resize((64, 64))

            idle_states.append(
                pygame.image.frombuffer(img.tobytes(),
                                        img.size,
                                        img.mode)
                )

        # Loading assets for walking state
        walk = Image.open(r'assets\char\Walk.png').convert('RGBA')
        side = walk.height

        steps = walk.width // side
        walk_states = []
        for i in range(steps):
            img = idle.crop((side * i, 0, side * (i + 1), side))
            img = img.resize((64, 64))

            walk_states.append(
                pygame.image.fromstring(img.tobytes(),
                                        img.size,
                                        img.mode)
                )

        self.walk_states = walk_states
        self.idle_states = idle_states

    def update_state(self, event):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w] or pressed[pygame.K_a] or\
                pressed[pygame.K_s] or pressed[pygame.K_d]:
            state = State['WALK']
        else:
            state = State['IDLE']

        if state != self.state:
            self.tick = 0

        self.state = state

    def update(self):
        self.tick += 1 / 10
        self.tick = self.tick % len(
            eval(f'self.{self.state.name.lower() + "_states"}')
        )

    def render(self, screen):
        image = eval(f'self.{self.state.name.lower() + "_states"}')[int(self.tick)]
        image.set_colorkey(image.get_at((0, 0)))

        screen.blit(
            image,
            (screen.get_width() // 2 - image.get_width() // 2,
             screen.get_height() // 2 - image.get_height() // 2)
        )
