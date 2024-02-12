import pygame
import numpy as np
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
SQUARE_SIZE = WIDTH // 3  # Calculate square size based on board size
BOARD_ROWS, BOARD_COLS = 3, 3
CUSTOM_BOARD_SIZE = False  # Flag for custom board size
AI_LEVEL = "easy"
game_over = False  # Initialize game_over

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)

# Initialize the board
board = np.zeros((BOARD_ROWS, BOARD_COLS))


def draw_board():
    # Draw horizontal lines
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    # Draw vertical lines
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                  row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3, 10)
            elif board[row][col] == 2:
                pygame.draw.line(screen, BLUE, (col * SQUARE_SIZE + 0.2 * SQUARE_SIZE, row * SQUARE_SIZE + 0.8 * SQUARE_SIZE),
                                 (col * SQUARE_SIZE + 0.8 * SQUARE_SIZE, row * SQUARE_SIZE + 0.2 * SQUARE_SIZE), 10)
                pygame.draw.line(screen, BLUE, (col * SQUARE_SIZE + 0.2 * SQUARE_SIZE, row * SQUARE_SIZE + 0.2 * SQUARE_SIZE),
                                 (col * SQUARE_SIZE + 0.8 * SQUARE_SIZE, row * SQUARE_SIZE + 0.8 * SQUARE_SIZE), 10)


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0


def is_board_full():
    return np.all(board != 0)


def check_win(player):
    # Check rows
    for row in range(BOARD_ROWS):
        if np.all(board[row] == player):
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if np.all(board[:, col] == player):
            return True
    # Check diagonals
    if np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board)) == player):
        return True
    return False


def ai_move_easy():
    while True:
        row = np.random.randint(0, BOARD_ROWS)
        col = np.random.randint(0, BOARD_COLS)
        if available_square(row, col):
            mark_square(row, col, 2)
            break


def handle_click(row, col):
    if available_square(row, col):
        mark_square(row, col, 1)
        if check_win(1):
            print("Player wins!")
            return True
        elif is_board_full():
            print("It's a tie!")
            return True
        else:
            ai_move_easy()
            if check_win(2):
                print("AI wins!")
                return True
            elif is_board_full():
                print("It's a tie!")
                return True
    return False


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE
            if handle_click(mouseY, mouseX):
                game_over = True

    screen.fill(WHITE)
    draw_board()
    draw_figures()
    pygame.display.update()

pygame.quit()
sys.exit()
