import pygame
from pygame.locals import *

from board import Board

WIDTH, HEIGHT = 400, 450
FPS = 24

class App:
    def __init__(self):
        self.awake()
        self.start()

    def awake(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048")
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.key_codes = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        self.inputs = {}
        for key_code in self.key_codes:
            self.inputs[key_code] = 0

    def start(self):
        self.all_sprites.add(Board(pygame.Vector2(50,100)))
        pass

    def handle_events(self): 
        for key_code in self.key_codes:
            self.inputs[key_code] = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                for key_code in self.key_codes:
                    if event.key == key_code:
                        self.inputs[key_code] = 1

    def update(self):
        self.all_sprites.update(self.inputs)

    def draw(self):
        self.screen.fill("Black")
        self.all_sprites.draw(self.screen)
        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def restart(self):
        self.awake()
        self.start()
        self.run()

    def play_step(self, action):
        print(action)
        # Convert action to inputs
        self.inputs = {key: 0 for key in self.key_codes}
        if action[0] == 1:
            self.inputs[pygame.K_w] = 1
        elif action[1] == 1:
            self.inputs[pygame.K_s] = 1
        elif action[2] == 1:
            self.inputs[pygame.K_a] = 1
        elif action[3] == 1:
            self.inputs[pygame.K_d] = 1

        self.handle_events()
        self.update()
        self.draw()
        self.clock.tick(FPS)

        reward = 0
        done = False
        score = self.all_sprites.sprites()[0].score

        if not self.running:
            done = True
            reward = -10  # Negative reward for losing

        return reward, done, score

    def reset(self):
        self.awake()
        self.start()


if __name__ == "__main__":
    app = App()
    app.run()
