# Example file showing a circle moving on screen
import pygame
from random import randint

# pygame setup
pygame.init()
screen_height = 720
screen_width =1280
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0

Square_side = 20

Grid = ((screen_width//Square_side)-1, (screen_height//Square_side)-1)

starting_x = 6

starting_y = 4

#### CLASSES ####

class Food:
    def __init__(self, Grid,snake_body):
        while True:
            self.x = randint(0, Grid[0])
            self.y = randint(0, Grid[1])
            if (self.x, self.y) not in snake_body:
                break

    def respawn(self, Grid, snake):
        while True:
            self.x = randint(0, Grid[0])
            self.y = randint(0, Grid[1])
            if (self.x, self.y) not in snake:
                break
    def location(self):
        return (self.x,self.y)



class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body = [(x, y)]

    def move(self, mov_x, mov_y, food, grid):
        # update snake position
        self.x += mov_x
        self.y += mov_y
        if self.x < 0 or self.y < 0 or self.x > grid[0] or self.y > grid[1]:
            return None
        if self.x == food[0] and self.y == food[1]:
            self.grow()
        
        self.body.insert(0, (self.x, self.y))
        self.body.pop()
        return self.body  


    def grow(self):
        self.body.append(self.body[-1])

 ################################################

snake = Snake(starting_x,starting_y)

food = Food(Grid,snake.body)

movement = [1,0]

move_delay = 0.1  # seconds between moves
time_since_move = 0


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    hit_wall = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        movement = [0,-1]
    if keys[pygame.K_s]:
        movement = [0,1]
    if keys[pygame.K_a]:
        movement = [-1,0]
    if keys[pygame.K_d]:
        movement = [1,0]

    if time_since_move >= move_delay:
        time_since_move = 0
        hit_wall = snake.move(movement[0], movement[1], food.location(), Grid)
        if hit_wall is None:
            break
        if snake.x == food.x and snake.y == food.y:
            snake.grow()
            food.respawn(Grid, snake.body)
    
    for segment in snake.body:
        pygame.draw.rect(screen, "green", (segment[0]*Square_side, segment[1]*Square_side, Square_side, Square_side))

    food_pos = food.location()    
    pygame.draw.rect(screen, "red",(food_pos[0]*Square_side, food_pos[1]*Square_side, Square_side, Square_side) )

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(120) / 1000  # delta time in seconds
    time_since_move += dt


pygame.quit()
