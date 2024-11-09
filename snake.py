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

# Main menu variables
menu_active = True

# Game variables
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

        # Handle menu input
        if menu_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_active = False

        else:  # Game is active
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

            # Handle game over
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and menu_active is False:  # Restart the game
                    snake_pos = [100, 50]
                    food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
                    snake_body = [[100, 50], [90, 50], [80, 50]]
                    direction = 'RIGHT'
                    menu_active = True

    # Draw the main menu
    if menu_active:
        win.fill(BACKGROUND_COLOR)
        title_text = font.render("Snake Game", True, SNAKE_COLOR)
        win.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() // 2))
        start_text = font.render("Press Space to Start", True, SNAKE_COLOR)
        win.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + title_text.get_height() // 2))

    # Draw the game
    else:
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

        win.fill(BACKGROUND_COLOR)
        for pos in snake_body:
            pygame.draw.rect(win, SNAKE_COLOR, (pos[0], pos[1], 10, 10))
        pygame.draw.rect(win, FOOD_COLOR, (food_pos[0], food_pos[1], 10, 10))

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    time.sleep(0.1)

    # Check for collisions with the wall or itself
    if not menu_active:
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
