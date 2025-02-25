import pygame
import random

# Initialize Pygame
pygame.init()

# Game window settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10  # 10x10 board
CELL_SIZE = WIDTH // COLS

# Colors for the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)  # Player color
BLUE = (0, 0, 255)  # AI color

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Adaptive Snake and Ladders")

# Load images for snakes, ladders, and dice
snake_img = pygame.image.load("C:\\Users\\shash\\OneDrive\\Desktop\\ai project\\snakes.png")
ladder_img = pygame.image.load("C:\\Users\\shash\\OneDrive\\Desktop\\ai project\\ladders.png")

# Resize images
snake_img = pygame.transform.scale(snake_img, (80, 150))
ladder_img = pygame.transform.scale(ladder_img, (80, 150))

# Load dice images (dice1.png to dice6.png)
dice_images = [pygame.image.load(f"C:\\Users\\shash\\OneDrive\\Desktop\\ai project\\dice{i}.png") for i in range(1, 7)]
dice_images = [pygame.transform.scale(img, (60, 60)) for img in dice_images]  # Resize dice images

# Original snakes and ladders (never removed)
original_ladders = {3: 22, 8: 30, 28: 84, 58: 77}
original_snakes = {99: 10, 95: 56, 52: 29, 79: 41}

# Dynamic ladders and snakes (change during gameplay)
dynamic_ladders = {}
dynamic_snakes = {}

# Player and AI positions
player_pos = 1
ai_pos = 1
turn = "player"
turn_count = 0  # Track turns

dice_value = 1
rolling = False  # Dice animation flag

def draw_board():
    """Draw the board with numbers, ladders, and snakes."""
    screen.fill(WHITE)

    # Draw grid and numbers
    for row in range(ROWS):
        for col in range(COLS):
            cell_num = row * COLS + col + 1
            x, y = col * CELL_SIZE, HEIGHT - (row + 1) * CELL_SIZE
            pygame.draw.rect(screen, WHITE if cell_num % 2 == 0 else (230, 230, 230), (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
            font = pygame.font.Font(None, 24)
            text = font.render(str(cell_num), True, BLACK)
            screen.blit(text, (x + 10, y + 10))

    # Draw ladders (both original and dynamic)
    for start, end in {**original_ladders, **dynamic_ladders}.items():
        sx, sy = ((start - 1) % 10) * CELL_SIZE, HEIGHT - ((start - 1) // 10 + 1) * CELL_SIZE
        screen.blit(ladder_img, (sx, sy))

    # Draw snakes (both original and dynamic)
    for start, end in {**original_snakes, **dynamic_snakes}.items():
        sx, sy = ((start - 1) % 10) * CELL_SIZE, HEIGHT - ((start - 1) // 10 + 1) * CELL_SIZE
        screen.blit(snake_img, (sx, sy))

def move_player(position, roll):
    """Move the player and check for snakes and ladders."""
    new_pos = position + roll

    # Check for ladders (original and dynamic)
    if new_pos in original_ladders:
        new_pos = original_ladders[new_pos]
    elif new_pos in dynamic_ladders:
        new_pos = dynamic_ladders[new_pos]

    # Check for snakes (original and dynamic)
    if new_pos in original_snakes:
        new_pos = original_snakes[new_pos]
    elif new_pos in dynamic_snakes:
        new_pos = dynamic_snakes[new_pos]

    return min(new_pos, 100)  # Ensure position doesn't go past 100

def ai_move():
    """AI rolls the dice and moves."""
    global ai_pos
    roll = random.randint(1, 6)
    new_pos = move_player(ai_pos, roll)
    return new_pos, roll

def roll_dice():
    """Simulate rolling dice animation."""
    global dice_value, rolling
    rolling = True

    for _ in range(10):  # Rolling effect
        dice_value = random.randint(1, 6)
        pygame.time.delay(50)
        draw_game()

    rolling = False
    return dice_value

def update_dynamic_board():
    """Adjust difficulty by adding new ladders or snakes dynamically."""
    global dynamic_ladders, dynamic_snakes

    dynamic_ladders.clear()
    dynamic_snakes.clear()

    if ai_pos > player_pos:  # AI winning → Add snakes
        for _ in range(2):
            start = random.randint(20, 99)
            end = random.randint(5, start - 10)
            if start not in original_snakes:
                dynamic_snakes[start] = end

    if player_pos < ai_pos - 10:  # Player losing → Add ladders
        for _ in range(2):
            start = random.randint(5, 70)
            end = random.randint(start + 10, 95)
            if start not in original_ladders:
                dynamic_ladders[start] = end

def draw_game():
    """Render the game board, players, and dice roll."""
    draw_board()

    # Draw players
    px, py = ((player_pos - 1) % 10) * CELL_SIZE, HEIGHT - ((player_pos - 1) // 10 + 1) * CELL_SIZE
    ax, ay = ((ai_pos - 1) % 10) * CELL_SIZE, HEIGHT - ((ai_pos - 1) // 10 + 1) * CELL_SIZE

    pygame.draw.circle(screen, RED, (px + CELL_SIZE // 2, py + CELL_SIZE // 2), 15)
    pygame.draw.circle(screen, BLUE, (ax + CELL_SIZE // 2, ay + CELL_SIZE // 2), 15)

    # Display dice roll
    screen.blit(dice_images[dice_value - 1], (260, 50))

    pygame.display.update()

# Main game loop
running = True
while running:
    draw_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and turn == "player" and not rolling:
            dice_value = roll_dice()
            player_pos = move_player(player_pos, dice_value)
            turn = "ai"

    if turn == "ai" and not rolling:
        ai_pos, ai_roll = ai_move()
        dice_value = ai_roll
        turn = "player"

    turn_count += 1
    if turn_count % 5 == 0:
        update_dynamic_board()
 
if player_pos == 100:
        font = pygame.font.Font(None, 48)
        text = font.render("You Win!", True, RED)
        screen.blit(text, (250, 300))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False
elif ai_pos == 100:
        font = pygame.font.Font(None, 48)
        text = font.render("AI Wins!", True, BLUE)
        screen.blit(text, (250, 300))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False


pygame.time.delay(500)

pygame.quit()