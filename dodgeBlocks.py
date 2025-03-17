import pygame
import random

# Initialize pygame
pygame.init()

# Set up game window
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dodge the Falling Blocks')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_width = 50
player_height = 50
player_x = screen_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Block settings
block_width = 50
block_height = 50
block_speed = 5

# Game clock
clock = pygame.time.Clock()
score = 0

# Font
font = pygame.font.SysFont(None, 36)

def draw_player(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, player_width, player_height))

def draw_block(x, y):
    pygame.draw.rect(screen, RED, (x, y, block_width, block_height))

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Main game loop
def game_loop():
    global player_x, score

    # Block position
    block_x = random.randint(0, screen_width - block_width)
    block_y = -block_height

    # Game loop
    running = True
    while running:
        screen.fill(WHITE)
        draw_score(score)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        # Move block
        block_y += block_speed

        # Check collision
        if block_y + block_height > player_y and block_x + block_width > player_x and block_x < player_x + player_width:
            print("Game Over!")
            running = False

        # Respawn block
        if block_y > screen_height:
            block_y = -block_height
            block_x = random.randint(0, screen_width - block_width)
            score += 1

        # Draw everything
        draw_player(player_x, player_y)
        draw_block(block_x, block_y)

        pygame.display.update()

        # Frame rate
        clock.tick(60)

    pygame.quit()

# Run the game
game_loop()