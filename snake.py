import pygame
from pygame.locals import *
import random as r

class Snake:
    def __init__(self, parent_screen):
        self.block = pygame.image.load("resources/block.jpg").convert()
        self._x = 100
        self._y = 100
        self.parent_surface = parent_screen

    def move_left(self):
        self._x -= 10
        self.draw()
    
    def move_right(self):
        self._x += 10
        self.draw()
    
    def move_up(self):
        self._y -= 10
        self.draw()
    
    def move_down(self):
        self._y += 10
        self.draw()



    def draw(self):
        self.parent_surface.fill((r.randrange(0,255), r.randrange(0,255), r.randrange(0,255)))
        self.parent_surface.blit(self.block, (self._x, self._y))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 1000))
        self.surface.fill((255, 255, 255))
        self.snake = Snake(self.surface)
        self.snake.draw()
    
    def run(self):
        running  = True

        while running:
            for event in pygame.event.get():

                if event.type == KEYDOWN:      
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()

                elif event.type == QUIT:
                    running = False



if __name__ == "__main__":
    game = Game()
    game.run()