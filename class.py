import pygame
from pygame.locals import *

class Board(pygame.sprite.Sprite):
    def __init__(self, image_path: str, pos: pygame.Vector2):
        self.awake(image_path, pos)
        self.start()

    def awake(self, image_path: str, pos: pygame.Vector2):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def start(self):
        self.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]

    def update(self):
        pass

class Piece(pygame.sprite.Sprite):
    def __init__(self, image_path: str, pos: pygame.Vector23 ):
        self.awake(image_path, pos)
        self.start()

    def awake(self, image_path: str, pos: pygame.Vector2):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def start(self):
        pass