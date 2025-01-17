import pygame
from pygame.locals import *
import random

class Board(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2):
        self.awake(pos)
        self.start()

    def awake(self, pos: pygame.Vector2):
        super().__init__()
        self.image = pygame.image.load("Assets/board.png")
        self.org_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.score = 0

    def start(self):
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        self.spawn_piece()
        self.draw_pieces()

    def update(self, inputs):
        """
        When a key is pressed, the board should move all the pieces so that they are stacked on the direction of the key pressed.
        Numbers of same size should be merged and added together.
        """
        
        if inputs[pygame.K_w] or inputs[pygame.K_UP]:
            self.move("up")
        elif inputs[pygame.K_s] or inputs[pygame.K_DOWN]:
            self.move("down")
        elif inputs[pygame.K_a] or inputs[pygame.K_LEFT]:
            self.move("left")
        elif inputs[pygame.K_d] or inputs[pygame.K_RIGHT]:
            self.move("right")

        self.draw_pieces()

    def move(self, direction: str):
        """
        Makes the pieces slide all the way in the specified direction. If two pieces of the same size collide, they should merge.
        """
        if direction == "up":
            for x in range(4):
                for y in range(1,4):
                    if self.board[y][x]:
                        for i in range(y, 0, -1):
                            if self.board[i-1][x] == 0:
                                self.board[i-1][x] = self.board[i][x]
                                self.board[i][x] = 0
                            elif self.board[i-1][x] == self.board[i][x]:
                                self.board[i-1][x] *= 2
                                self.board[i][x] = 0
                                break
                            else:
                                break
        elif direction == "down":
            for x in range(4):
                for y in range(2, -1, -1):
                    if self.board[y][x]:
                        for i in range(y, 3):
                            if self.board[i+1][x] == 0:
                                self.board[i+1][x] = self.board[i][x]
                                self.board[i][x] = 0
                            elif self.board[i+1][x] == self.board[i][x]:
                                self.board[i+1][x] *= 2
                                self.board[i][x] = 0
                                break
                            else:
                                break
        elif direction == "left":
            for y in range(4):
                for x in range(1,4):
                    if self.board[y][x]:
                        for i in range(x, 0, -1):
                            if self.board[y][i-1] == 0:
                                self.board[y][i-1] = self.board[y][i]
                                self.board[y][i] = 0
                            elif self.board[y][i-1] == self.board[y][i]:
                                self.board[y][i-1] *= 2
                                self.board[y][i] = 0
                                break
                            else:
                                break
        elif direction == "right":
            for y in range(4):
                for x in range(2, -1, -1):
                    if self.board[y][x]:
                        for i in range(x, 3):
                            if self.board[y][i+1] == 0:
                                self.board[y][i+1] = self.board[y][i]
                                self.board[y][i] = 0
                            elif self.board[y][i+1] == self.board[y][i]:
                                self.board[y][i+1] *= 2
                                self.board[y][i] = 0
                                break
                            else:
                                break

        self.spawn_piece()
        self.update_score()

        """Check if the player has lost by checking if a new move is possible"""
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == 0:
                    return
                if y > 0 and self.board[y][x] == self.board[y-1][x]:
                    return
                if y < 3 and self.board[y][x] == self.board[y+1][x]:
                    return
                if x > 0 and self.board[y][x] == self.board[y][x-1]:
                    return
                if x < 3 and self.board[y][x] == self.board[y][x+1]:
                    return
        
        # Create pygame event to close the game
        pygame.event.post(pygame.event.Event(QUIT))

    def update_score(self):
        self.score = 0
        for row in self.board:
            for num in row:
                self.score += num
        print(self.score)

    def spawn_piece(self):
        """
        Spawns a new piece in a random empty spot.
        """
        empty_spots = []
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == 0:
                    empty_spots.append((y,x))

        if empty_spots:
            spot = empty_spots[pygame.time.get_ticks() % len(empty_spots)]
            self.board[spot[0]][spot[1]] = random.choice([2,2,2,4])
        

    def draw_pieces(self):
        self.image = self.org_image.copy()

        y = 0
        for row in self.board:
            x = 0
            for num in row:
                if num:
                    piece = Piece("Assets/piece.png", pygame.Vector2(10+68*x,10+68*y), num)
                    self.image.blit(piece.image, piece.rect)            
                x += 1
            y += 1



class Piece(pygame.sprite.Sprite):
    def __init__(self, image_path: str, pos: pygame.Vector2, value: int):
        self.awake(image_path, pos, value)
        self.start()

    def awake(self, image_path: str, pos: pygame.Vector2, value: int):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.value = value

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 20)

    def start(self):
        self.image.blit(self.font.render(str(self.value), True, "White"), (0,0))