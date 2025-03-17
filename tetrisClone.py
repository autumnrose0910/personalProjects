import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
COLOR_LIST = [CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, PURPLE]

# Block size
BLOCK_SIZE = 30

# Grid dimensions
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Define shapes and colors
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1, 1]],  # I
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

# Grid for the game (initialize as empty)
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Class for the tetrominoes
class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

# Function to draw the grid
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(SCREEN, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Function to draw a piece on the screen
def draw_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(SCREEN, piece.color, (piece.x * BLOCK_SIZE + x * BLOCK_SIZE, piece.y * BLOCK_SIZE + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Function to check for collisions
def check_collision(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                if (piece.y + y >= GRID_HEIGHT or
                    piece.x + x < 0 or
                    piece.x + x >= GRID_WIDTH or
                    grid[piece.y + y][piece.x + x] != 0):
                    return True
    return False

# Function to place the tetromino in the grid
def place_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[piece.y + y][piece.x + x] = piece.color

# Function to clear lines
def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    lines_cleared = GRID_HEIGHT - len(new_grid)
    grid = [[0] * GRID_WIDTH for _ in range(lines_cleared)] + new_grid
    return lines_cleared

# Function to draw the game
def draw_game(piece):
    SCREEN.fill((0, 0, 0))  # Clear the screen
    draw_grid()  # Draw the grid
    draw_piece(piece)  # Draw the current piece
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(SCREEN, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.display.update()

# Main game loop
def game_loop():
    clock = pygame.time.Clock()
    piece = Tetromino(random.choice(SHAPES), random.choice(COLOR_LIST))
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece.move(-1, 0)
                    if check_collision(piece):
                        piece.move(1, 0)
                elif event.key == pygame.K_RIGHT:
                    piece.move(1, 0)
                    if check_collision(piece):
                        piece.move(-1, 0)
                elif event.key == pygame.K_DOWN:
                    piece.move(0, 1)
                    if check_collision(piece):
                        piece.move(0, -1)
                elif event.key == pygame.K_UP:
                    piece.rotate()
                    if check_collision(piece):
                        piece.rotate()
                        piece.rotate()
                        piece.rotate()

        piece.move(0, 1)
        if check_collision(piece):
            piece.move(0, -1)
            place_piece(piece)
            score += clear_lines()
            piece = Tetromino(random.choice(SHAPES), random.choice(COLOR_LIST))
            if check_collision(piece):
                running = False  # Game over if new piece collides immediately

        draw_game(piece)
        clock.tick(10)  # Speed of the game (adjust as necessary)

    pygame.quit()

# Start the game
game_loop()

