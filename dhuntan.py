import pygame
import random
import sys

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Set the width and height of each block
block_width = 20
block_height = 20

# Set the margin between blocks
margin = 5

# Set the screen dimensions
screen_width = 400
screen_height = 500

# Set the size of the grid
grid_width = screen_width // (block_width + margin)
grid_height = screen_height // (block_height + margin)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption("Tetris")

# Define the shapes of the Tetris pieces
shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

# Define the colors of the Tetris pieces
colors = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (128, 128, 128)  # Gray
]

# Initialize the grid
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

# Initialize the current piece
def new_piece():
    return {
        "shape": random.choice(shapes),
        "color": random.choice(colors),
        "x": grid_width // 2,
        "y": 0
    }

current_piece = new_piece()

# Initialize the score
score = 0

# Function to check for collision
def check_collision(grid, piece):
    for y, row in enumerate(piece["shape"]):
        for x, val in enumerate(row):
            if val:
                if (piece["y"] + y >= grid_height or
                        piece["x"] + x < 0 or
                        piece["x"] + x >= grid_width or
                        grid[piece["y"] + y][piece["x"] + x]):
                    return True
    return False

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the current piece down
    current_piece["y"] += 1

    # Check for collisions
    if check_collision(grid, current_piece):
        # Collision detected, move the piece back up
        current_piece["y"] -= 1

        # Add the piece to the grid
        for y, row in enumerate(current_piece["shape"]):
            for x, val in enumerate(row):
                if val:
                    grid[current_piece["y"] + y][current_piece["x"] + x] = current_piece["color"]

        # Check for full rows
        grid = [row for row in grid if any(val == 0 for val in row)]
        while len(grid) < grid_height:
            grid.insert(0, [0 for _ in range(grid_width)])

        # Increase the score
        score += 1

        # Get a new piece
        current_piece = new_piece()

    # Draw everything
    screen.fill(BLACK)
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val:
                pygame.draw.rect(screen, val, (x * (block_width + margin) + margin, y * (block_height + margin) + margin, block_width, block_height))

    # Draw the current piece
    for y, row in enumerate(current_piece["shape"]):
        for x, val in enumerate(row):
            if val:
                pygame.draw.rect(screen, current_piece["color"], (current_piece["x"] * (block_width + margin) + x * (block_width + margin) + margin, current_piece["y"] * (block_height + margin) + y * (block_height + margin) + margin, block_width, block_height))

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(100)
