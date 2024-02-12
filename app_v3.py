import pygame
import numpy as np
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
SQUARE_SIZE = 0  # Will be calculated based on board size
BOARD_ROWS, BOARD_COLS = 3, 3
CUSTOM_BOARD_SIZE = False  # Flag for custom board size
AI_LEVEL = "easy"
game_over = False  # Initialize game_over

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

board = np.zeros((BOARD_ROWS, BOARD_COLS))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)


def ai_move_impossible():
    global board  # Add global keyword
    # Impossible difficulty AI: Implements a perfect game strategy
    # For Tic Tac Toe, this would involve searching for the optimal move using a game tree algorithm (e.g., minimax)
    # For simplicity, let's assume the AI always wins or forces a tie if winning is not possible
    # You can replace this with a more sophisticated algorithm if desired
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if available_square(row, col):
                board[row][col] = 2
                if check_win(2):
                    return
                board[row][col] = 1
                if check_win(1):
                    mark_square(row, col, 2)
                    return
                board[row][col] = 0

    ai_move_medium()  # If no winning moves found, use a fallback strategy (e.g., medium difficulty)


def ai_move_medium():
    global board  # Add global keyword
    # Medium difficulty AI: Tries to block player from winning and go for winning moves
    # Otherwise, makes a random move
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if available_square(row, col):
                # Check if AI wins by making this move
                board[row][col] = 2
                if check_win(2):
                    return
                board[row][col] = 0  # Reset the move

                # Check if player wins by making this move
                board[row][col] = 1
                if check_win(1):
                    mark_square(row, col, 2)
                    return
                board[row][col] = 0  # Reset the move

    # If no winning moves found, make a random move
    ai_move_easy()


def end_game(winner):
    global game_over  # Add global keyword
    if winner == 1:
        print("Player wins!")
    elif winner == 2:
        print("AI wins!")
    else:
        print("It's a tie!")

    # Add option to close the window after game ends
    # print("Press any key to exit.")
    game_over = True  # Set game_over to True


# Define functions
def ai_move_easy():
    global board  # Add global keyword
    # Simple AI that makes random moves
    while True:
        row = np.random.randint(0, BOARD_ROWS)
        col = np.random.randint(0, BOARD_COLS)
        if available_square(row, col):
            mark_square(row, col, 2)
            break


def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, BLACK, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, BLACK, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    global board  # Add global keyword
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (
                    int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), 60, 15)
            elif board[row][col] == 2:
                pygame.draw.line(screen, BLUE, (col * SQUARE_SIZE + 55, row * SQUARE_SIZE + SQUARE_SIZE - 55),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 55, row * SQUARE_SIZE + 55), LINE_WIDTH)
                pygame.draw.line(screen, BLUE, (col * SQUARE_SIZE + 55, row * SQUARE_SIZE + 55),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 55, row * SQUARE_SIZE + SQUARE_SIZE - 55),
                                 LINE_WIDTH)


def mark_square(row, col, player):
    global board  # Add global keyword
    board[row][col] = player


def available_square(row, col):
    global board  # Add global keyword
    return board[row][col] == 0


def is_board_full():
    global board  # Add global keyword
    return np.all(board != 0)


def check_win(player):
    global board  # Add global keyword
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


def get_custom_options():
    global BOARD_ROWS, BOARD_COLS, CUSTOM_BOARD_SIZE, AI_LEVEL  # Add global keyword
    print("Welcome to Tic Tac Toe!")
    customize = input("Would you like to customize the game settings? (yes/no): ").lower()
    if customize == "yes":
        CUSTOM_BOARD_SIZE = True
        BOARD_ROWS = 3  # int(input("Enter the number of rows for the board: "))
        BOARD_COLS = 3  # int(input("Enter the number of columns for the board: "))
        AI_LEVEL = input("Enter the AI level for the game (easy/medium/hard): ")


def initialize_game():
    global screen, board, player, current_player, difficulty, SQUARE_SIZE  # Add global keyword
    # Initialize the game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")
    screen.fill(WHITE)

    # Initialize the board size
    initialize_board()
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    player = 1
    current_player = 1  # Track the current player for single-player mode
    difficulty = AI_LEVEL


def initialize_board():
    global SQUARE_SIZE  # Add global keyword
    global board  # Add global keyword
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    if CUSTOM_BOARD_SIZE:
        SQUARE_SIZE = min(WIDTH // BOARD_COLS, HEIGHT // BOARD_ROWS)
    else:
        SQUARE_SIZE = WIDTH // BOARD_COLS


def main():
    global current_player  # Add this line to declare current_player as global
    global game_over  # Add global keyword
    global screen
    global player
    global difficulty
    # Get customization options from the user
    get_custom_options()

    running = True
    while running:
        initialize_game()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = True
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and current_player == 1 \
                        and not check_win(1) and not check_win(2):
                    mouseX = event.pos[0] // SQUARE_SIZE
                    mouseY = event.pos[1] // SQUARE_SIZE

                    if available_square(mouseY, mouseX):
                        mark_square(mouseY, mouseX, player)
                        if check_win(player):
                            print("Player", player, "wins!")
                            game_over = True
                        elif is_board_full():
                            print("It's a tie!")
                            game_over = True
                        else:
                            current_player = 2

                if current_player == 2 and not check_win(1) and not check_win(2):
                    if difficulty == "easy":
                        ai_move_easy()
                    elif difficulty == "medium":
                        ai_move_medium()
                    elif difficulty == "hard":
                        ai_move_impossible()
                    if check_win(2):
                        end_game(2)
                        game_over = True
                    elif is_board_full():
                        end_game(0)
                        game_over = True

                    current_player = 1
                    if check_win(2):
                        end_game(2)
                        game_over = True
                    elif is_board_full():
                        end_game(0)
                        game_over = True

            screen.fill(WHITE)
            draw_lines()
            draw_figures()
            pygame.display.update()

        print("Game over!")
        pygame.quit()
        # sys.exit()
        play_again = input("Do you want to play again? (yes/no): ").lower()

        if play_again != "yes":
            running = False
        else:
            game_over = False
            running = True
            get_custom_options()

            # Initialize the game window
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Tic Tac Toe")
            screen.fill(WHITE)

            # Initialize the board size
            initialize_board()
            board = np.zeros((BOARD_ROWS, BOARD_COLS))
            player = 1
            current_player = 1  # Track the current player for single-player mode
            difficulty = AI_LEVEL

    pygame.quit()
    sys.exit()


# Call the main function
if __name__ == "__main__":
    main()
