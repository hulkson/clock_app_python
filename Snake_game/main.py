import pygame
import random
import time

pygame.init()

width = 400
height = width
HEAD_COLOR = (30,171,157)
FOOD_COLOR = (255, 0, 0)

game_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

x = 200
y = 200
deltaX = 10
deltaY = 0
foodX = random.randrange(0, width) // 10 * 10
foodY = random.randrange(0, height) // 10 * 10

body_list = [(x, y)]

clock = pygame.time.Clock()

game_over = False
font = pygame.font.SysFont('monospace', 25)

def snake():
    global x, y, foodX, foodY, game_over
    x = (x + deltaX) % width
    y = (y + deltaY) % height

    if(x, y) in body_list:
        game_over = True
        return

    body_list.append((x, y))

    # check collision with food
    if(foodX == x and foodY == y):
        while ((foodX, foodY) in body_list):
            foodX = random.randrange(0, width) // 10 * 10
            foodY = random.randrange(0, height) // 10 * 10
    else:
        del body_list[0]

    game_screen.fill((0, 0, 0))
    score = font.render('Score: ' + str(len(body_list) - 1), True, ( 255, 255, 255))
    game_screen.blit(score, [0, 0])
    pygame.draw.rect(game_screen, FOOD_COLOR, [foodX, foodY, 10 ,10])
    
    for(i, j) in body_list:
        pygame.draw.rect(game_screen, HEAD_COLOR, [i, j, 10, 10])
    
    pygame.display.update()

while True:
    if(game_over):
        game_screen.fill((0, 0, 0))
        msg = font.render('GAME OVER', True, (255, 255, 255))
        game_screen.blit(msg, [width // 3, height // 3])
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        quit()

    events = pygame.event.get()
    for event in events:
        if (event.type == pygame.QUIT):
            pygame.quit()
            quit()

        # check button is press
        if (event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_LEFT) and (deltaX != 10):
                deltaX = -10
                deltaY = 0
            elif (event.key == pygame.K_RIGHT) and (deltaX != -10):
                deltaX = 10
                deltaY = 0
            elif (event.key == pygame.K_UP) and (deltaY != 10):
                deltaX = 0
                deltaY = -10
            elif (event.key == pygame.K_DOWN) and (deltaY != -10):
                deltaX = 0
                deltaY = 10
            else: 
                continue

    if (not events):
        snake()
    clock.tick(10)