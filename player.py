import os
import pygame
import numpy as np
from miskibin import get_logger
from typing import Literal
import math
from logging import Logger


def load_png(name):
    """Load image and return image object"""
    fullname = os.path.join("data", name)
    image = pygame.image.load(fullname)
    return image


class Player(pygame.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(
        self,
        vector: tuple,
        size: tuple = (200, 400),
        position: tuple = (0, 0),
        name: Literal["player.png", "enemy.png"] = "player.png",
        logger: Logger = get_logger(lvl=10),
        index: int = 0,
    ):
        pygame.sprite.Sprite.__init__(self)
        self.logger = logger
        self.name = name.split(".")[0]
        self.image = load_png(name)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        self.index = index
        self.h = 10
        self.rect.topleft = position

    def update(self, players):
        self.calc_vector(players)
        # self.__draw_rect(pygame.display.get_surface())

    def draw_rect(self, screen):
        x, y = self.rect.topleft
        w, h = self.rect.size
        # draw red rectangle around the player
        pygame.draw.rect(screen, (255, 0, 0), (x, y, w, h), 1)

    def __update_angle(self, angle: float, player_rect: pygame.Rect):
        if (
            abs(self.rect.left - player_rect.right) < self.h
            or abs(self.rect.right - player_rect.left) < self.h
        ):
            self.logger.info(f"l r collision: plyer index: {self.index}")
            return (np.pi - angle) % (2 * np.pi)
        if (
            abs(self.rect.top - player_rect.bottom) < self.h
            or abs(self.rect.bottom - player_rect.top) < self.h
        ):
            self.logger.warning(f"top/bottom collision: plyer index: {self.index}")
            return -angle
        self.rect.topleft = np.random.randint(0, 500), np.random.randint(0, 300)
        return angle

    def move(self):
        (angle, z) = self.vector
        (dx, dy) = (z * np.cos(angle), z * np.sin(angle))
        moved = self.rect.move(dx, dy)
        self.rect = moved

    def calc_vector(self, players):
        (angle, z) = self.vector

        # change vector when hitting the top or bottom of the screen
        if self.rect.top < self.area.top or self.rect.bottom > self.area.bottom:
            angle = -angle
        # change vector when hitting the left or right of the screen
        elif self.rect.left < self.area.left or self.rect.right > self.area.right:
            angle = (np.pi - angle) % (2 * np.pi)
        # prevent collision with other players

        for player in players:
            if player != self and self.rect.colliderect(player.rect):
                angle = self.__update_angle(angle, player.rect)
        self.vector = (
            angle + np.random.random() / 100,
            z + (np.random.random() - 0.5) / 4,
        )
