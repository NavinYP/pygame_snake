import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH = 800
HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (255, 255, 255)
FOOD_COLOR = (255, 0, 0)

# Set up the display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the snake and food
snake_pos = [100, 50]
food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
snake_body = [[100, 50], [90, 50], [80, 50]]

# Set up the direction
direction = 'RIGHT'

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

    # Move the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    elif direction == 'DOWN':
        snake_pos[1] += 10
    elif direction == 'LEFT':
        snake_pos[0] -= 10
    elif direction == 'RIGHT':
        snake_pos[0] += 10

    # Add to the snake body if it eats food
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
    else:
        snake_body.pop()

    # Add new segment to the body
    snake_body.insert(0, list(snake_pos))

    # Draw everything
    win.fill(BACKGROUND_COLOR)
    for pos in snake_body:
        pygame.draw.rect(win, SNAKE_COLOR, (pos[0], pos[1], 10, 10))
    pygame.draw.rect(win, FOOD_COLOR, (food_pos[0], food_pos[1], 10, 10))

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    time.sleep(0.1)

    # Check for collisions with the wall or itself
    if snake_pos[0] < 0 or snake_pos[0] > WIDTH - 10:
        print('Game Over')
        break
    if snake_pos[1] < 0 or snake_pos[1] > HEIGHT - 10:
        print('Game Over')
        break
    for block in snake_body[1:]:
        if block == snake_pos:
            print('Game Over')
            break

# Quit Pygame
pygame.quit()