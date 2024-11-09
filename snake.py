import pygame
import sys
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
score_font = pygame.font.Font(None, 24)

# Main menu and game over variables
menu_active = True
game_over = False

# Initialize game variables
snake_pos = [100, 50]
food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
snake_body = [[100, 50], [90, 50], [80, 50]]
score = 0

# Set up the direction
direction = 'RIGHT'
next_direction = 'RIGHT'

# Initialize the clock and movement timing
clock = pygame.time.Clock()
desired_fps = 120  # Set high fps for smooth rendering
snake_speed = 40  # Milliseconds per snake movement update
last_move_time = pygame.time.get_ticks()  # Last time snake moved

def reset_game():
    global snake_pos, food_pos, snake_body, direction, next_direction, score, menu_active, game_over, last_move_time
    snake_pos = [100, 50]
    food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    next_direction = 'RIGHT'
    score = 0
    menu_active = True
    game_over = False
    last_move_time = pygame.time.get_ticks()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if menu_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_active = False

        elif game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

        else:  # Game is active
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    next_direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    next_direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    next_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    next_direction = 'RIGHT'

    # Draw the main menu
    if menu_active:
        win.fill(BACKGROUND_COLOR)
        title_text = font.render("Snake Game", True, SNAKE_COLOR)
        win.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() // 2))
        start_text = font.render("Press Space to Start", True, SNAKE_COLOR)
        win.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + title_text.get_height() // 2))

    elif game_over:
        # Display Game Over screen
        win.fill(BACKGROUND_COLOR)
        game_over_text = font.render("Game Over", True, SNAKE_COLOR)
        win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        retry_text = font.render("Press 'R' to Retry", True, SNAKE_COLOR)
        win.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() // 2))

    else:
        # Check if it's time to move the snake
        current_time = pygame.time.get_ticks()
        if current_time - last_move_time > snake_speed:
            # Move the snake
            direction = next_direction  # Update direction only once per movement interval
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
                score += 1
                food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
            else:
                if len(snake_body) > 0:  # Remove the last segment of the snake body if it didn't eat any food
                    snake_body.pop()

            # Add new segment to the body
            snake_body.insert(0, list(snake_pos))

            # Update last movement time
            last_move_time = current_time

        # Draw everything
        win.fill(BACKGROUND_COLOR)
        for pos in snake_body:
            pygame.draw.rect(win, SNAKE_COLOR, (pos[0], pos[1], 10, 10))
        pygame.draw.rect(win, FOOD_COLOR, (food_pos[0], food_pos[1], 10, 10))

        # Display score
        score_text = score_font.render("Score: " + str(score), True, SNAKE_COLOR)
        win.blit(score_text, (10, 10))

        # Check for collisions with the wall or itself
        if snake_pos[0] < 0 or snake_pos[0] > WIDTH - 10 or snake_pos[1] < 0 or snake_pos[1] > HEIGHT - 10:
            game_over = True
        for block in snake_body[1:]:
            if block == snake_pos:
                game_over = True

    # Update the display
    pygame.display.update()

    # Control frame rate using clock
    clock.tick(desired_fps)  # Controls rendering frame rate for smooth visuals
