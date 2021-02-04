import pygame
import sys
import random
from pygame.math import Vector2
import tkinter as tk
from tkinter import messagebox

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] #the starting position of the snake
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
        
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)    #create a rectangle
            pygame.draw.rect(screen, (217, 26, 26), block_rect)             #draw the rectangle

    def move_snake(self):
        ''' 1. A new block it added to the snake, everytime the snake collects a new bug. 
            2. Simulates the illusion of moving(moves through the walls as well)
        The head is moved to a new block. 
        The next block gets the position where the head used to be.
        Each block is moved to the position of the block that used to be before it     
        '''
        if self.new_block == True:  
            body_copy = self.body[:]   #copy the entire body of the snake
            body_copy.insert(0, body_copy[0] + self.direction)    #adding a new position at the front, moving forward
            body_copy[0] = Vector2(body_copy[0].x % cell_number, body_copy[0].y % cell_number)  #by using modulo, once the snake is over the borders, reset the snake-head position to 0 accordingly to x/y corrdinates
            self.body = body_copy[:]     
            self.new_block = False     
        else:   #moving the snake without adding anything to it
            body_copy = self.body[:-1]    #from the first to the one before the last, the first 2 elements
            body_copy.insert(0, body_copy[0] + self.direction)
            body_copy[0] = Vector2(body_copy[0].x % cell_number, body_copy[0].y % cell_number)
            self.body = body_copy[:]     

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False


class BUG:
    def __init__(self):
        self.randomize()
        
    def draw_bug(self):
        bug_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)  #create a rectangle
        pygame.draw.rect(screen, (17, 156, 31), bug_rect)   #draw the rectangle

    def randomize(self):     #creats random positions for the bugs
        self.x = random.randint(0, cell_number -1)   
        self.y = random.randint(0, cell_number -1)
        self.pos = Vector2(self.x, self.y)
    

class MAIN:   #connects the bugs and snake 
    def __init__(self):
        self.snake = SNAKE()  
        self.bug = BUG()

    def update(self):    
        self.snake.move_snake()
        self.check_collision()    
        self.check_fail()
    

    def draw_elements(self):
        self.bug.draw_bug()
        self.snake.draw_snake()
        self.draw_score()
        

    def check_collision(self):
        ''' If the bug and snake-head have the same position, then the snake eats the bug
        Reposition the bug
        Add another block to the snake
        '''
        if self.bug.pos == self.snake.body[0]:
            self.bug.randomize()  
            self.snake.add_block()  
            
        for block in self.snake.body[1:]:  #if the food appears on top of the snake
            if block == self.bug.pos:
                self.bug.randomize()

    def check_fail(self):   #check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]: 
                res = message_box('You Lost!', 'Play again...')     
                if res:
                    self.reset()
                else:
                    self.game_over()
                break        
                
                
    def reset(self):
        self.snake.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.snake.direction = Vector2(1,0)
        self.snake.new_block = False
        self.bug.draw_bug()
        self.snake.draw_snake()
        self.draw_score()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_score(self):
        score_text = str(len(self.snake.body) -3)
        score_surface = game_font.render(f"Score: {score_text}", True, (255, 255, 255))
        score_x = int(cell_size * cell_number - 300)
        score_y = int(cell_size * cell_number - 550)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        screen.blit(score_surface, score_rect)

    

    
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    res = messagebox.askyesno(subject, content)
    try:
        root.destroy()
        return res
    except:
        pass  


pygame.init()    
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock() 

game_font = pygame.font.Font(None, 50)


SCREEN_UPDATE = pygame.USEREVENT   
pygame.time.set_timer(SCREEN_UPDATE,100)  #create timer, triggered every 100 ms

main_game = MAIN()

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  #closing the window by clicking on x 
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_LEFT:    #changing the direction of the snake
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y !=1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
    
      
    screen.fill((0, 0, 0))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(10)  #framerate (the game will not run faster than 10 frames per second)
    