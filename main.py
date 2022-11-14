from miskibin import get_logger
from player import Player
import pygame
from socket import *
from pygame.locals import *
import numpy as np
from copy import deepcopy
from pathlib import Path
import os
import json

LABELS_PATH = Path("data/labels").resolve()
SCREENS_PATH = Path("data/images").resolve()

WIDTH, HEIGHT = 960, 640
FPS = 120
PLAYERS_NUM = 2
FRAME = 0


def make_screen_shot(screen, players: pygame.sprite.Group):
    global FRAME, LABELS_PATH, SCREENS_PATH
    FRAME += 1
    img_path = os.path.join(SCREENS_PATH, f"{FRAME}.png")
    label_path = os.path.join(LABELS_PATH, f"{FRAME}.json")
    os.makedirs(SCREENS_PATH, exist_ok=True)
    os.makedirs(LABELS_PATH, exist_ok=True)
    label = []
    for player in players:
        if player.name == "player":
            coord = []
            coord += player.rect.topleft
            coord += player.rect.size
            label.append(coord)
    # normalize label
    if label:
        label = np.array(label)
        label = label / np.array([WIDTH, HEIGHT, WIDTH, HEIGHT])
    else:
        label = np.array([0, 0])
    json.dump(label.tolist(), open(label_path, "w"))
    pygame.image.save(screen, img_path)


def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Basic Pong")

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    # blue background
    background.fill((0, 0, 255))
    players = pygame.sprite.Group()
    for player_num in range(PLAYERS_NUM):
        # randomize player position
        name = np.random.choice(["player.png", "enemy.png"])
        angle = np.random.uniform(0, 2 * np.pi)
        z = np.random.randint(3, 5)
        position = (
            np.random.randint(0, WIDTH - 100),
            np.random.randint(0, HEIGHT - 200),
        )
        width = np.random.randint(50, 150)
        player = Player(
            name=name,
            vector=(angle, z),
            size=(width, 2 * width),
            position=position,
            index=player_num,
        )
        players.add(player)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    # Initialise clock
    clock = pygame.time.Clock()

    # Event loop
    while True:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        for player in players:
            player.update(players)
        for player in players:
            player.move()
        screen.blit(background, (0, 0))
        players.draw(screen)
        # for player in players:
        #    player.draw_rect(screen)

        pygame.display.flip()
        make_screen_shot(screen, players)


if __name__ == "__main__":
    main()
