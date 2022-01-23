import pygame
from pygame.locals import *
import random as r
import time
from CONSTANTS import * # local file to handle all the constant values


# self.parent_surface.fill((r.randrange(0,255), r.randrange(0,255), r.randrange(0,255)))
BACKGROUND_COLOR = (120, 120, 50)

class Apple:
    def __init__(self, parent_surface):
        self.parent_surface = parent_surface
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self._x = r.randrange(0, 1000, 40)
        self._y = r.randrange(0, 800, 40)

    def move_apple(self):
        self._x = r.randrange(0, 1000, 40)
        self._y = r.randrange(0, 800, 40)
        self.draw_apple()

    def draw_apple(self):
        self.parent_surface.blit(self.apple,(self._x, self._y))
        pygame.display.flip()

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self._x = [SIZE]*length
        self._y = [SIZE]*length
        self.parent_surface = parent_screen
        self.direction = 'right'

    def move_left(self):
        self.direction = 'left'
    
    def move_right(self):
        self.direction = 'right'
    
    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
       self.direction = 'down'

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self._x[i] = self._x[i-1]
            self._y[i] = self._y[i-1]

        if self.direction == 'right':
            self._x[0] += SIZE
        if self.direction == 'left':
            self._x[0] -= SIZE
        if self.direction == 'up':
            self._y[0] -= SIZE
        if self.direction == 'down':
            self._y[0] += SIZE
        
        self.draw()

    def increase_length(self):
        self.length += 1
        self._x.append(SIZE)
        self._y.append(SIZE)


    def draw(self):
        #self.parent_surface.fill((r.randrange(0,255), r.randrange(0,255), r.randrange(0,255))) // To be implemented later
        #self.parent_surface.render_background()
        for i in range(self.length):
            self.parent_surface.blit(self.block, (self._x[i], self._y[i]))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init() # initializing pygame module for display
        pygame.mixer.init() # initialising pygame module for sound
        self.surface = pygame.display.set_mode(SURFACE_SIZE) # setting up the dimentions of game window 
        #self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface, 1)
        self.snake.draw() # drawing snake on the screen
        self.apple = Apple(self.surface)
        self.apple.draw_apple() #drawing apple on the screen
        self.play_music() #playing backgroung music
    
    def is_collision(self, s_x, a_x, s_y, a_y):
        if s_x >= a_x and s_x < a_x+SIZE:
            if s_y >= a_y and s_y < a_y+SIZE:
                return True

    def score(self):
        font = pygame.font.SysFont("arial", SCORE_TEXT_SIZE)
        score = font.render(f'Score: {self.snake.length}', True, SCORE_TEXT_COLOR)
        self.surface.blit(score, (800, 10))

    def render_background(self):
        bg = pygame.image.load('resources/background.jpg').convert()
        self.surface.blit(bg, (0,0))


    def play_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()


    def play_sound(self, sound):
        Sound = pygame.mixer.Sound(f'resources/{sound}.mp3')
        pygame.mixer.Sound.play(Sound)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw_apple()
        self.score()
        pygame.display.flip()


        if self.is_collision(self.snake._x[0], self.apple._x, self.snake._y[0],self.apple._y): # collision between snake and apple
            #print("Collision occured")
            self.play_sound('ding')
            self.snake.increase_length()
            self.apple.move_apple()

        # collion between snake and its body part
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake._x[0], self.snake._x[i], self.snake._y[0], self.snake._y[i]):
                self.play_sound('crash')
                raise ValueError("Game Over")

        #collision with the walls
        if (self.snake._x[0] == 0 or self.snake._x[0]==1000)| (self.snake._y[0]==0 or self.snake._y[0] == 800):
            self.play_sound('crash')
            raise ValueError("Game Over")

            
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont("arial", GAME_OVER_TEXT_SIZE)
        GameOver = font.render(f'Game Over. Score: {self.snake.length}', True, GAME_OVER_TEXT_COLOR)
        self.surface.blit(GameOver, (400, 400))
        restart = font.render(f'Press Enter to continue', True, GAME_OVER_TEXT_COLOR)
        self.surface.blit(restart, (400, 420))
        pygame.display.flip()
        pygame.mixer.music.pause()


    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        
        running  = True
        pause = False
        while running:
            for event in pygame.event.get():

                if event.type == KEYDOWN:      
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.play()
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_SPACE:
                            pause = True

                elif event.type == QUIT:
                    running = False
            
            try:
                if not pause:
                    self.play()
            except ValueError:
                self.show_game_over()
                self.reset()
                pause = True

            time.sleep(0.3)


if __name__ == "__main__":
    game = Game()
    game.run()